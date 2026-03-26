import logging
from hotmart._logging import HotmartLogger, mask_sensitive


def test_mask_sensitive_masks_known_keys():
    data = {"authorization": "Bearer secret123", "user": "alice"}
    result = mask_sensitive(data)
    assert "secret123" not in result["authorization"]
    assert result["user"] == "alice"


def test_mask_sensitive_is_case_insensitive():
    data = {"Authorization": "Bearer secret"}
    result = mask_sensitive(data)
    assert "secret" not in str(result["Authorization"])


def test_mask_sensitive_leaves_unknown_keys_unchanged():
    data = {"product_id": 123, "buyer_name": "Paula"}
    assert mask_sensitive(data) == data


def test_request_log_does_not_leak_token(caplog):
    logger = HotmartLogger(log_level=logging.DEBUG)
    with caplog.at_level(logging.DEBUG, logger="hotmart"):
        logger.request(
            method="GET",
            url="https://example.com",
            request_id="req-1",
            params={"authorization": "Bearer supersecret"},
        )
    assert "supersecret" not in caplog.text


def test_auth_refresh_log_never_shows_token_value(caplog):
    logger = HotmartLogger(log_level=logging.DEBUG)
    with caplog.at_level(logging.DEBUG, logger="hotmart"):
        logger.auth_refresh(cached=False)
    assert "token" not in caplog.text.lower() or "refreshed" in caplog.text
