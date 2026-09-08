"""SQLAlchemy tables — column names match the approved logical schema."""

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apoza.domain.enums import Role, SaleStatus
from apoza.persistence.database import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    password_salt: Mapped[str] = mapped_column(String(64), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class PharmacySettings(Base):
    __tablename__ = "pharmacy_settings"

    pharmacy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(40), nullable=True)
    receipt_footer: Mapped[str | None] = mapped_column(String(255), nullable=True)
    near_expiry_days: Mapped[int] = mapped_column(Integer, nullable=False, default=90)
    currency_code: Mapped[str] = mapped_column(String(3), nullable=False, default="ZMW")


class MedicineCategory(Base):
    __tablename__ = "medicine_categories"

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    medicines = relationship("Medicine", back_populates="category")


class Medicine(Base):
    __tablename__ = "medicines"

    medicine_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_code: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    generic_name: Mapped[str | None] = mapped_column(String(160), nullable=True)
    strength: Mapped[str | None] = mapped_column(String(40), nullable=True)
    form: Mapped[str | None] = mapped_column(String(40), nullable=True)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("medicine_categories.category_id"))
    requires_prescription: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    reorder_level: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    category = relationship("MedicineCategory", back_populates="medicines")
    batches = relationship("StockBatch", back_populates="medicine")


class Supplier(Base):
    __tablename__ = "suppliers"

    supplier_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(40), nullable=True)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class StockBatch(Base):
    __tablename__ = "stock_batches"

    batch_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    medicine_id: Mapped[int] = mapped_column(ForeignKey("medicines.medicine_id"), nullable=False)
    batch_number: Mapped[str] = mapped_column(String(60), nullable=False)
    expiry_date: Mapped[date] = mapped_column(Date, nullable=False)
    quantity_on_hand: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    unit_cost: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    received_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    medicine = relationship("Medicine", back_populates="batches")


class StockReceipt(Base):
    __tablename__ = "stock_receipts"

    receipt_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.supplier_id"), nullable=False)
    received_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    received_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    reference_note: Mapped[str | None] = mapped_column(String(120), nullable=True)
    lines = relationship("StockReceiptLine", back_populates="receipt")
    supplier = relationship("Supplier")
    received_by = relationship("User")


class StockReceiptLine(Base):
    __tablename__ = "stock_receipt_lines"

    receipt_line_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    receipt_id: Mapped[int] = mapped_column(ForeignKey("stock_receipts.receipt_id"), nullable=False)
    batch_id: Mapped[int] = mapped_column(ForeignKey("stock_batches.batch_id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    receipt = relationship("StockReceipt", back_populates="lines")
    batch = relationship("StockBatch")


class StockAdjustment(Base):
    __tablename__ = "stock_adjustments"

    adjustment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    batch_id: Mapped[int] = mapped_column(ForeignKey("stock_batches.batch_id"), nullable=False)
    adjusted_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    quantity_delta: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(String(40), nullable=False)
    note: Mapped[str | None] = mapped_column(String(255), nullable=True)
    adjusted_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    batch = relationship("StockBatch")
    adjusted_by = relationship("User")


class Customer(Base):
    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(160), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(40), nullable=True)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)


class Prescription(Base):
    __tablename__ = "prescriptions"

    prescription_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.customer_id"), nullable=False)
    reference_no: Mapped[str] = mapped_column(String(60), nullable=False)
    prescriber_name: Mapped[str | None] = mapped_column(String(160), nullable=True)
    issued_on: Mapped[date | None] = mapped_column(Date, nullable=True)
    recorded_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    customer = relationship("Customer")
    items = relationship("PrescriptionItem", back_populates="prescription")


class PrescriptionItem(Base):
    __tablename__ = "prescription_items"

    prescription_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    prescription_id: Mapped[int] = mapped_column(ForeignKey("prescriptions.prescription_id"), nullable=False)
    medicine_id: Mapped[int] = mapped_column(ForeignKey("medicines.medicine_id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    prescription = relationship("Prescription", back_populates="items")
    medicine = relationship("Medicine")


class Sale(Base):
    __tablename__ = "sales"

    sale_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sold_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    customer_id: Mapped[int | None] = mapped_column(ForeignKey("customers.customer_id"), nullable=True)
    prescription_id: Mapped[int | None] = mapped_column(ForeignKey("prescriptions.prescription_id"), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=SaleStatus.IN_PROGRESS)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    void_reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=Decimal("0.00"))
    total: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=Decimal("0.00"))
    items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")
    payment = relationship("Payment", back_populates="sale", uselist=False)
    sold_by = relationship("User")
    customer = relationship("Customer")
    prescription = relationship("Prescription")


class SaleItem(Base):
    __tablename__ = "sale_items"

    sale_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sale_id: Mapped[int] = mapped_column(ForeignKey("sales.sale_id"), nullable=False)
    medicine_id: Mapped[int] = mapped_column(ForeignKey("medicines.medicine_id"), nullable=False)
    batch_id: Mapped[int] = mapped_column(ForeignKey("stock_batches.batch_id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    line_total: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    sale = relationship("Sale", back_populates="items")
    medicine = relationship("Medicine")
    batch = relationship("StockBatch")


class Payment(Base):
    __tablename__ = "payments"

    payment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sale_id: Mapped[int] = mapped_column(ForeignKey("sales.sale_id"), unique=True, nullable=False)
    method: Mapped[str] = mapped_column(String(20), nullable=False)
    amount_tendered: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    change_due: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=Decimal("0.00"))
    external_reference: Mapped[str | None] = mapped_column(String(80), nullable=True)
    paid_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    sale = relationship("Sale", back_populates="payment")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    audit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.user_id"), nullable=True)
    action: Mapped[str] = mapped_column(String(40), nullable=False)
    entity_name: Mapped[str | None] = mapped_column(String(40), nullable=True)
    entity_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    details: Mapped[str | None] = mapped_column(String(500), nullable=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    user = relationship("User")


# Keep Role / SaleStatus importable from tables for older imports
__all__ = [
    "User",
    "PharmacySettings",
    "MedicineCategory",
    "Medicine",
    "Supplier",
    "StockBatch",
    "StockReceipt",
    "StockReceiptLine",
    "StockAdjustment",
    "Customer",
    "Prescription",
    "PrescriptionItem",
    "Sale",
    "SaleItem",
    "Payment",
    "AuditLog",
    "Role",
    "SaleStatus",
]
