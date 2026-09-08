# PharmaPoint

**PharmaPoint** is a pharmacy point-of-sale system for retail pharmacies in Zambia. It supports counter sales, batch-level expiry control, prescription capture, cash/card/mobile-money recording, receipts, voids, inventory management, reports, and a full audit trail.

Each pharmacy configures its own name, address, and staff accounts. The system is designed for a single branch or a small LAN deployment.

## Features

- Counter sales that refuse expired or short stock
- Prescription details required before dispensing controlled medicines
- Inventory receive/adjust with reasons
- Two roles: **Administrator** and **Pharmacist** (cashier/dispenser)
- Zambian Kwacha (ZMW) by default — configurable per pharmacy
- Deploy on one workstation or a small office network

Out of scope: e-commerce, NHIMA claims, live payment gateways, national e-prescription feeds.

## Quick start (Windows)

```powershell
cd Pharmacy-POS\apoza
python -m pip install -r requirements.txt
python run.py
```

Open http://127.0.0.1:8000

| Role | Username | Default password |
| --- | --- | --- |
| Administrator | `admin` | `Admin@Change1` |
| Pharmacist | `pharmacist` | `Rx@Change1` |

**Change these immediately** on any production machine (`ADMIN_PASSWORD` / `PHARMACIST_PASSWORD` in `.env`, or via Users in the Administrator screen). Then update your pharmacy name under **Settings**.

## Production setup

1. Copy `.env.example` to `.env`.
2. Set a long random `SECRET_KEY`.
3. Set new admin and pharmacist passwords.
4. Enter your pharmacy's legal name in `PHARMACY_NAME` (also editable under Settings).
5. Keep `data/pharmacy.db` on a disk that is backed up daily.
6. Run behind HTTPS if the browser is not only on localhost.
7. Do not expose port 8000 to the public internet without TLS and a firewall.

### Docker

```powershell
docker compose up -d --build
```

Data lives in the `pharmacy-data` volume.

## Architecture

- Presentation — Jinja screens (`presentation/`)
- Application — sale, authentication, inventory, and user services
- Domain — stock batch rules, payment rules, authorisation policy
- Persistence — SQLite database (see `Database-Design/` for schema documentation)
- Security — PBKDF2 password hashing with per-user salt, audit logging

Sale completion and stock decrement run in one database transaction.

## Tests

```powershell
python -m pytest -q
```

## Backup

Stop the application, copy `data/pharmacy.db` (and `-wal`/`-shm` if present) to encrypted off-site storage, then start again. Test a restore on a spare PC before you need it.

## Design documentation

Database schema and relationship diagrams are kept in the `Database-Design/` folder at the project root. These documents are the reference for the logical data model and are not modified by the application code.
