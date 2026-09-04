from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_signup_login_flow(client: TestClient) -> None:
    email = "flow@test.com"
    signup = client.post(
        "/api/v1/auth/signup",
        json={
            "email": email,
            "password": "pw12345678",
            "display_name": "테스터",
            "role": "user",
        },
    )
    assert signup.status_code in (201, 400)  # 재실행 시 이미 존재할 수 있음

    login = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "pw12345678"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == email
