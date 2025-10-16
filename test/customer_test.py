def test_customer_crud(client):
    # Crear
    payload = {
        "name": "Manuel Oliver",
        "email": "manuel@example.com",
        "phone": "7555583506"
    }
    r = client.post("/customers", json=payload)
    assert r.status_code in (200, 201)
    data = r.json()
    customer_id = data.get("id_customer")

    # Leer
    r = client.get(f"/customers/{customer_id}")
    assert r.status_code == 200
    assert r.json().get("email") == "manuel@example.com"

    # Actualizar
    update = {
        "name": "Manuel Sanchez",
        "email": "manuel@gmail.com",
        "phone": "7551010765"
    }
    r = client.put(f"/customers/{customer_id}", json=update)
    assert r.status_code == 200
    assert r.json().get("name") == "Manuel Sanchez"

    # Eliminar
    r = client.delete(f"/customers/{customer_id}")
    assert r.status_code in (200, 204)

    # Verificar eliminado
    r = client.get(f"/customers/{customer_id}")
    assert r.status_code == 404
