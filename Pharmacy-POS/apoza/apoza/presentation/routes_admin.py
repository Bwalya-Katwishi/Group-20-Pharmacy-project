from datetime import date

from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from apoza.application.auth_service import UserService
from apoza.application.errors import AppError, AuthError, ForbiddenError
from apoza.application.inventory_service import (
    InventoryService,
    MedicineService,
    ReportService,
    SettingsService,
    SupplierService,
)
from apoza.persistence.database import get_db
from apoza.persistence.tables import Medicine, MedicineCategory, User
from apoza.presentation.deps import admin_required, flash, pop_flash

router = APIRouter()


def _ctx(request: Request, db: Session, user: User, extra=None):
    settings = SettingsService(db).get()
    inv = InventoryService(db)
    data = {
        "request": request,
        "user": user,
        "settings": settings,
        "flash": pop_flash(request),
        "nav": "dashboard",
        "role_label": "Administrator",
        "low_stock": inv.low_stock(),
        "near_expiry": inv.near_expiry(),
        "expired": inv.expired(),
        "today": date.today(),
    }
    if extra:
        data.update(extra)
    return data


@router.get("/admin")
def dashboard(request: Request, db: Session = Depends(get_db),
              user: User = Depends(admin_required)):
    today = date.today()
    total, count = ReportService(db).sales_between(today, today)
    return request.app.state.templates.TemplateResponse(
        "admin_dashboard.html",
        _ctx(request, db, user, {
            "today_total": total or 0,
            "today_count": count or 0,
            "nav": "dashboard",
        }),
    )


@router.get("/admin/medicines")
def medicines(request: Request, db: Session = Depends(get_db),
              user: User = Depends(admin_required)):
    rows = MedicineService(db).list_all()
    cats = db.query(MedicineCategory).order_by(MedicineCategory.name).all()
    return request.app.state.templates.TemplateResponse(
        "medicines.html",
        _ctx(request, db, user, {"rows": rows, "categories": cats, "edit": None, "nav": "medicines"}),
    )


@router.get("/admin/medicines/{medicine_id}")
def edit_medicine(medicine_id: int, request: Request, db: Session = Depends(get_db),
                  user: User = Depends(admin_required)):
    rows = MedicineService(db).list_all()
    cats = db.query(MedicineCategory).order_by(MedicineCategory.name).all()
    edit = db.get(Medicine, medicine_id)
    return request.app.state.templates.TemplateResponse(
        "medicines.html",
        _ctx(request, db, user, {"rows": rows, "categories": cats, "edit": edit, "nav": "medicines"}),
    )


@router.post("/admin/medicines")
def save_medicine(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(admin_required),
    medicine_id: str = Form(""),
    product_code: str = Form(...),
    name: str = Form(...),
    generic_name: str = Form(""),
    strength: str = Form(""),
    form: str = Form(""),
    category_id: str = Form(""),
    unit_price: str = Form(...),
    reorder_level: int = Form(10),
    requires_prescription: str = Form(""),
    is_active: str = Form("on"),
):
    try:
        MedicineService(db).save(
            medicine_id=int(medicine_id) if medicine_id else None,
            product_code=product_code,
            name=name,
            generic_name=generic_name,
            strength=strength,
            form=form,
            category_id=category_id or None,
            unit_price=unit_price,
            reorder_level=reorder_level,
            requires_prescription=requires_prescription in ("on", "true", "1", "Yes"),
            is_active=is_active in ("on", "true", "1", "Yes"),
        )
        flash(request, "Medicine saved.")
    except AppError as exc:
        flash(request, exc.message, "err")
    return RedirectResponse("/admin/medicines", status_code=303)


@router.get("/admin/inventory")
def inventory(request: Request, db: Session = Depends(get_db),
              user: User = Depends(admin_required)):
    return request.app.state.templates.TemplateResponse(
        "inventory.html",
        _ctx(request, db, user, {"batches": InventoryService(db).batches(), "nav": "inventory"}),
    )


@router.get("/admin/inventory/receive")
def receive_form(request: Request, db: Session = Depends(get_db),
                 user: User = Depends(admin_required)):
    return request.app.state.templates.TemplateResponse(
        "receive.html",
        _ctx(request, db, user, {
            "suppliers": SupplierService(db).list_all(active_only=True),
            "medicines": MedicineService(db).list_all(include_inactive=False),
            "nav": "inventory",
        }),
    )


@router.post("/admin/inventory/receive")
def receive(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(admin_required),
    supplier_id: int = Form(...),
    reference_note: str = Form(""),
    medicine_id: int = Form(...),
    batch_number: str = Form(...),
    expiry_date: str = Form(...),
    quantity: int = Form(...),
    unit_cost: str = Form(""),
):
    try:
        InventoryService(db).receive_stock(user, supplier_id, reference_note, [{
            "medicine_id": medicine_id,
            "batch_number": batch_number,
            "expiry_date": expiry_date,
            "quantity": quantity,
            "unit_cost": unit_cost or None,
        }])
        flash(request, "Stock received.")
        return RedirectResponse("/admin/inventory", status_code=303)
    except AppError as exc:
        flash(request, exc.message, "err")
        return RedirectResponse("/admin/inventory/receive", status_code=303)


