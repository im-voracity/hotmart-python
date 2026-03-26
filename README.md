# hotmart-python

Python SDK for the Hotmart API. See the full documentation below.

- [English docs](docs/README.md)
- [Documentacao em Portugues](docs/README-ptBR.md)
- [Contributing](docs/CONTRIBUTING.md) | [Contribuindo](docs/CONTRIBUTING-ptBR.md)

## Quick Install

```bash
pip install hotmart-python
```

Or with uv:

```bash
uv add hotmart-python
```

## Quick Example

```python
from hotmart import Hotmart

client = Hotmart(
    client_id="your_client_id",
    client_secret="your_client_secret",
    basic="Basic your_base64_credentials",
)

# All sales, all pages — one iterator
for sale in client.sales.history_autopaginate(transaction_status="APPROVED"):
    print(sale.purchase.transaction, sale.buyer.email)
```
