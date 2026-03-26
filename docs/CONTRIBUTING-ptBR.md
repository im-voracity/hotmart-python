# Contribuindo com o hotmart-python

Obrigado pelo interesse em contribuir! Este guia cobre tudo que voce precisa: configuracao do ambiente, execucao de testes, padroes de codigo e como adicionar um novo endpoint da API Hotmart.

**English documentation available at [CONTRIBUTING.md](CONTRIBUTING.md).**

---

## Indice

- [Primeiros Passos](#primeiros-passos)
- [Executando os Testes](#executando-os-testes)
- [Lint e Formatacao](#lint-e-formatacao)
- [Verificacao de Tipos](#verificacao-de-tipos)
- [Estilo de Codigo](#estilo-de-codigo)
- [Como Adicionar um Novo Endpoint](#como-adicionar-um-novo-endpoint)
- [Referencia da API](#referencia-da-api)
- [Checklist de Pull Request](#checklist-de-pull-request)

---

## Primeiros Passos

Este projeto usa [uv](https://github.com/astral-sh/uv) para gerenciamento de dependencias.

1. Faca o fork e clone o repositorio:

```bash
git clone https://github.com/im-voracity/hotmart-python.git
cd hotmart-python
```

2. Instale todas as dependencias (incluindo as de desenvolvimento):

```bash
uv sync
```

So isso. O `uv` cria e gerencia o ambiente virtual automaticamente — sem precisar configurar `venv` manualmente.

---

## Executando os Testes

```bash
uv run pytest tests/ --ignore=tests/test_integration.py
```

Para saida verbosa com tracebacks curtos:

```bash
uv run pytest tests/ --ignore=tests/test_integration.py -v --tb=short
```

Todos os testes unitarios usam `respx` para mockar HTTP — sem chamadas reais a API, sem necessidade de credenciais.

### Testes de integracao

Os testes de integracao rodam contra a API real da Hotmart. Sao pulados automaticamente se as credenciais nao estiverem presentes:

```bash
# Requer HOTMART_CLIENT_ID, HOTMART_CLIENT_SECRET, HOTMART_BASIC no ambiente
set -a && source .env && set +a
uv run pytest tests/test_integration.py -v
```

Veja o `.env.example` para as variaveis de ambiente esperadas.

---

## Lint e Formatacao

```bash
# Verificar erros de lint
uv run ruff check src/ tests/

# Corrigir automaticamente o que for possivel
uv run ruff check --fix src/ tests/

# Formatar
uv run ruff format src/ tests/

# Verificar formatacao sem modificar arquivos
uv run ruff format --check src/ tests/
```

---

## Verificacao de Tipos

```bash
uv run mypy src/hotmart/
```

O projeto roda `mypy --strict`. Todas as APIs publicas devem ser totalmente anotadas.

---

## Estilo de Codigo

- **Sem `if` aninhados.** Use early returns e guard clauses.
- **Early returns primeiro.** Valide entradas e trate casos de erro no inicio da funcao, antes do caminho feliz.
- **Guard clauses.** Prefira `if not x: return` em vez de `if x: <bloco grande>`.
- **Docstrings em EN + PT-BR.** Todo metodo publico deve ter uma descricao breve em ingles seguida da traducao em portugues. Veja os metodos de recursos existentes para o padrao.

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

Determine a qual grupo de recursos o endpoint pertence (`sales`, `subscriptions`, `products`, `coupons`, `club`, `events` ou `negotiation`). Se for um novo grupo, crie um novo arquivo de recurso seguindo os padroes existentes.

### Passo 2 — Adicione ou atualize o modelo Pydantic

Adicione o modelo de resposta em `src/hotmart/models/`. Mantenha um arquivo por grupo de recursos. Use `extra="allow"` em todos os modelos para que novos campos da API nao quebrem o codigo existente:

```python
# src/hotmart/models/sales.py
from pydantic import BaseModel, ConfigDict

class MeuNovoModelo(BaseModel):
    model_config = ConfigDict(extra="allow")

    campo_um: str
    campo_dois: int | None = None
```

Exporte o novo modelo em `src/hotmart/models/__init__.py` e em `src/hotmart/__init__.py`.

### Passo 3 — Adicione o metodo na classe de recurso

Adicione o metodo no arquivo correspondente em `src/hotmart/resources/`:

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

Se o endpoint for paginado, adicione tambem uma variante `*_autopaginate` seguindo o padrao existente.

### Passo 4 — Escreva os testes

Adicione testes em `tests/resources/`. Siga os padroes existentes — mocke `BaseSyncClient._request` e verifique se a URL e os parametros corretos sao passados:

```python
# tests/resources/test_sales.py
def test_meu_novo_metodo(client, mock_paginated_response):
    with patch.object(client, "_request", return_value=mock_paginated_response) as mock_req:
        client.sales.meu_novo_metodo(algum_param="valor")
    mock_req.assert_called_once()
    _, kwargs = mock_req.call_args
    assert kwargs["params"]["algum_param"] == "valor"
```

### Passo 5 — Atualize a documentacao

Atualize `docs/README.md` e `docs/README-ptBR.md` para documentar o novo metodo na secao de recurso correspondente.

---

## Referencia da API

O arquivo [`HOTMART-API-REFERENCE.md`](HOTMART-API-REFERENCE.md) contem uma referencia completa e legivel por maquina de todos os endpoints da API Hotmart. Ele existe porque a documentacao oficial da Hotmart e renderizada como uma SPA JavaScript e nao e acessivel por crawlers ou agentes de IA.

Se voce estiver implementando um novo endpoint, este arquivo e a sua referencia principal para parametros de requisicao, formatos de resposta e comportamentos conhecidos.

---

## Checklist de Pull Request

Antes de enviar um PR, verifique:

- [ ] `uv run pytest tests/ --ignore=tests/test_integration.py` passa sem falhas
- [ ] `uv run ruff check src/ tests/` nao reporta erros
- [ ] `uv run ruff format --check src/ tests/` nao reporta alteracoes necessarias
- [ ] `uv run mypy src/hotmart/` nao reporta erros
- [ ] Novo endpoint coberto por ao menos um teste
- [ ] `docs/README.md` e `docs/README-ptBR.md` atualizados se aplicavel

---

## Licenca

Ao contribuir com este projeto, voce concorda que suas contribuicoes serao licenciadas sob a Apache License 2.0.
