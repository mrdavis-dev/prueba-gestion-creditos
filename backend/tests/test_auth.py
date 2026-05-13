def test_login_exitoso(client):
    client.post("/auth/register", json={"username": "admin", "password": "admin123"})
    response = client.post("/auth/login", json={"username": "admin", "password": "admin123"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_credenciales_invalidas(client):
    client.post("/auth/register", json={"username": "admin", "password": "admin123"})
    response = client.post("/auth/login", json={"username": "admin", "password": "wrongpass"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales inválidas"


def test_login_usuario_no_existe(client):
    response = client.post("/auth/login", json={"username": "noexiste", "password": "1234"})
    assert response.status_code == 401


def test_register_exitoso(client):
    response = client.post("/auth/register", json={"username": "nuevo", "password": "pass123"})
    assert response.status_code == 201
    assert "access_token" in response.json()


def test_register_usuario_duplicado(client):
    client.post("/auth/register", json={"username": "admin", "password": "admin123"})
    response = client.post("/auth/register", json={"username": "admin", "password": "admin123"})
    assert response.status_code == 400
    assert response.json()["detail"] == "El usuario ya existe"
