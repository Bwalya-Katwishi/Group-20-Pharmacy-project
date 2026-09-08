from datetime import date, timedelta

from sqlalchemy.orm import Session

from apoza.config import settings
from apoza.domain.enums import Role
from apoza.persistence.tables import (
    Customer,
    Medicine,
    MedicineCategory,
    PharmacySettings,
    StockBatch,
    Supplier,
    User,
)
from apoza.security.passwords import PasswordHasher


def seed_if_empty(db: Session) -> None:
    if db.query(User).first():
        if not db.query(PharmacySettings).first():
            _settings(db)
            db.commit()
        return
    _settings(db)
    db.add_all([
        Customer(full_name="Walk-in"),
    ])
    db.flush()
    admin_hash, admin_salt = PasswordHasher.hash(settings.admin_password)
    rx_hash, rx_salt = PasswordHasher.hash(settings.pharmacist_password)
    db.add_all([
        User(username=settings.admin_username, full_name="System Administrator",
             role=Role.ADMINISTRATOR, password_hash=admin_hash, password_salt=admin_salt, is_active=True),
        User(username=settings.pharmacist_username, full_name="Dispensing Pharmacist",
             role=Role.PHARMACIST, password_hash=rx_hash, password_salt=rx_salt, is_active=True),
    ])
    cats = {
        "Analgesic": MedicineCategory(name="Analgesic", description="Pain and fever"),
        "Antibiotic": MedicineCategory(name="Antibiotic", description="Prescription antimicrobials"),
        "ORS": MedicineCategory(name="Rehydration", description="Oral rehydration"),
        "Cough": MedicineCategory(name="Cough and cold", description="OTC cough"),
        "Chronic": MedicineCategory(name="Chronic care", description="Long-term therapy"),
    }
    db.add_all(list(cats.values()))
    db.flush()
    meds = [
        Medicine(product_code="PAR-500", name="Paracetamol 500mg", generic_name="Paracetamol",
                 strength="500 mg", form="Tablet", category_id=cats["Analgesic"].category_id,
                 requires_prescription=False, unit_price=12.00, reorder_level=20, is_active=True),
        Medicine(product_code="PAR-SYR", name="Paracetamol syrup", generic_name="Paracetamol",
                 strength="120 mg/5ml", form="Syrup", category_id=cats["Analgesic"].category_id,
                 requires_prescription=False, unit_price=28.50, reorder_level=8, is_active=True),
        Medicine(product_code="AMOX-500", name="Amoxicillin 500mg", generic_name="Amoxicillin",
                 strength="500 mg", form="Capsule", category_id=cats["Antibiotic"].category_id,
                 requires_prescription=True, unit_price=35.00, reorder_level=15, is_active=True),
        Medicine(product_code="AMOX-250", name="Amoxicillin 250mg", generic_name="Amoxicillin",
                 strength="250 mg", form="Capsule", category_id=cats["Antibiotic"].category_id,
                 requires_prescription=True, unit_price=22.00, reorder_level=15, is_active=True),
        Medicine(product_code="COUGH-100", name="Cough syrup 100ml", generic_name="Dextromethorphan",
                 strength="100 ml", form="Syrup", category_id=cats["Cough"].category_id,
                 requires_prescription=False, unit_price=45.00, reorder_level=10, is_active=True),
        Medicine(product_code="ORS-20", name="ORS sachets", generic_name="Oral rehydration salts",
                 strength="20.5 g", form="Sachet", category_id=cats["ORS"].category_id,
                 requires_prescription=False, unit_price=8.00, reorder_level=20, is_active=True),
        Medicine(product_code="INS-R", name="Insulin regular", generic_name="Human insulin",
                 strength="100 IU/ml", form="Vial", category_id=cats["Chronic"].category_id,
                 requires_prescription=True, unit_price=180.00, reorder_level=4, is_active=True),
    ]
    db.add_all(meds)
    db.flush()
    by_code = {m.product_code: m for m in meds}
    today = date.today()
    db.add_all([
        StockBatch(medicine_id=by_code["PAR-500"].medicine_id, batch_number="B19-04",
                   expiry_date=today + timedelta(days=400), quantity_on_hand=84, unit_cost=6.00),
        StockBatch(medicine_id=by_code["PAR-SYR"].medicine_id, batch_number="P02-11",
                   expiry_date=today + timedelta(days=220), quantity_on_hand=12, unit_cost=14.00),
        StockBatch(medicine_id=by_code["AMOX-500"].medicine_id, batch_number="A11-08",
                   expiry_date=today + timedelta(days=180), quantity_on_hand=40, unit_cost=18.00),
        StockBatch(medicine_id=by_code["AMOX-250"].medicine_id, batch_number="A03-02",
                   expiry_date=today + timedelta(days=35), quantity_on_hand=16, unit_cost=11.00),
        StockBatch(medicine_id=by_code["COUGH-100"].medicine_id, batch_number="C02-11",
                   expiry_date=today + timedelta(days=300), quantity_on_hand=18, unit_cost=22.00),
        StockBatch(medicine_id=by_code["COUGH-100"].medicine_id, batch_number="C88-01",
                   expiry_date=today - timedelta(days=18), quantity_on_hand=3, unit_cost=22.00),
        StockBatch(medicine_id=by_code["ORS-20"].medicine_id, batch_number="O09-01",
                   expiry_date=today + timedelta(days=500), quantity_on_hand=8, unit_cost=3.50),
        StockBatch(medicine_id=by_code["INS-R"].medicine_id, batch_number="I11-08",
                   expiry_date=today + timedelta(days=25), quantity_on_hand=6, unit_cost=95.00),
    ])
    db.add_all([
        Supplier(name="Medical Stores Limited", phone="+260 211 250 400",
                 address="Industrial Area, Lusaka", is_active=True),
        Supplier(name="Pharmanova Zambia", phone="+260 211 290 100",
                 address="Cairo Road, Lusaka", is_active=True),
    ])
    db.commit()


def _settings(db: Session) -> None:
    db.add(PharmacySettings(
        pharmacy_id=1,
        name=settings.pharmacy_name,
        address=settings.pharmacy_address,
        phone=settings.pharmacy_phone,
        receipt_footer="Thank you for choosing us. Medicines cannot be returned once dispensed.",
        near_expiry_days=90,
        currency_code=settings.currency_code,
    ))
