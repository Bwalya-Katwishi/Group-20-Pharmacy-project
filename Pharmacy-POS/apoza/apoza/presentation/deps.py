from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from apoza.domain.rules import AuthorisationPolicy
from apoza.persistence.database import get_db
from apoza.persistence.tables import User


def current_user(request: Request, db: Session = Depends(get_db)) -> User | None:
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return db.get(User, int(user_id))


def login_required(user: User | None = Depends(current_user)) -> User:
    if user is None or not user.is_active:
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    return user


def admin_required(user: User = Depends(login_required)) -> User:
    if not AuthorisationPolicy.can_administer(user.role):
        raise HTTPException(status_code=303, headers={"Location": "/pos"})
    return user


def pharmacist_required(user: User = Depends(login_required)) -> User:
    if not AuthorisationPolicy.can_sell(user.role):
        raise HTTPException(status_code=303, headers={"Location": "/admin"})
    return user


def flash(request: Request, message: str, kind: str = "ok") -> None:
    request.session["flash"] = {"message": message, "kind": kind}


def pop_flash(request: Request) -> dict | None:
    return request.session.pop("flash", None)
