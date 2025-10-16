VALID_PAN = "4242424242424242"
INVALID_PAN = "4242424242424241"

def test_card_crud_and_luhn(client):
    # Crear cliente
    cust = {"name": "Manuel Sanchez",
            "email": "manuel@gmail.com",
            "phone": "7551010765"
            }
    r = client.post("/customers", json=cust)
    assert r.status_code in (200, 201)
    customer_id = r.json().get("id_customer")

    # Crear tarjeta válida
    card_payload = {
        "customer_id": customer_id,
        "card_number": VALID_PAN,
        "expiration_month": 12,
        "expiration_year": 2029
    }
    r = client.post("/cards", json=card_payload)
    assert r.status_code in (200, 201)
    card_id = r.json().get("id_card")

    # Crear tarjeta inválida (Luhn fail)
    bad_payload = {
        "customer_id": customer_id,
        "card_number": INVALID_PAN,
        "expiration_month": 12,
        "expiration_year": 2099
    }
    r = client.post("/cards", json=bad_payload)
    assert r.status_code == 400

    # Leer tarjeta
    r = client.get(f"/cards/{card_id}")
    assert r.status_code == 200
    assert "last_4" in r.json()

    # Actualizar solo expiración
    update = {"expiration_month": 1, "expiration_year": 2026}
    r = client.put(f"/cards/{card_id}", json=update)
    assert r.status_code == 200
    assert "expiration_date" in r.json()

    # Eliminar tarjeta
    r = client.delete(f"/cards/{card_id}")
    assert r.status_code in (200, 204)

    # Verificar eliminado
    r = client.get(f"/cards/{card_id}")
    assert r.status_code == 404
