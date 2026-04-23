from __future__ import annotations

from ..models.negotiation import NegotiationResponse
from ._async_base import AsyncAPIResource


class AsyncNegotiation(AsyncAPIResource):

    async def create(self, subscriber_code: str) -> NegotiationResponse | None:
        return await self._post("/negotiation", json={"subscriber_code": subscriber_code}, cast_to=NegotiationResponse)
