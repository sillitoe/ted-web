from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from app.core.config import settings
from app.utils import generate_password_reset_token


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_get_access_token_incorrect_password(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": "incorrect",
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert r.status_code == 400


def test_use_access_token(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/login/test-token",
        headers=superuser_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert "email" in result


def test_recovery_password(
    client: TestClient, normal_user_token_headers: dict[str, str], mocker: MockerFixture
) -> None:
    mocker.patch("app.utils.send_email", return_value=None)
    mocker.patch("app.core.config.settings.SMTP_HOST", "smtp.example.com")
    mocker.patch("app.core.config.settings.SMTP_USER", "admin@example.com")
    email = "test@example.com"
    r = client.post(
        f"{settings.API_V1_STR}/password-recovery/{email}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 200
    assert r.json() == {"message": "Password recovery email sent"}


def test_recovery_password_user_not_exits(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    email = "jVgQr@example.com"
    r = client.post(
        f"{settings.API_V1_STR}/password-recovery/{email}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 404

# TODO: this changes the superuser password, which makes subsequent tests fail
#
# def test_reset_password(
#     client: TestClient, superuser_token_headers: dict[str, str]
# ) -> None:
#     token = generate_password_reset_token(email=settings.FIRST_SUPERUSER)
#     data = {"new_password": "changethis", "token": token}
#     r = client.post(
#         f"{settings.API_V1_STR}/reset-password/",
#         headers=superuser_token_headers,
#         json=data,
#     )
#     assert r.status_code == 200
#     assert r.json() == {"message": "Password updated successfully"}


def test_reset_password_invalid_token(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"new_password": "changethis", "token": "invalid"}
    r = client.post(
        f"{settings.API_V1_STR}/reset-password/",
        headers=superuser_token_headers,
        json=data,
    )
    response = r.json()

    assert "detail" in response
    assert r.status_code == 400
    assert response["detail"] == "Invalid token"
