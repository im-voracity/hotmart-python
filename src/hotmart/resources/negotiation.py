from __future__ import annotations

from ..models.negotiation import NegotiationResponse
from ._base import APIResource


class Negotiation(APIResource):

    def create(self, subscriber_code: str) -> NegotiationResponse | None:
        return self._post("/negotiation", json={"subscriber_code": subscriber_code}, cast_to=NegotiationResponse)
