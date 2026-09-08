from apoza.domain.enums import Role


def test_it01_otc_sale_path(client, db):
    login = client.post("/login", data={"username": "pharmacist", "password": "Rx@Change1"}, follow_redirects=False)
    assert login.status_code == 303
    add = client.post("/pos/scan", data={"code": "PAR-500", "quantity": 2}, follow_redirects=False)
    assert add.status_code == 303
    pay = client.post(
        "/pos/pay",
        data={"method": "CASH", "amount_tendered": "30.00", "external_reference": ""},
        follow_redirects=False,
    )
    assert pay.status_code == 303
    assert "/pos/receipt/" in pay.headers["location"]


def test_it06_pharmacist_cannot_open_users(client):
    client.post("/login", data={"username": "pharmacist", "password": "Rx@Change1"})
    r = client.get("/admin/users", follow_redirects=False)
    assert r.status_code in (303, 401, 403)


def test_admin_dashboard(client):
    client.post("/login", data={"username": "admin", "password": "Admin@Change1"})
    r = client.get("/admin")
    assert r.status_code == 200
    assert "Administrator" in r.text
