from datetime import date, datetime, timedelta
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from apoza.application.audit import AuditLogger
from apoza.application.errors import AppError
from apoza.domain.rules import ADJUST_REASONS, StockBatchExpert
from apoza.persistence.tables import (
    Medicine,
    PharmacySettings,
    Sale,
    StockAdjustment,
    StockBatch,
    StockReceipt,
    StockReceiptLine,
    Supplier,
    User,
)


class InventoryService:
    def __init__(self, db: Session):
        self.db = db
        self.audit = AuditLogger(db)

    def settings(self) -> PharmacySettings:
        row = self.db.query(PharmacySettings).first()
        if not row:
            raise AppError("Pharmacy settings are missing.")
        return row

    def batches(self) -> list[StockBatch]:
        return (
            self.db.query(StockBatch)
            .options(joinedload(StockBatch.medicine))
            .order_by(StockBatch.expiry_date)
            .all()
        )

    def receive_stock(self, user: User, supplier_id: int, reference_note: str | None,
                      lines: list[dict]) -> StockReceipt:
        if not lines:
            raise AppError("Add at least one receipt line.")
        supplier = self.db.get(Supplier, supplier_id)
        if not supplier or not supplier.is_active:
            raise AppError("Select an active supplier.")
        receipt = StockReceipt(
            supplier_id=supplier.supplier_id,
            received_by_user_id=user.user_id,
            reference_note=(reference_note or "").strip() or None,
        )
        self.db.add(receipt)
        self.db.flush()
        today = date.today()
        for line in lines:
            medicine = self.db.get(Medicine, int(line["medicine_id"]))
            if not medicine:
                raise AppError("A medicine on the receipt was not found.")
            qty = int(line["quantity"])
            if qty <= 0:
                raise AppError("Receipt quantity must be positive.")
            expiry = line["expiry_date"]
            if isinstance(expiry, str):
                expiry = date.fromisoformat(expiry)
            if expiry <= today:
                raise AppError(f"{medicine.name}: expiry must be in the future.")
            batch_number = str(line["batch_number"]).strip()
            if not batch_number:
                raise AppError("Batch number is required.")
            batch = (
                self.db.query(StockBatch)
                .filter(
                    StockBatch.medicine_id == medicine.medicine_id,
                    StockBatch.batch_number == batch_number,
                    StockBatch.expiry_date == expiry,
                )
                .one_or_none()
            )
            if batch is None:
                cost = line.get("unit_cost")
                batch = StockBatch(
                    medicine_id=medicine.medicine_id,
                    batch_number=batch_number,
                    expiry_date=expiry,
                    quantity_on_hand=0,
                    unit_cost=Decimal(str(cost)) if cost not in (None, "") else None,
                    received_at=datetime.utcnow(),
                )
                self.db.add(batch)
                self.db.flush()
            batch.quantity_on_hand += qty
            self.db.add(StockReceiptLine(receipt_id=receipt.receipt_id, batch_id=batch.batch_id, quantity=qty))
        self.audit.write("STOCK_RECEIPT", user.user_id, "stock_receipts", receipt.receipt_id,
                         f"supplier={supplier.name} lines={len(lines)}")
        self.db.commit()
        return receipt

    def adjust_stock(self, user: User, batch_id: int, quantity_delta: int, reason: str, note: str | None) -> StockBatch:
        reason = (reason or "").upper()
        if reason not in ADJUST_REASONS:
            raise AppError("Choose a reason: damage, expiry, recount, or recall.")
        if quantity_delta == 0:
            raise AppError("Adjustment cannot be zero.")
        batch = self.db.get(StockBatch, batch_id)
        if not batch:
            raise AppError("Batch not found.")
        new_qty = batch.quantity_on_hand + quantity_delta
        if new_qty < 0:
            raise AppError("Adjustment would make quantity negative.")
        batch.quantity_on_hand = new_qty
        self.db.add(StockAdjustment(
            batch_id=batch.batch_id,
            adjusted_by_user_id=user.user_id,
            quantity_delta=quantity_delta,
            reason=reason,
            note=(note or "").strip() or None,
        ))
        self.audit.write("STOCK_ADJUST", user.user_id, "stock_batches", batch.batch_id,
                         f"{reason} delta={quantity_delta}")
        self.db.commit()
        return batch

    def low_stock(self) -> list[dict]:
        rows = []
        medicines = self.db.query(Medicine).filter(Medicine.is_active.is_(True)).all()
        today = date.today()
        for med in medicines:
            on_hand = sum(
                b.quantity_on_hand for b in med.batches
                if StockBatchExpert.is_sellable(b.expiry_date, b.quantity_on_hand, 1, today)
                or b.quantity_on_hand > 0 and b.expiry_date >= today
            )
            if on_hand <= med.reorder_level:
                rows.append({"medicine": med, "on_hand": on_hand})
        return rows

    def near_expiry(self) -> list[StockBatch]:
        days = self.settings().near_expiry_days
        horizon = date.today() + timedelta(days=days)
        today = date.today()
        return (
            self.db.query(StockBatch)
            .options(joinedload(StockBatch.medicine))
            .filter(
                StockBatch.quantity_on_hand > 0,
                StockBatch.expiry_date >= today,
                StockBatch.expiry_date <= horizon,
            )
            .order_by(StockBatch.expiry_date)
            .all()
        )

    def expired(self) -> list[StockBatch]:
        return (
            self.db.query(StockBatch)
            .options(joinedload(StockBatch.medicine))
            .filter(StockBatch.quantity_on_hand > 0, StockBatch.expiry_date < date.today())
            .order_by(StockBatch.expiry_date)
            .all()
        )


