from __future__ import annotations

import httpx


class HotmartError(Exception):
    pass


class AuthenticationError(HotmartError):
    pass


class BadRequestError(HotmartError):
    pass


class NotFoundError(HotmartError):
    pass


class RateLimitError(HotmartError):
    def __init__(self, message: str, retry_after: float = 0.0) -> None:
        super().__init__(message)
        self.retry_after = retry_after


class InternalServerError(HotmartError):
    pass


class APIStatusError(HotmartError):
    def __init__(self, message: str, *, status_code: int, body: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = body


_STATUS_MAP: dict[int, type[HotmartError]] = {
    400: BadRequestError,
    401: AuthenticationError,
    403: AuthenticationError,
    404: NotFoundError,
    500: InternalServerError,
    502: InternalServerError,
    503: InternalServerError,
}


def make_status_error(response: httpx.Response) -> HotmartError:
    body = response.text
    message = f"HTTP {response.status_code}: {body[:200]}"

    if response.status_code == 429:
        retry_after = float(response.headers.get("RateLimit-Reset", 0))
        return RateLimitError(message, retry_after=retry_after)

    exc_class = _STATUS_MAP.get(response.status_code)
    if exc_class is not None:
        return exc_class(message)

    return APIStatusError(message, status_code=response.status_code, body=body)