@router.get("/admin/inventory/adjust")
def adjust_form(request: Request, db: Session = Depends(get_db),
                user: User = Depends(admin_required)):
    return request.app.state.templates.TemplateResponse(
        "adjust.html",
        _ctx(request, db, user, {"batches": InventoryService(db).batches(), "nav": "inventory"}),
    )


@router.post("/admin/inventory/adjust")
def adjust(request: Request, db: Session = Depends(get_db), user: User = Depends(admin_required),
           batch_id: int = Form(...), quantity_delta: int = Form(...),
           reason: str = Form(...), note: str = Form("")):
    try:
        InventoryService(db).adjust_stock(user, batch_id, quantity_delta, reason, note)
        flash(request, "Stock adjusted.")
        return RedirectResponse("/admin/inventory", status_code=303)
    except AppError as exc:
        flash(request, exc.message, "err")
        return RedirectResponse("/admin/inventory/adjust", status_code=303)


@router.get("/admin/users")
def users(request: Request, db: Session = Depends(get_db),
          user: User = Depends(admin_required)):
    return request.app.state.templates.TemplateResponse(
        "users.html",
        _ctx(request, db, user, {"rows": UserService(db).list_users(), "nav": "users"}),
    )


@router.post("/admin/users")
def save_user(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(admin_required),
    user_id: str = Form(""),
    username: str = Form(""),
    full_name: str = Form(...),
    role: str = Form(...),
    password: str = Form(""),
    is_active: str = Form("on"),
):
    svc = UserService(db)
    try:
        if user_id:
            svc.update(user, int(user_id), full_name, role, is_active in ("on", "true", "1"),
                       password or None)
            flash(request, "User updated.")
        else:
            if not username:
                raise AuthError("Username is required for a new account.")
            svc.create(user, username, full_name, role, password)
            flash(request, "User created.")
    except (AppError, AuthError, ForbiddenError) as exc:
        flash(request, exc.message, "err")
    return RedirectResponse("/admin/users", status_code=303)


@router.get("/admin/suppliers")
def suppliers(request: Request, db: Session = Depends(get_db),
              user: User = Depends(admin_required)):
    return request.app.state.templates.TemplateResponse(
        "suppliers.html",
        _ctx(request, db, user, {"rows": SupplierService(db).list_all(), "nav": "suppliers"}),
    )


@router.post("/admin/suppliers")
def save_supplier(request: Request, db: Session = Depends(get_db),
                  user: User = Depends(admin_required),
                  supplier_id: str = Form(""), name: str = Form(...),
                  phone: str = Form(""), address: str = Form(""),
                  is_active: str = Form("on")):
    try:
        SupplierService(db).save(int(supplier_id) if supplier_id else None, name, phone, address,
                                 is_active in ("on", "true", "1"))
        flash(request, "Supplier saved.")
    except AppError as exc:
        flash(request, exc.message, "err")
    return RedirectResponse("/admin/suppliers", status_code=303)


@router.get("/admin/reports")
def reports(request: Request, start: str = "", end: str = "", kind: str = "sales",
            db: Session = Depends(get_db), user: User = Depends(admin_required)):
    today = date.today()
    start_d = date.fromisoformat(start) if start else today
    end_d = date.fromisoformat(end) if end else today
    inv = InventoryService(db)
    rows = ReportService(db).sale_rows(start_d, end_d) if kind == "sales" else []
    total, count = ReportService(db).sales_between(start_d, end_d)
    return request.app.state.templates.TemplateResponse(
        "reports.html",
        _ctx(request, db, user, {
            "nav": "reports",
            "kind": kind,
            "start": start_d,
            "end": end_d,
            "rows": rows,
            "total": total or 0,
            "count": count or 0,
            "low_stock": inv.low_stock(),
            "near_expiry": inv.near_expiry(),
        }),
    )


@router.get("/admin/settings")
def settings_form(request: Request, db: Session = Depends(get_db),
                  user: User = Depends(admin_required)):
    return request.app.state.templates.TemplateResponse(
        "settings.html", _ctx(request, db, user, {"nav": "settings"}),
    )


@router.post("/admin/settings")
def save_settings(request: Request, db: Session = Depends(get_db),
                  user: User = Depends(admin_required),
                  name: str = Form(...), address: str = Form(""), phone: str = Form(""),
                  receipt_footer: str = Form(""), near_expiry_days: int = Form(90),
                  currency_code: str = Form("ZMW")):
    try:
        SettingsService(db).save(name, address, phone, receipt_footer, near_expiry_days, currency_code)
        flash(request, "Pharmacy settings saved. New receipts will use them.")
    except AppError as exc:
        flash(request, exc.message, "err")
    return RedirectResponse("/admin/settings", status_code=303)