class MedicineService:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self, include_inactive: bool = True) -> list[Medicine]:
        q = self.db.query(Medicine).options(joinedload(Medicine.category)).order_by(Medicine.name)
        if not include_inactive:
            q = q.filter(Medicine.is_active.is_(True))
        return q.all()

    def save(self, **data) -> Medicine:
        code = data["product_code"].strip().upper()
        existing = self.db.query(Medicine).filter(Medicine.product_code == code).one_or_none()
        medicine_id = data.get("medicine_id")
        if existing and existing.medicine_id != medicine_id:
            raise AppError("That product code is already in use.")
        if Decimal_safe(data["unit_price"]) < 0:
            raise AppError("Price cannot be negative.")
        if int(data["reorder_level"]) < 0:
            raise AppError("Reorder level cannot be negative.")
        if not data.get("name", "").strip():
            raise AppError("Medicine name is required.")
        if medicine_id:
            med = self.db.get(Medicine, medicine_id)
            if not med:
                raise AppError("Medicine not found.")
        else:
            med = Medicine()
            self.db.add(med)
        med.product_code = code
        med.name = data["name"].strip()
        med.generic_name = (data.get("generic_name") or "").strip() or None
        med.strength = (data.get("strength") or "").strip() or None
        med.form = (data.get("form") or "").strip() or None
        med.category_id = int(data["category_id"]) if data.get("category_id") else None
        med.requires_prescription = bool(data.get("requires_prescription"))
        med.unit_price = Decimal_safe(data["unit_price"])
        med.reorder_level = int(data["reorder_level"])
        med.is_active = bool(data.get("is_active", True))
        self.db.commit()
        return med


def Decimal_safe(value):
    from decimal import Decimal
    return Decimal(str(value or "0"))


class SupplierService:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self, active_only: bool = False) -> list[Supplier]:
        q = self.db.query(Supplier).order_by(Supplier.name)
        if active_only:
            q = q.filter(Supplier.is_active.is_(True))
        return q.all()

    def save(self, supplier_id: int | None, name: str, phone: str | None, address: str | None, is_active: bool = True) -> Supplier:
        if not name.strip():
            raise AppError("Supplier name is required.")
        if supplier_id:
            row = self.db.get(Supplier, supplier_id)
            if not row:
                raise AppError("Supplier not found.")
        else:
            row = Supplier()
            self.db.add(row)
        row.name = name.strip()
        row.phone = (phone or "").strip() or None
        row.address = (address or "").strip() or None
        row.is_active = is_active
        self.db.commit()
        return row


class SettingsService:
    def __init__(self, db: Session):
        self.db = db

    def get(self) -> PharmacySettings:
        return self.db.query(PharmacySettings).first()

    def save(self, name: str, address: str, phone: str, receipt_footer: str, near_expiry_days: int, currency_code: str):
        if not name.strip():
            raise AppError("Pharmacy name is required.")
        if int(near_expiry_days) <= 0:
            raise AppError("Near-expiry days must be a positive number.")
        row = self.get()
        row.name = name.strip()
        row.address = address.strip() or None
        row.phone = phone.strip() or None
        row.receipt_footer = receipt_footer.strip() or None
        row.near_expiry_days = int(near_expiry_days)
        row.currency_code = (currency_code or "ZMW").strip()[:3].upper()
        self.db.commit()
        return row


class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def sales_between(self, start: date, end: date):
        from apoza.domain.enums import SaleStatus
        return (
            self.db.query(func.sum(Sale.total), func.count(Sale.sale_id))
            .filter(Sale.status == SaleStatus.COMPLETED, func.date(Sale.completed_at) >= start,
                    func.date(Sale.completed_at) <= end)
            .one()
        )

    def sale_rows(self, start: date, end: date):
        from apoza.domain.enums import SaleStatus
        return (
            self.db.query(Sale)
            .options(joinedload(Sale.payment), joinedload(Sale.sold_by))
            .filter(
                Sale.status == SaleStatus.COMPLETED,
                func.date(Sale.completed_at) >= start,
                func.date(Sale.completed_at) <= end,
            )
            .order_by(Sale.completed_at.desc())
            .all()
        )
