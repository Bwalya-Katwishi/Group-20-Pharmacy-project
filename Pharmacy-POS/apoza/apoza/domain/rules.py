"""Information Experts and payment rules (Larman / GRASP)."""

from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from apoza.domain.enums import Role, SaleStatus

MONEY = Decimal("0.01")
ROLES = (Role.ADMINISTRATOR, Role.PHARMACIST)
PAYMENT_METHODS = ("CASH", "CARD", "MOBILE_MONEY")
ADJUST_REASONS = ("DAMAGE", "EXPIRY", "RECOUNT", "RECALL")


def money(value) -> Decimal:
    return Decimal(str(value)).quantize(MONEY, rounding=ROUND_HALF_UP)


class StockBatchExpert:
    """GRASP Information Expert: a batch knows if it may be sold."""

    @staticmethod
    def is_sellable(expiry_date: date, quantity_on_hand: int, qty: int, on_date: date | None = None) -> bool:
        on_date = on_date or date.today()
        if qty <= 0:
            return False
        if quantity_on_hand < qty:
            return False
        if expiry_date < on_date:
            return False
        return True


class SalesLineExpert:
    @staticmethod
    def line_total(quantity: int, unit_price) -> Decimal:
        return money(Decimal(quantity) * money(unit_price))


class SaleExpert:
    @staticmethod
    def total(line_totals) -> Decimal:
        return money(sum((money(x) for x in line_totals), Decimal("0.00")))

    @staticmethod
    def requires_prescription(any_rx_line: bool, has_prescription: bool) -> bool:
        return (not any_rx_line) or has_prescription


class PaymentExpert:
    """Protected Variations: each method records differently, same acceptance rule."""

    @staticmethod
    def is_acceptable(method: str, amount_tendered, total) -> tuple[bool, str]:
        method = (method or "").upper()
        if method not in PAYMENT_METHODS:
            return False, "Payment method must be cash, card, or mobile money."
        tendered = money(amount_tendered)
        due = money(total)
        if tendered <= 0:
            return False, "Amount tendered must be greater than zero."
        if method == "CASH" and tendered < due:
            return False, f"Cash tendered is short by {due - tendered}."
        return True, ""

    @staticmethod
    def change_due(method: str, amount_tendered, total) -> Decimal:
        if (method or "").upper() != "CASH":
            return money(0)
        return money(max(money(amount_tendered) - money(total), Decimal("0")))


class AuthorisationPolicy:
    """Exactly two roles. No Cashier, Manager, or Inventory Clerk."""

    ADMIN = Role.ADMINISTRATOR
    PHARMACIST = Role.PHARMACIST

    @staticmethod
    def can_administer(role: str) -> bool:
        return role == Role.ADMINISTRATOR

    @staticmethod
    def can_sell(role: str) -> bool:
        return role == Role.PHARMACIST

    @staticmethod
    def is_known_role(role: str) -> bool:
        return role in ROLES
