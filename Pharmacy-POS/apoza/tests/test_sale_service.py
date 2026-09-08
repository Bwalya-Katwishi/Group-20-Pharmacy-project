from datetime import date, timedelta
from decimal import Decimal

import pytest

from apoza.application.auth_service import AuthenticationService, UserService
from apoza.application.errors import AppError, AuthError, ForbiddenError
from apoza.application.sale_service import SaleService
from apoza.domain.enums import Role, SaleStatus
from apoza.persistence.tables import Medicine, StockBatch, User


def _admin(db):
    return db.query(User).filter(User.role == Role.ADMINISTRATOR).one()


def _pharmacist(db):
    return db.query(User).filter(User.role == Role.PHARMACIST).one()


def test_ut01_valid_login(db):
    user = AuthenticationService(db).authenticate("pharmacist", "Rx@Change1")
    assert user.role == Role.PHARMACIST


def test_ut02_wrong_password(db):
    with pytest.raises(AuthError):
        AuthenticationService(db).authenticate("pharmacist", "nope")


def test_ut03_pharmacist_cannot_create_user(db):
    pharm = _pharmacist(db)
    with pytest.raises(ForbiddenError):
        AuthenticationService(db).require_admin(pharm)


def test_enter_item_and_total(db):
    svc = SaleService(db)
    sale = svc.make_new_sale(_pharmacist(db))
    svc.add_by_code(sale, "PAR-500", 2)
    db.refresh(sale)
    assert sale.total == Decimal("24.00")


def test_add_by_code_not_found(db):
    svc = SaleService(db)
    sale = svc.make_new_sale(_pharmacist(db))
    with pytest.raises(AppError, match="not found"):
        svc.add_by_code(sale, "NO-SUCH-CODE", 1)


def test_ut04_expired_refused(db):
    svc = SaleService(db)
    sale = svc.make_new_sale(_pharmacist(db))
    med = db.query(Medicine).filter(Medicine.product_code == "COUGH-100").one()
    expired = [b for b in med.batches if b.expiry_date < date.today()][0]
    # empty the good batch so only expired remains
    for b in med.batches:
        if b.batch_id != expired.batch_id:
            b.quantity_on_hand = 0
    db.commit()
    with pytest.raises(AppError):
        svc.enter_item(sale, med.medicine_id, 1)


def test_ut09_end_sale_requires_prescription(db):
    svc = SaleService(db)
    sale = svc.make_new_sale(_pharmacist(db))
    med = db.query(Medicine).filter(Medicine.product_code == "AMOX-500").one()
    svc.enter_item(sale, med.medicine_id, 1)
    with pytest.raises(AppError, match="prescription"):
        svc.end_sale_guard(sale)


def test_complete_sale_decrements_stock(db):
    svc = SaleService(db)
    user = _pharmacist(db)
    sale = svc.make_new_sale(user)
    med = db.query(Medicine).filter(Medicine.product_code == "PAR-500").one()
    before = sum(b.quantity_on_hand for b in med.batches)
    svc.enter_item(sale, med.medicine_id, 2)
    svc.complete_sale(sale, user, "CASH", "24.00", None)
    db.refresh(med)
    after = sum(b.quantity_on_hand for b in db.query(StockBatch).filter(StockBatch.medicine_id == med.medicine_id))
    assert after == before - 2
    assert sale.status == SaleStatus.COMPLETED


def test_ut10_void_restores_stock(db):
    svc = SaleService(db)
    user = _pharmacist(db)
    sale = svc.make_new_sale(user)
    med = db.query(Medicine).filter(Medicine.product_code == "PAR-500").one()
    before = sum(b.quantity_on_hand for b in med.batches)
    svc.enter_item(sale, med.medicine_id, 1)
    svc.complete_sale(sale, user, "CASH", "12.00", None)
    svc.void_sale(sale.sale_id, user, "Wrong item")
    after = sum(b.quantity_on_hand for b in db.query(StockBatch).filter(StockBatch.medicine_id == med.medicine_id))
    assert after == before
    assert svc.get_sale(sale.sale_id).status == SaleStatus.VOIDED


def test_short_cash_does_not_complete(db):
    svc = SaleService(db)
    user = _pharmacist(db)
    sale = svc.make_new_sale(user)
    med = db.query(Medicine).filter(Medicine.product_code == "PAR-500").one()
    svc.enter_item(sale, med.medicine_id, 1)
    with pytest.raises(AppError):
        svc.complete_sale(sale, user, "CASH", "1.00", None)
    db.refresh(sale)
    assert sale.status == SaleStatus.IN_PROGRESS
