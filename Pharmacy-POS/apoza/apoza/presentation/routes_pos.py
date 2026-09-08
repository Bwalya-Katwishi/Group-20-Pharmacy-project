from datetime import date

from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from apoza.application.errors import AppError
from apoza.application.inventory_service import SettingsService
from apoza.application.sale_service import SaleService
from apoza.persistence.database import get_db
from apoza.persistence.tables import User
from apoza.presentation.deps import flash, pharmacist_required, pop_flash

router = APIRouter()


def _ctx(request: Request, db: Session, user: User, extra: dict | None = None):
    svc = SaleService(db)
    sale = svc.current_or_new(user)
    settings = SettingsService(db).get()
    data = {
        "request": request,
        "user": user,
        "sale": sale,
        "settings": settings,
        "flash": pop_flash(request),
        "nav": "sale",
        "role_label": "Pharmacist/Cashier",
        "needs_rx": svc.requires_prescription_capture(sale),
    }
    if extra:
        data.update(extra)
    return data


@router.get("/pos")
def pos(request: Request, db: Session = Depends(get_db),
        user: User = Depends(pharmacist_required)):
    return request.app.state.templates.TemplateResponse(
        "pos.html", _ctx(request, db, user, {"nav": "sale"}),
    )


@router.post("/pos/scan")
def scan_item(request: Request, code: str = Form(...), quantity: int = Form(1),
              db: Session = Depends(get_db), user: User = Depends(pharmacist_required)):
    svc = SaleService(db)
    sale = svc.current_or_new(user)
    try:
        item = svc.add_by_code(sale, code, quantity)
        med = item.medicine
        flash(request, f"Added {med.name} × {quantity}.")
    except AppError as exc:
        flash(request, exc.message, "err")
    return RedirectResponse("/pos", status_code=303)


@router.post("/pos/items/{item_id}/remove")
def remove_item(item_id: int, request: Request, db: Session = Depends(get_db),
                user: User = Depends(pharmacist_required)):
    svc = SaleService(db)
    sale = svc.current_or_new(user)
    try:
        svc.remove_line(sale, item_id)
        flash(request, "Line removed.")
    except AppError as exc:
        flash(request, exc.message, "err")
    return RedirectResponse("/pos", status_code=303)


@router.post("/pos/cancel")
def cancel(request: Request, db: Session = Depends(get_db),
           user: User = Depends(pharmacist_required)):
    svc = SaleService(db)
    sale = svc.current_or_new(user)
    try:
        svc.cancel_in_progress(sale, user)
        flash(request, "Sale cancelled. No stock was changed.")
    except AppError as exc:
        flash(request, exc.message, "err")
    return RedirectResponse("/pos", status_code=303)


@router.post("/pos/prescription")
def attach_rx(request: Request, reference_no: str = Form(...),
              prescriber_name: str = Form(""), issued_on: str = Form(""),
              db: Session = Depends(get_db), user: User = Depends(pharmacist_required)):
    svc = SaleService(db)
    sale = svc.current_or_new(user)
    issued = date.fromisoformat(issued_on) if issued_on else None
    try:
        svc.attach_prescription(sale, user, reference_no, prescriber_name, issued)
        flash(request, "Prescription recorded. You may now take payment.")
    except AppError as exc:
        flash(request, exc.message, "err")
    return RedirectResponse("/pos", status_code=303)


@router.post("/pos/pay")
def pay(request: Request, method: str = Form(...), amount_tendered: str = Form(...),
        external_reference: str = Form(""), db: Session = Depends(get_db),
        user: User = Depends(pharmacist_required)):
    svc = SaleService(db)
    sale = svc.current_or_new(user)
    try:
        svc.end_sale_guard(sale)
        completed = svc.complete_sale(sale, user, method, amount_tendered, external_reference)
        return RedirectResponse(f"/pos/receipt/{completed.sale_id}", status_code=303)
    except AppError as exc:
        flash(request, exc.message, "err")
        return RedirectResponse("/pos", status_code=303)


@router.get("/pos/receipt/{sale_id}")
def receipt(sale_id: int, request: Request, db: Session = Depends(get_db),
            user: User = Depends(pharmacist_required)):
    sale = SaleService(db).get_sale(sale_id)
    if not sale:
        flash(request, "Receipt not found.", "err")
        return RedirectResponse("/pos", status_code=303)
    settings = SettingsService(db).get()
    return request.app.state.templates.TemplateResponse(
        "receipt.html",
        {"request": request, "user": user, "sale": sale, "settings": settings,
         "flash": pop_flash(request), "nav": "sale", "role_label": "Pharmacist/Cashier"},
    )


@router.get("/pos/sales")
def todays(request: Request, db: Session = Depends(get_db),
           user: User = Depends(pharmacist_required)):
    rows = SaleService(db).todays_sales()
    return request.app.state.templates.TemplateResponse(
        "today.html", _ctx(request, db, user, {"rows": rows, "nav": "today"}),
    )


@router.get("/pos/void")
def void_form(request: Request, db: Session = Depends(get_db),
              user: User = Depends(pharmacist_required)):
    rows = SaleService(db).todays_sales()
    return request.app.state.templates.TemplateResponse(
        "void.html", _ctx(request, db, user, {"rows": rows, "nav": "void"}),
    )


@router.post("/pos/void")
def void_sale(request: Request, sale_id: int = Form(...), reason: str = Form(...),
              db: Session = Depends(get_db), user: User = Depends(pharmacist_required)):
    try:
        SaleService(db).void_sale(sale_id, user, reason)
        flash(request, "Sale voided. Stock restored if it had been completed.")
    except AppError as exc:
        flash(request, exc.message, "err")
    return RedirectResponse("/pos/void", status_code=303)
