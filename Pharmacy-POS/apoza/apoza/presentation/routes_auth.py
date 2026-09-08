from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from apoza.application.inventory_service import SettingsService
from apoza.application.auth_service import AuthenticationService
from apoza.application.errors import AuthError
from apoza.persistence.database import get_db
from apoza.presentation.deps import current_user, flash, pop_flash

router = APIRouter()


@router.get("/login")
def login_form(request: Request, db: Session = Depends(get_db), user=Depends(current_user)):
    if user:
        return RedirectResponse("/", status_code=303)
    settings = SettingsService(db).get()
    return request.app.state.templates.TemplateResponse(
        "login.html",
        {"request": request, "flash": pop_flash(request), "error": None, "settings": settings},
    )


@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...),
          db: Session = Depends(get_db)):
    settings = SettingsService(db).get()
    try:
        user = AuthenticationService(db).authenticate(username, password)
    except AuthError as exc:
        return request.app.state.templates.TemplateResponse(
            "login.html",
            {"request": request, "flash": None, "error": exc.message, "settings": settings},
            status_code=401,
        )
    request.session["user_id"] = user.user_id
    request.session["role"] = user.role
    request.session["full_name"] = user.full_name
    dest = "/admin" if user.role == "ADMINISTRATOR" else "/pos"
    return RedirectResponse(dest, status_code=303)


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)
