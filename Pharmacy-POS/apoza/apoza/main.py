from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from apoza import PRODUCT_NAME, PRODUCT_TAGLINE, __version__
from apoza.config import settings
from apoza.persistence.database import SessionLocal, engine
from apoza.persistence.seed import seed_if_empty
from apoza.persistence.tables import Base
from apoza.presentation.routes_admin import router as admin_router
from apoza.presentation.routes_auth import router as auth_router
from apoza.presentation.routes_pos import router as pos_router

TEMPLATES = Path(__file__).resolve().parent / "presentation" / "templates"
STATIC = Path(__file__).resolve().parent / "presentation" / "static"


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    if settings.seed_on_start:
        db = SessionLocal()
        try:
            seed_if_empty(db)
        finally:
            db.close()
    yield


def create_app() -> FastAPI:
    app = FastAPI(title=PRODUCT_NAME, version=__version__, docs_url=None, redoc_url=None, lifespan=lifespan)
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.secret_key,
        session_cookie="pharmapoint_session",
        max_age=settings.session_idle_minutes * 60,
        same_site="lax",
        https_only=False,
    )
    app.mount("/static", StaticFiles(directory=STATIC), name="static")
    templates = Jinja2Templates(directory=str(TEMPLATES))
    templates.env.globals["product"] = PRODUCT_NAME
    templates.env.globals["product_tagline"] = PRODUCT_TAGLINE
    app.state.templates = templates

    @app.get("/health")
    def health():
        return {"product": PRODUCT_NAME, "version": __version__, "status": "ok"}

    @app.get("/")
    def home(request: Request):
        role = request.session.get("role")
        if role == "ADMINISTRATOR":
            return RedirectResponse("/admin", status_code=303)
        if role == "PHARMACIST":
            return RedirectResponse("/pos", status_code=303)
        return RedirectResponse("/login", status_code=303)

    app.include_router(auth_router)
    app.include_router(pos_router)
    app.include_router(admin_router)
    return app


app = create_app()
