VALID_PAN = "4242424242424242"      # Aprobado
INVALID_PAN = "4111111111111234"    # Rechazado (por regla o patrón)

def test_charge_flow(client):
    # Crear cliente
    r = client.post("/customers", json={
        "name": "Manuel Oliver",
        "email": "manuel@example.com",
        "phone": "7555583506"
    })
    assert r.status_code in (200, 201)
    customer_id = r.json().get("id_customer")

    # Crear tarjeta válida
    r = client.post("/cards", json={
        "customer_id": customer_id,
        "card_number": VALID_PAN,
        "expiration_month": 12,
        "expiration_year": 2030
    })
    card_id = r.json().get("id_card") or r.json().get("_id")

    # Crear cobro aprobado
    charge_payload = {"customer_id": customer_id, "card_id": card_id, "amount": 500.0}
    r = client.post("/charges", json=charge_payload)
    assert r.status_code in (200, 201)
    data = r.json()
    assert data["status"] == "APPROVED"
    charge_id = data.get("id_charge") or data.get("_id")


    # Cobro rechazado
    r = client.post("/charges", json={"customer_id": customer_id, "card_id": card_id, "amount": 100000})
    assert r.status_code in (200, 400)
    if r.status_code == 200:
        assert r.json()["status"] == "DECLINED"

    # Reembolsar cobro aprobado
    r = client.post(f"/charges/{charge_id}/refund")
    assert r.status_code in (200, 201)
    refunded = r.json()
    assert refunded["is_refunded"] is True

    # Historial del cliente
    r = client.get(f"/charges/customer/{customer_id}")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert any(c.get("is_refunded") for c in data)
