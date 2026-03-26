import httpx
import pytest

from hotmart._base_client import BaseSyncClient
from hotmart._config import ClientConfig
from hotmart.resources.club import Club

TOKEN_URL = "https://api-sec-vlc.hotmart.com/security/oauth/token"
CLUB_BASE = "https://developers.hotmart.com/club/api/v1"

@pytest.fixture(autouse=True)
def mock_token(respx_mock):
    respx_mock.post(TOKEN_URL).mock(return_value=httpx.Response(200, json={
        "access_token": "tok", "token_type": "bearer", "expires_in": 86400,
    }))

@pytest.fixture
def club():
    config = ClientConfig(client_id="cid", client_secret="csec", basic="Basic x", max_retries=0)
    return Club(BaseSyncClient(config))


def test_modules_returns_list(club, respx_mock):
    data = [{"module_id": "m1", "name": "Module 1", "sequence": 1}]
    respx_mock.get(f"{CLUB_BASE}/modules").mock(return_value=httpx.Response(200, json=data))
    result = club.modules("mysubdomain")
    assert isinstance(result, list)
    assert result[0].module_id == "m1"


def test_modules_passes_subdomain(club, respx_mock):
    captured: list[httpx.Request] = []
    def capture(req: httpx.Request) -> httpx.Response:
        captured.append(req)
        return httpx.Response(200, json=[])
    respx_mock.get(f"{CLUB_BASE}/modules").mock(side_effect=capture)
    club.modules("mysubdomain")
    assert "subdomain=mysubdomain" in str(captured[0].url)


def test_students_returns_list(club, respx_mock):
    respx_mock.get(f"{CLUB_BASE}/students").mock(return_value=httpx.Response(200, json=[{"email": "s@test.com"}]))
    result = club.students("mysubdomain")
    assert len(result) == 1
