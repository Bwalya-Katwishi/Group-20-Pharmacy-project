from datetime import date, timedelta
from decimal import Decimal

from apoza.domain.enums import Role
from apoza.domain.rules import (
    AuthorisationPolicy,
    PaymentExpert,
    SaleExpert,
    SalesLineExpert,
    StockBatchExpert,
)
from apoza.security.passwords import PasswordHasher


def test_ut04_expired_batch_not_sellable():
    yesterday = date.today() - timedelta(days=1)
    assert StockBatchExpert.is_sellable(yesterday, 10, 1) is False


def test_ut05_zero_quantity_not_sellable():
    future = date.today() + timedelta(days=10)
    assert StockBatchExpert.is_sellable(future, 0, 1) is False


def test_ut06_line_total():
    assert SalesLineExpert.line_total(2, "12.00") == Decimal("24.00")


def test_sale_total():
    assert SaleExpert.total([Decimal("24.00"), Decimal("45.00")]) == Decimal("69.00")


def test_ut11_short_cash_rejected():
    ok, _ = PaymentExpert.is_acceptable("CASH", "10.00", "69.00")
    assert ok is False


def test_cash_change():
    assert PaymentExpert.change_due("CASH", "100.00", "69.00") == Decimal("31.00")


def test_ut03_pharmacist_cannot_administer():
    assert AuthorisationPolicy.can_administer(Role.PHARMACIST) is False
    assert AuthorisationPolicy.can_sell(Role.PHARMACIST) is True
    assert AuthorisationPolicy.is_known_role("CASHIER") is False


def test_ut01_ut02_password_hash():
    digest, salt = PasswordHasher.hash("secret-pass")
    assert digest != "secret-pass"
    assert PasswordHasher.verify("secret-pass", digest, salt) is True
    assert PasswordHasher.verify("wrong", digest, salt) is False
