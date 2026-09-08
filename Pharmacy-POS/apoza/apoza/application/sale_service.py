from datetime import date, datetime

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from apoza.application.audit import AuditLogger
from apoza.application.errors import AppError
from apoza.domain.enums import SaleStatus
from apoza.domain.rules import PaymentExpert, SaleExpert, SalesLineExpert, StockBatchExpert, money
from apoza.persistence.tables import (
    Customer,
    Medicine,
    Payment,
    Prescription,
    PrescriptionItem,
    Sale,
    SaleItem,
    StockBatch,
    User,
)


class SaleService:
    """Coordinates UC-02 / UC-09. completeSale is one unit of work (R-01 / NFR-04)."""

    def __init__(self, db: Session):
        self.db = db
        self.audit = AuditLogger(db)

    def _recompute(self, sale: Sale) -> None:
        items = self.db.query(SaleItem).filter(SaleItem.sale_id == sale.sale_id).all()
        totals = [item.line_total for item in items]
        sale.subtotal = SaleExpert.total(totals)
        sale.total = sale.subtotal

    def current_or_new(self, user: User) -> Sale:
        sale = (
            self.db.query(Sale)
            .options(joinedload(Sale.items).joinedload(SaleItem.medicine),
                     joinedload(Sale.items).joinedload(SaleItem.batch),
                     joinedload(Sale.customer),
                     joinedload(Sale.prescription))
            .filter(Sale.sold_by_user_id == user.user_id, Sale.status == SaleStatus.IN_PROGRESS)
            .order_by(Sale.started_at.desc())
            .first()
        )
        if sale:
            return sale
        return self.make_new_sale(user)

    def make_new_sale(self, user: User) -> Sale:
        sale = Sale(
            sold_by_user_id=user.user_id,
            status=SaleStatus.IN_PROGRESS,
            started_at=datetime.utcnow(),
            subtotal=money(0),
            total=money(0),
        )
        self.db.add(sale)
        self.db.commit()
        self.db.refresh(sale)
        return sale

    def lookup_by_code(self, code: str) -> Medicine | None:
        """Exact match on product code (case-insensitive). Used for barcode/QR scans."""
        normalized = (code or "").strip().upper()
        if not normalized:
            return None
        return (
            self.db.query(Medicine)
            .options(joinedload(Medicine.batches))
            .filter(Medicine.is_active.is_(True), func.upper(Medicine.product_code) == normalized)
            .one_or_none()
        )

    def add_by_code(self, sale: Sale, code: str, quantity: int = 1) -> SaleItem:
        medicine = self.lookup_by_code(code)
        if not medicine:
            raise AppError(
                f"Product code \"{(code or '').strip()}\" was not found. "
                "Scan the QR/barcode or enter the code printed on the package."
            )
        return self.enter_item(sale, medicine.medicine_id, quantity)

    def requires_prescription_capture(self, sale: Sale) -> bool:
        return self._needs_prescription(sale) and not sale.prescription_id

    def _walk_in_customer(self) -> Customer:
        customer = self.db.query(Customer).filter(Customer.full_name == "Walk-in").one_or_none()
        if customer:
            return customer
        customer = Customer(full_name="Walk-in")
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def search_medicines(self, query: str) -> list[dict]:
        q = (query or "").strip()
        if not q:
            return []
        like = f"%{q}%"
        medicines = (
            self.db.query(Medicine)
            .options(joinedload(Medicine.batches))
            .filter(
                Medicine.is_active.is_(True),
                (Medicine.name.ilike(like))
                | (Medicine.generic_name.ilike(like))
                | (Medicine.product_code.ilike(like)),
            )
            .order_by(Medicine.name)
            .limit(20)
            .all()
        )
        today = date.today()
        rows = []
        for med in medicines:
            sellable = sum(
                b.quantity_on_hand
                for b in med.batches
                if StockBatchExpert.is_sellable(b.expiry_date, b.quantity_on_hand, 1, today)
            )
            rows.append({
                "medicine_id": med.medicine_id,
                "product_code": med.product_code,
                "name": med.name,
                "generic_name": med.generic_name,
                "strength": med.strength,
                "unit_price": money(med.unit_price),
                "requires_prescription": med.requires_prescription,
                "sellable_qty": sellable,
            })
        return rows

    def _find_sellable_batch(self, medicine_id: int, qty: int) -> StockBatch:
        today = date.today()
        batches = (
            self.db.query(StockBatch)
            .filter(StockBatch.medicine_id == medicine_id)
            .order_by(StockBatch.expiry_date.asc())
            .with_for_update(nowait=False)
            .all()
        )
        for batch in batches:
            if StockBatchExpert.is_sellable(batch.expiry_date, batch.quantity_on_hand, qty, today):
                return batch
        expired_only = [
            b for b in batches
            if b.quantity_on_hand >= qty and b.expiry_date < today
        ]
        if expired_only:
            raise AppError("That quantity is only available on an expired batch. Sale refused.")
        on_hand = sum(b.quantity_on_hand for b in batches if b.expiry_date >= today)
        raise AppError(f"Not enough sellable stock. Available: {on_hand}.")

    def enter_item(self, sale: Sale, medicine_id: int, quantity: int) -> SaleItem:
        if sale.status != SaleStatus.IN_PROGRESS:
            raise AppError("This sale is no longer in progress.")
        if quantity <= 0:
            raise AppError("Quantity must be at least 1.")
        medicine = self.db.get(Medicine, medicine_id)
        if not medicine or not medicine.is_active:
            raise AppError("Medicine was not found or is not active.")
        batch = self._find_sellable_batch(medicine_id, quantity)
        line = SaleItem(
            sale_id=sale.sale_id,
            medicine_id=medicine.medicine_id,
            batch_id=batch.batch_id,
            quantity=quantity,
            unit_price=money(medicine.unit_price),
            line_total=SalesLineExpert.line_total(quantity, medicine.unit_price),
        )
        self.db.add(line)
        self.db.flush()
        self.db.refresh(sale)
        self._recompute(sale)
        self.db.commit()
        return line

    def remove_line(self, sale: Sale, sale_item_id: int) -> None:
        if sale.status != SaleStatus.IN_PROGRESS:
            raise AppError("This sale is no longer in progress.")
        item = self.db.get(SaleItem, sale_item_id)
        if not item or item.sale_id != sale.sale_id:
            raise AppError("Line was not found.")
        self.db.delete(item)
        self.db.flush()
        self.db.refresh(sale)
        self._recompute(sale)
        self.db.commit()

    def find_customers(self, query: str) -> list[Customer]:
        q = (query or "").strip()
        if not q:
            return []
        like = f"%{q}%"
        return (
            self.db.query(Customer)
            .filter((Customer.full_name.ilike(like)) | (Customer.phone.ilike(like)))
            .order_by(Customer.full_name)
            .limit(20)
            .all()
        )

    def record_customer(self, full_name: str, phone: str | None = None, address: str | None = None) -> Customer:
        if not full_name.strip():
            raise AppError("Customer name is required.")
        customer = Customer(full_name=full_name.strip(), phone=(phone or "").strip() or None,
                            address=(address or "").strip() or None)
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def attach_customer(self, sale: Sale, customer_id: int) -> None:
        customer = self.db.get(Customer, customer_id)
        if not customer:
            raise AppError("Customer not found.")
        sale.customer_id = customer.customer_id
        self.db.commit()

    def attach_prescription(self, sale: Sale, user: User, reference_no: str,
                            prescriber_name: str | None, issued_on: date | None) -> Prescription:
        if sale.status != SaleStatus.IN_PROGRESS:
            raise AppError("This sale is no longer in progress.")
        if not reference_no.strip():
            raise AppError("Prescription reference is required.")
        customer = self._walk_in_customer()
        rx = Prescription(
            customer_id=customer.customer_id,
            reference_no=reference_no.strip(),
            prescriber_name=(prescriber_name or "").strip() or None,
            issued_on=issued_on,
            recorded_by_user_id=user.user_id,
        )
        self.db.add(rx)
        self.db.flush()
        seen = set()
        for item in sale.items:
            if item.medicine.requires_prescription and item.medicine_id not in seen:
                self.db.add(PrescriptionItem(
                    prescription_id=rx.prescription_id,
                    medicine_id=item.medicine_id,
                    quantity=item.quantity,
                ))
                seen.add(item.medicine_id)
        sale.customer_id = customer.customer_id
        sale.prescription_id = rx.prescription_id
        self.db.commit()
        return rx

    def _needs_prescription(self, sale: Sale) -> bool:
        self.db.refresh(sale)
        items = sale.items
        return any(self.db.get(Medicine, i.medicine_id).requires_prescription for i in items)

    def end_sale_guard(self, sale: Sale) -> None:
        if sale.status != SaleStatus.IN_PROGRESS:
            raise AppError("This sale is no longer in progress.")
        if not sale.items:
            raise AppError("Add at least one medicine before payment.")
        if self._needs_prescription(sale) and not sale.prescription_id:
            raise AppError("A prescription-only item is on this sale. Attach prescription details first.")

    def complete_sale(self, sale: Sale, user: User, method: str, amount_tendered, external_reference: str | None) -> Sale:
        """CO-02 makePayment — payment, completion, and stock move together."""
        self.end_sale_guard(sale)
        ok, msg = PaymentExpert.is_acceptable(method, amount_tendered, sale.total)
        if not ok:
            raise AppError(msg)
        change = PaymentExpert.change_due(method, amount_tendered, sale.total)

        try:
            for item in sale.items:
                batch = (
                    self.db.query(StockBatch)
                    .filter(StockBatch.batch_id == item.batch_id)
                    .with_for_update()
                    .one()
                )
                if not StockBatchExpert.is_sellable(batch.expiry_date, batch.quantity_on_hand, item.quantity):
                    raise AppError(
                        f"Stock changed for {item.medicine.name}. The line is no longer sellable."
                    )
                batch.quantity_on_hand -= item.quantity

            payment = Payment(
                sale_id=sale.sale_id,
                method=method.upper(),
                amount_tendered=money(amount_tendered),
                change_due=change,
                external_reference=(external_reference or "").strip() or None,
                paid_at=datetime.utcnow(),
            )
            self.db.add(payment)
            sale.status = SaleStatus.COMPLETED
            sale.completed_at = datetime.utcnow()
            self._recompute(sale)
            self.audit.write(
                "SALE_COMPLETE", user.user_id, "sales", sale.sale_id,
                f"total={sale.total} method={method.upper()}",
            )
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        return sale

    def cancel_in_progress(self, sale: Sale, user: User, reason: str = "Cancelled before payment") -> None:
        if sale.status != SaleStatus.IN_PROGRESS:
            raise AppError("Only an in-progress sale can be cancelled this way.")
        sale.status = SaleStatus.VOIDED
        sale.void_reason = reason
        sale.completed_at = datetime.utcnow()
        self.audit.write("VOID", user.user_id, "sales", sale.sale_id, reason)
        self.db.commit()

    def void_sale(self, sale_id: int, user: User, reason: str) -> Sale:
        if not (reason or "").strip():
            raise AppError("A void reason is required.")
        sale = (
            self.db.query(Sale)
            .options(joinedload(Sale.items))
            .filter(Sale.sale_id == sale_id)
            .one_or_none()
        )
        if not sale:
            raise AppError("Sale not found.")
        if sale.status == SaleStatus.VOIDED:
            raise AppError("This sale is already voided.")
        if sale.status == SaleStatus.COMPLETED:
            for item in sale.items:
                batch = (
                    self.db.query(StockBatch)
                    .filter(StockBatch.batch_id == item.batch_id)
                    .with_for_update()
                    .one()
                )
                batch.quantity_on_hand += item.quantity
        sale.status = SaleStatus.VOIDED
        sale.void_reason = reason.strip()
        sale.completed_at = datetime.utcnow()
        self.audit.write("VOID", user.user_id, "sales", sale.sale_id, reason.strip())
        self.db.commit()
        return sale

    def get_sale(self, sale_id: int) -> Sale | None:
        return (
            self.db.query(Sale)
            .options(
                joinedload(Sale.items).joinedload(SaleItem.medicine),
                joinedload(Sale.items).joinedload(SaleItem.batch),
                joinedload(Sale.payment),
                joinedload(Sale.sold_by),
                joinedload(Sale.customer),
                joinedload(Sale.prescription),
            )
            .filter(Sale.sale_id == sale_id)
            .one_or_none()
        )

    def todays_sales(self, user_id: int | None = None) -> list[Sale]:
        today = datetime.utcnow().date()
        q = (
            self.db.query(Sale)
            .options(joinedload(Sale.payment), joinedload(Sale.sold_by))
            .filter(func.date(Sale.started_at) == today)
            .order_by(Sale.started_at.desc())
        )
        if user_id:
            q = q.filter(Sale.sold_by_user_id == user_id)
        return q.all()
