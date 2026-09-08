from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT / ".env", extra="ignore")

    app_name: str = "PharmaPoint"
    secret_key: str = "change-this-to-a-long-random-string-before-production"
    database_url: str = f"sqlite:///{(DATA_DIR / 'pharmacy.db').as_posix()}"
    session_idle_minutes: int = 30
    host: str = "0.0.0.0"
    port: int = 8000
    seed_on_start: bool = True
    admin_username: str = "admin"
    admin_password: str = "Admin@Change1"
    pharmacist_username: str = "pharmacist"
    pharmacist_password: str = "Rx@Change1"
    pharmacy_name: str = "Demo Pharmacy"
    pharmacy_address: str = "Plot 1, Main Street, Lusaka"
    pharmacy_phone: str = "+260 211 000 000"
    currency_code: str = "ZMW"


settings = Settings()
