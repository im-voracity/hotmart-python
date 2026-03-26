# Contribuindo com o hotmart-python

Obrigado pelo interesse em contribuir! Este guia cobre tudo que você precisa: configuração do ambiente, execução de testes, padrões de código e como adicionar um novo endpoint da API Hotmart.

**English documentation available at [CONTRIBUTING.md](CONTRIBUTING.md).**

---

## Índice

- [Primeiros Passos](#primeiros-passos)
- [Executando os Testes](#executando-os-testes)
- [Lint e Formatação](#lint-e-formatação)
- [Verificação de Tipos](#verificação-de-tipos)
- [Estilo de Código](#estilo-de-código)
- [Como Adicionar um Novo Endpoint](#como-adicionar-um-novo-endpoint)
- [Referência da API](#referência-da-api)
- [Checklist de Pull Request](#checklist-de-pull-request)

---

## Primeiros Passos

Este projeto usa [uv](https://github.com/astral-sh/uv) para gerenciamento de dependências.

1. Faça o fork e clone o repositório:

```bash
git clone https://github.com/im-voracity/hotmart-python.git
cd hotmart-python
```

2. Instale todas as dependências (incluindo as de desenvolvimento):

```bash
uv sync
```

Só isso. O `uv` cria e gerencia o ambiente virtual automaticamente — sem precisar configurar `venv` manualmente.

---

## Executando os Testes

```bash
uv run pytest tests/ --ignore=tests/test_integration.py
```

Para saída verbosa com tracebacks curtos:

```bash
uv run pytest tests/ --ignore=tests/test_integration.py -v --tb=short
```

Todos os testes unitários usam `respx` para mockar HTTP — sem chamadas reais à API, sem necessidade de credenciais.

### Testes de integração

Os testes de integração rodam contra a API real da Hotmart. São pulados automaticamente se as credenciais não estiverem presentes:

```bash
# Requer HOTMART_CLIENT_ID, HOTMART_CLIENT_SECRET, HOTMART_BASIC no ambiente
set -a && source .env && set +a
uv run pytest tests/test_integration.py -v
```

Veja o `.env.example` para as variáveis de ambiente esperadas.

---

## Lint e Formatação

```bash
# Verificar erros de lint
uv run ruff check src/ tests/

# Corrigir automaticamente o que for possível
uv run ruff check --fix src/ tests/

# Formatar
uv run ruff format src/ tests/

# Verificar formatação sem modificar arquivos
uv run ruff format --check src/ tests/
```

---

## Verificação de Tipos

```bash
uv run mypy src/hotmart/
```

O projeto roda `mypy --strict`. Todas as APIs públicas devem ser totalmente anotadas.

---

## Estilo de Código

- **Sem `if` aninhados.** Use early returns e guard clauses.
- **Early returns primeiro.** Valide entradas e trate casos de erro no início da função, antes do caminho feliz.
- **Guard clauses.** Prefira `if not x: return` em vez de `if x: <bloco grande>`.
- **Docstrings em EN + PT-BR.** Todo método público deve ter uma descrição breve em inglês seguida da tradução em português. Veja os métodos de recursos existentes para o padrão.

**Preferido:**

```python
def meu_metodo(self, valor: str | None) -> str:
    if not valor:
        return ""
    if len(valor) > 100:
        raise ValueError("valor muito longo")
    return valor.strip()
```

**Evite:**

```python
def meu_metodo(self, valor: str | None) -> str:
    if valor:
        if len(valor) <= 100:
            return valor.strip()
    return ""
```

---

## Como Adicionar um Novo Endpoint

### Passo 1 — Identifique o recurso

Determine a qual grupo de recursos o endpoint pertence (`sales`, `subscriptions`, `products`, `coupons`, `club`, `events` ou `negotiation`). Se for um novo grupo, crie um novo arquivo de recurso seguindo os padrões existentes.

### Passo 2 — Adicione ou atualize o modelo Pydantic

Adicione o modelo de resposta em `src/hotmart/models/`. Mantenha um arquivo por grupo de recursos. Use `extra="allow"` em todos os modelos para que novos campos da API não quebrem o código existente:

```python
# src/hotmart/models/sales.py
from pydantic import BaseModel, ConfigDict

class MeuNovoModelo(BaseModel):
    model_config = ConfigDict(extra="allow")

    campo_um: str
    campo_dois: int | None = None
```

Exporte o novo modelo em `src/hotmart/models/__init__.py` e em `src/hotmart/__init__.py`.

### Passo 3 — Adicione o método na classe de recurso

Adicione o método no arquivo correspondente em `src/hotmart/resources/`:

```python
# src/hotmart/resources/sales.py
def meu_novo_metodo(
    self,
    *,
    algum_param: str | None = None,
    **kwargs: Any,
) -> PaginatedResponse[MeuNovoModelo]:
    """Fetch my new resource.

    Busca o novo recurso.
    """
    params = _build_params(locals())
    return self._get("/meu-endpoint", params=params, cast_to=PaginatedResponse[MeuNovoModelo])  # type: ignore[return-value]
```

Se o endpoint for paginado, adicione também uma variante `*_autopaginate` seguindo o padrão existente.

### Passo 4 — Escreva os testes

Adicione testes em `tests/resources/`. Siga os padrões existentes — mocke `BaseSyncClient._request` e verifique se a URL e os parâmetros corretos são passados:

```python
# tests/resources/test_sales.py
def test_meu_novo_metodo(client, mock_paginated_response):
    with patch.object(client, "_request", return_value=mock_paginated_response) as mock_req:
        client.sales.meu_novo_metodo(algum_param="valor")
    mock_req.assert_called_once()
    _, kwargs = mock_req.call_args
    assert kwargs["params"]["algum_param"] == "valor"
```

### Passo 5 — Atualize a documentação

Atualize `README.md` e `docs/README-ptBR.md` para documentar o novo método na seção de recurso correspondente.

---

## Referência da API

O arquivo [`HOTMART-API-REFERENCE.md`](HOTMART-API-REFERENCE.md) contém uma referência completa e legível por máquina de todos os endpoints da API Hotmart. Ele existe porque a documentação oficial da Hotmart é renderizada como uma SPA JavaScript e não é acessível por crawlers ou agentes de IA.

Se você estiver implementando um novo endpoint, este arquivo é a sua referência principal para parâmetros de requisição, formatos de resposta e comportamentos conhecidos.

---

## Checklist de Pull Request

Antes de enviar um PR, verifique:

- [ ] `uv run pytest tests/ --ignore=tests/test_integration.py` passa sem falhas
- [ ] `uv run ruff check src/ tests/` não reporta erros
- [ ] `uv run ruff format --check src/ tests/` não reporta alterações necessárias
- [ ] `uv run mypy src/hotmart/` não reporta erros
- [ ] Novo endpoint coberto por ao menos um teste
- [ ] `README.md` e `docs/README-ptBR.md` atualizados se aplicável

---

## Licença

Ao contribuir com este projeto, você concorda que suas contribuições serão licenciadas sob a Apache License 2.0.
