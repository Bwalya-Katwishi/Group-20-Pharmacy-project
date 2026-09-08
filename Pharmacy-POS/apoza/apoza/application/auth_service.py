from datetime import datetime

from sqlalchemy.orm import Session

from apoza.application.audit import AuditLogger
from apoza.application.errors import AuthError, ForbiddenError
from apoza.domain.enums import Role
from apoza.domain.rules import AuthorisationPolicy
from apoza.persistence.tables import User
from apoza.security.passwords import PasswordHasher


class AuthenticationService:
    def __init__(self, db: Session):
        self.db = db
        self.audit = AuditLogger(db)

    def authenticate(self, username: str, password: str) -> User:
        user = self.db.query(User).filter(User.username == username.strip()).one_or_none()
        if user is None or not user.is_active:
            self.audit.write("LOGIN_FAIL", details=f"username={username.strip()[:40]}")
            self.db.commit()
            raise AuthError("Username or password is not correct.")
        if not PasswordHasher.verify(password, user.password_hash, user.password_salt):
            self.audit.write("LOGIN_FAIL", user_id=user.user_id, details="bad password")
            self.db.commit()
            raise AuthError("Username or password is not correct.")
        user.last_login_at = datetime.utcnow()
        self.audit.write("LOGIN", user_id=user.user_id, entity_name="users", entity_id=user.user_id)
        self.db.commit()
        return user

    def require(self, user: User | None) -> User:
        if user is None or not user.is_active:
            raise AuthError("Please sign in.")
        return user

    def require_admin(self, user: User | None) -> User:
        user = self.require(user)
        if not AuthorisationPolicy.can_administer(user.role):
            raise ForbiddenError("This action is for the Administrator only.")
        return user

    def require_pharmacist(self, user: User | None) -> User:
        user = self.require(user)
        if not AuthorisationPolicy.can_sell(user.role):
            raise ForbiddenError("This action is for the Pharmacist/Cashier only.")
        return user


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.audit = AuditLogger(db)

    def list_users(self) -> list[User]:
        return self.db.query(User).order_by(User.full_name).all()

    def create(self, actor: User, username: str, full_name: str, role: str, password: str) -> User:
        if not AuthorisationPolicy.is_known_role(role):
            raise ForbiddenError("Only Administrator and Pharmacist/Cashier roles exist.")
        if self.db.query(User).filter(User.username == username.strip()).one_or_none():
            raise AuthError("That username is already in use.")
        if len(password) < 8:
            raise AuthError("Password must be at least 8 characters.")
        digest, salt = PasswordHasher.hash(password)
        user = User(
            username=username.strip(),
            full_name=full_name.strip(),
            role=role,
            password_hash=digest,
            password_salt=salt,
            is_active=True,
        )
        self.db.add(user)
        self.db.flush()
        self.audit.write("USER_ADMIN", actor.user_id, "users", user.user_id, f"created {user.username} as {role}")
        self.db.commit()
        return user

    def update(self, actor: User, user_id: int, full_name: str, role: str, is_active: bool,
               new_password: str | None = None) -> User:
        if not AuthorisationPolicy.is_known_role(role):
            raise ForbiddenError("Only Administrator and Pharmacist/Cashier roles exist.")
        user = self.db.get(User, user_id)
        if not user:
            raise AuthError("User not found.")
        if user.user_id == actor.user_id and not is_active:
            raise AuthError("You cannot deactivate your own account.")
        if role == Role.ADMINISTRATOR and not is_active:
            others = self.db.query(User).filter(
                User.role == Role.ADMINISTRATOR, User.is_active.is_(True), User.user_id != user.user_id
            ).count()
            if others == 0:
                raise AuthError("At least one active Administrator must remain.")
        user.full_name = full_name.strip()
        user.role = role
        user.is_active = is_active
        if new_password:
            if len(new_password) < 8:
                raise AuthError("Password must be at least 8 characters.")
            user.password_hash, user.password_salt = PasswordHasher.hash(new_password)
        self.audit.write("USER_ADMIN", actor.user_id, "users", user.user_id, f"updated {user.username}")
        self.db.commit()
        return user
