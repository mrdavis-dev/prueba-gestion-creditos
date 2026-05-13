def test_crear_solicitud_valida(client):
    response = client.post("/solicitudes/", json={
        "cedula": "1234567890",
        "monto": 5000,
        "plazo_meses": 12
    })
    assert response.status_code == 201
    data = response.json()
    assert data["estado"] == "pendiente"
    assert data["cedula"] == "1234567890"
    assert data["monto"] == 5000


def test_monto_minimo_invalido(client):
    response = client.post("/solicitudes/", json={
        "cedula": "123",
        "monto": 499,
        "plazo_meses": 12
    })
    assert response.status_code == 422


def test_monto_maximo_invalido(client):
    response = client.post("/solicitudes/", json={
        "cedula": "123",
        "monto": 50001,
        "plazo_meses": 12
    })
    assert response.status_code == 422


def test_plazo_minimo_invalido(client):
    response = client.post("/solicitudes/", json={
        "cedula": "123",
        "monto": 1000,
        "plazo_meses": 5
    })
    assert response.status_code == 422


def test_plazo_maximo_invalido(client):
    response = client.post("/solicitudes/", json={
        "cedula": "123",
        "monto": 1000,
        "plazo_meses": 61
    })
    assert response.status_code == 422


def test_listar_solicitudes(client):
    client.post("/solicitudes/", json={"cedula": "111", "monto": 1000, "plazo_meses": 12})
    client.post("/solicitudes/", json={"cedula": "222", "monto": 2000, "plazo_meses": 24})
    response = client.get("/solicitudes/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_filtrar_por_estado(client):
    r = client.post("/solicitudes/", json={"cedula": "111", "monto": 1000, "plazo_meses": 12})
    solicitud_id = r.json()["id"]
    client.post("/solicitudes/", json={"cedula": "222", "monto": 2000, "plazo_meses": 24})

    client.patch(f"/solicitudes/{solicitud_id}/estado", json={
        "estado": "aprobado",
        "comentario": "Todo ok"
    })

    response = client.get("/solicitudes/?estado=pendiente")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["estado"] == "pendiente"


def test_aprobar_solicitud(client):
    r = client.post("/solicitudes/", json={"cedula": "123", "monto": 1000, "plazo_meses": 12})
    solicitud_id = r.json()["id"]

    response = client.patch(f"/solicitudes/{solicitud_id}/estado", json={
        "estado": "aprobado",
        "comentario": "Perfil crediticio aceptable"
    })
    assert response.status_code == 200
    assert response.json()["estado"] == "aprobado"
    assert response.json()["comentario"] == "Perfil crediticio aceptable"


def test_rechazar_solicitud(client):
    r = client.post("/solicitudes/", json={"cedula": "123", "monto": 1000, "plazo_meses": 12})
    solicitud_id = r.json()["id"]

    response = client.patch(f"/solicitudes/{solicitud_id}/estado", json={
        "estado": "rechazado",
        "comentario": "Historial crediticio negativo"
    })
    assert response.status_code == 200
    assert response.json()["estado"] == "rechazado"


def test_no_modificar_solicitud_ya_procesada(client):
    r = client.post("/solicitudes/", json={"cedula": "123", "monto": 1000, "plazo_meses": 12})
    solicitud_id = r.json()["id"]

    client.patch(f"/solicitudes/{solicitud_id}/estado", json={
        "estado": "aprobado",
        "comentario": "Aprobado"
    })

    response = client.patch(f"/solicitudes/{solicitud_id}/estado", json={
        "estado": "rechazado",
        "comentario": "Intento de cambio"
    })
    assert response.status_code == 400


def test_solicitud_no_encontrada(client):
    response = client.patch("/solicitudes/9999/estado", json={
        "estado": "aprobado",
        "comentario": "No existe"
    })
    assert response.status_code == 404
