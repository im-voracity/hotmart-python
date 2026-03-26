# hotmart-python

Python SDK for the Hotmart API. See [docs/README.md](docs/README.md) for full documentation.

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

for sale in client.sales.history_autopaginate(buyer_name="Paula"):
    print(sale.purchase.transaction)
```

See [English docs](docs/README.md) | [Documentacao em Portugues](docs/README-ptBR.md)
