# hotmart-python — SDK Python para a API Hotmart

![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![PyPI version](https://img.shields.io/pypi/v/hotmart-python)
![Licenca Apache 2.0](https://img.shields.io/badge/licenca-Apache%202.0-green)

SDK Python tipado para a [API Hotmart](https://developers.hotmart.com/docs/en/). Cobre todos os 7 grupos de recursos da plataforma, com refresh automatico de token, retentativas com backoff exponencial, controle proativo de rate limit e iteradores de paginacao.

A Hotmart e uma plataforma brasileira de produtos digitais, aceita pagamentos via PIX, boleto bancario, cartao de credito e outros metodos.

**English documentation available at [README.md](README.md).**

---

## Indice

- [Instalacao](#instalacao)
- [Inicio Rapido](#inicio-rapido)
- [Autenticacao](#autenticacao)
- [Recursos](#recursos)
  - [Vendas](#vendas)
  - [Assinaturas](#assinaturas)
  - [Produtos](#produtos)
  - [Cupons de Desconto](#cupons-de-desconto)
  - [Club (Area de Membros)](#club-area-de-membros)
  - [Eventos](#eventos)
  - [Negociacao de Parcelas](#negociacao-de-parcelas)
- [Paginacao](#paginacao)
- [Modo Sandbox](#modo-sandbox)
- [Tratamento de Erros](#tratamento-de-erros)
- [Logging](#logging)
- [Gerenciador de Contexto](#gerenciador-de-contexto)
- [Parametros Extras (kwargs)](#parametros-extras-kwargs)
- [Licenca](#licenca)

---

## Instalacao

```bash
pip install hotmart-python
```

Ou com [uv](https://github.com/astral-sh/uv):

```bash
uv add hotmart-python
```

---

## Inicio Rapido

```python
from hotmart import Hotmart

client = Hotmart(
    client_id="seu_client_id",
    client_secret="seu_client_secret",
    basic="Basic suas_credenciais_base64",
)

pagina = client.sales.history(buyer_name="Paula")
for venda in pagina.items:
    print(venda.purchase.transaction, venda.buyer.email)
```

---

## Autenticacao

A Hotmart utiliza **OAuth 2.0 Client Credentials**. O SDK gerencia a obtencao e o refresh do token automaticamente — voce apenas precisa fornecer tres valores na inicializacao.

### Onde encontrar suas credenciais

1. Acesse o [Hotmart](https://app.hotmart.com) e faca login.
2. Va em **Ferramentas → Ferramentas para Desenvolvedores → Credenciais** (secao de Credenciais de Desenvolvedor).
3. Gere um novo conjunto de credenciais. Voce recebera:
   - `client_id` — o ID do seu aplicativo
   - `client_secret` — o segredo do seu aplicativo
   - `basic` — a string Base64 de `client_id:client_secret` prefixada com `Basic ` (a Hotmart exibe esse valor diretamente no painel)

```python
from hotmart import Hotmart

client = Hotmart(
    client_id="abcdef12-1234-5678-abcd-abcdef123456",
    client_secret="seu_segredo_aqui",
    basic="Basic YWJjZGVmMTItMTIzNC01Njc4LWFiY2QtYWJjZGVmMTIzNDU2OnNldV9zZWdyZWRvX2FxdWk=",
)
```

Os tokens sao validos por 24 horas. O SDK armazena o token em cache e o renova proativamente antes do vencimento, com thread safety garantido.

---

## Recursos

### Vendas

A Hotmart suporta diversos metodos de pagamento: PIX, boleto bancario, cartao de credito (parcelado ou a vista), cartao de debito, PayPal, entre outros.

```python
# Pagina unica
pagina = client.sales.history(buyer_name="Paula", transaction_status="APPROVED")
pagina = client.sales.summary(start_date=1700000000000, end_date=1710000000000)
pagina = client.sales.participants(buyer_email="paula@exemplo.com.br")
pagina = client.sales.commissions(commission_as="PRODUCER")
pagina = client.sales.price_details(product_id=1234567)

# Solicitar reembolso
client.sales.refund("HP17715690036014")

# Autopaginacao (iterador — percorre todas as paginas automaticamente)
for venda in client.sales.history_autopaginate(buyer_name="Paula"):
    print(venda.purchase.transaction)
```

Metodos disponiveis:

| Metodo | Descricao |
|--------|-----------|
| `history(**kwargs)` | Lista todas as vendas com informacoes detalhadas |
| `history_autopaginate(**kwargs)` | Iterador sobre todas as paginas |
| `summary(**kwargs)` | Total de comissoes por moeda |
| `summary_autopaginate(**kwargs)` | Iterador sobre todas as paginas |
| `participants(**kwargs)` | Dados de participantes por venda |
| `participants_autopaginate(**kwargs)` | Iterador sobre todas as paginas |
| `commissions(**kwargs)` | Detalhamento de comissoes por venda |
| `commissions_autopaginate(**kwargs)` | Iterador sobre todas as paginas |
| `price_details(**kwargs)` | Detalhes de preco e taxas por venda |
| `price_details_autopaginate(**kwargs)` | Iterador sobre todas as paginas |
| `refund(transaction_code)` | Solicita reembolso de uma transacao |

---

### Assinaturas

Ideal para planos de assinatura mensais, anuais e recorrentes.

```python
# Listar assinantes
pagina = client.subscriptions.list(status="ACTIVE", product_id=1234567)

# Resumo de assinaturas
pagina = client.subscriptions.summary()

# Compras e transacoes de um assinante especifico
compras = client.subscriptions.purchases("SUB-ABC123")
transacoes = client.subscriptions.transactions("SUB-ABC123")

# Cancelar uma ou mais assinaturas
resultado = client.subscriptions.cancel(["SUB-ABC123", "SUB-DEF456"], send_mail=True)

# Reativar assinaturas (em lote)
resultado = client.subscriptions.reactivate(["SUB-ABC123"], charge=False)

# Reativar uma unica assinatura
resultado = client.subscriptions.reactivate_single("SUB-ABC123", charge=True)

# Alterar data de vencimento
client.subscriptions.change_due_day("SUB-ABC123", due_day=15)

# Autopaginacao
for assinante in client.subscriptions.list_autopaginate(status="ACTIVE"):
    print(assinante.subscriber_code)
```

Metodos disponiveis:

| Metodo | Descricao |
|--------|-----------|
| `list(**kwargs)` | Lista assinaturas com filtros |
| `list_autopaginate(**kwargs)` | Iterador sobre todas as paginas |
| `summary(**kwargs)` | Resumo de assinaturas |
| `summary_autopaginate(**kwargs)` | Iterador sobre todas as paginas |
| `purchases(subscriber_code)` | Historico de compras de um assinante |
| `transactions(subscriber_code)` | Transacoes de um assinante |
| `cancel(subscriber_code, send_mail)` | Cancela uma ou mais assinaturas |
| `reactivate(subscriber_code, charge)` | Reativa assinaturas (em lote) |
| `reactivate_single(subscriber_code, charge)` | Reativa uma unica assinatura |
| `change_due_day(subscriber_code, due_day)` | Altera o dia de vencimento da cobranca |

---

### Produtos

```python
# Listar produtos
pagina = client.products.list(status="ACTIVE")

# Ofertas de um produto
pagina = client.products.offers("ucode-do-produto")

# Planos de um produto
pagina = client.products.plans("ucode-do-produto")

# Autopaginacao
for produto in client.products.list_autopaginate():
    print(produto.name)
```

Metodos disponiveis:

| Metodo | Descricao |
|--------|-----------|
| `list(**kwargs)` | Lista todos os produtos |
| `list_autopaginate(**kwargs)` | Iterador sobre todas as paginas |
| `offers(ucode, **kwargs)` | Ofertas de um produto |
| `offers_autopaginate(ucode, **kwargs)` | Iterador sobre todas as paginas |
| `plans(ucode, **kwargs)` | Planos de um produto |
| `plans_autopaginate(ucode, **kwargs)` | Iterador sobre todas as paginas |

---

### Cupons de Desconto

```python
# Criar cupom de 10% de desconto para o produto 1234567
client.coupons.create("1234567", "VERAO10", discount=10.0)

# Listar cupons de um produto
pagina = client.coupons.list("1234567")

# Excluir cupom por ID
client.coupons.delete("id-do-cupom")

# Autopaginacao
for cupom in client.coupons.list_autopaginate("1234567"):
    print(cupom.code)
```

Metodos disponiveis:

| Metodo | Descricao |
|--------|-----------|
| `create(product_id, coupon_code, discount)` | Cria um cupom de desconto |
| `list(product_id, **kwargs)` | Lista cupons de um produto |
| `list_autopaginate(product_id, **kwargs)` | Iterador sobre todas as paginas |
| `delete(coupon_id)` | Exclui um cupom |

---

### Club (Area de Membros)

O recurso Club requer o argumento `subdomain` — o subdominio da sua Area de Membros.

```python
# Modulos da area de membros
modulos = client.club.modules("subdominio-do-curso")

# Paginas de um modulo
paginas = client.club.pages("subdominio-do-curso", module_id="uuid-do-modulo")

# Alunos matriculados
alunos = client.club.students("subdominio-do-curso")

# Progresso dos alunos
progresso = client.club.student_progress(
    "subdominio-do-curso",
    student_email="aluno@exemplo.com.br",
)
```

Metodos disponiveis:

| Metodo | Descricao |
|--------|-----------|
| `modules(subdomain, **kwargs)` | Lista modulos da area de membros |
| `pages(subdomain, module_id, **kwargs)` | Lista paginas de um modulo |
| `students(subdomain, **kwargs)` | Lista alunos matriculados |
| `student_progress(subdomain, **kwargs)` | Dados de progresso dos alunos |

---

### Eventos

```python
# Obter detalhes de um evento
evento = client.events.get("id-do-evento")

# Listar ingressos de um produto
pagina = client.events.tickets(product_id=1234567)

# Autopaginacao
for ingresso in client.events.tickets_autopaginate(product_id=1234567):
    print(ingresso.name)
```

Metodos disponiveis:

| Metodo | Descricao |
|--------|-----------|
| `get(event_id)` | Retorna detalhes de um evento |
| `tickets(product_id, **kwargs)` | Lista ingressos de um produto |
| `tickets_autopaginate(product_id, **kwargs)` | Iterador sobre todas as paginas |

---

### Negociacao de Parcelas

```python
# Criar negociacao de parcelas para um assinante
resultado = client.negotiation.create("SUB-ABC123")
```

Metodos disponiveis:

| Metodo | Descricao |
|--------|-----------|
| `create(subscriber_code)` | Cria uma negociacao de parcelas |

---

## Paginacao

A API Hotmart usa paginacao baseada em cursor. Cada resposta paginada contem um objeto `page_info` com `next_page_token`.

### Chamada de pagina unica

Retorna um `PaginatedResponse[T]` com `.items` e `.page_info`:

```python
pagina = client.sales.history(max_results=50)
print(f"Recebidos {len(pagina.items)} itens")
print(f"Proximo token: {pagina.page_info.next_page_token}")

# Buscar proxima pagina manualmente
proxima_pagina = client.sales.history(page_token=pagina.page_info.next_page_token)
```

### Autopaginacao (recomendado)

Cada metodo paginado possui uma variante `*_autopaginate` que retorna um iterador e gerencia automaticamente todas as paginas:

```python
for venda in client.sales.history_autopaginate(buyer_name="Paula"):
    print(venda.purchase.transaction)
```

O iterador para automaticamente quando nao ha mais paginas.

---

## Modo Sandbox

Use `sandbox=True` para apontar todas as requisicoes para o ambiente sandbox da Hotmart. Voce precisa de **credenciais sandbox separadas** — credenciais de producao e sandbox nao sao intercambiaveis.

Gere as credenciais sandbox no painel da Hotmart, na mesma secao de Credenciais de Desenvolvedor, selecionando "Sandbox" como ambiente.

```python
from hotmart import Hotmart

client = Hotmart(
    client_id="seu_client_id_sandbox",
    client_secret="seu_client_secret_sandbox",
    basic="Basic suas_credenciais_sandbox_base64",
    sandbox=True,
)

pagina = client.sales.history()
```

Observacao: alguns endpoints se comportam de forma diferente ou nao sao totalmente suportados no ambiente sandbox. Consulte o [SANDBOX-GUIDE.md](SANDBOX-GUIDE.md) para detalhes.

---

## Tratamento de Erros

Todos os erros do SDK herdam de `HotmartError`. Importe e capture as excecoes especificas conforme necessario:

```python
from hotmart import (
    Hotmart,
    HotmartError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    BadRequestError,
    InternalServerError,
)

client = Hotmart(
    client_id="...",
    client_secret="...",
    basic="Basic ...",
)

try:
    pagina = client.sales.history()
except AuthenticationError:
    print("Verifique suas credenciais.")
except RateLimitError as e:
    print(f"Limite de requisicoes atingido. Tente novamente em {e.retry_after} segundos.")
except NotFoundError:
    print("Recurso nao encontrado.")
except HotmartError as e:
    print(f"Erro da API: {e}")
```

Hierarquia de excecoes:

| Excecao | Status HTTP | Significado |
|---------|------------|-------------|
| `AuthenticationError` | 401, 403 | Credenciais invalidas ou ausentes |
| `BadRequestError` | 400 | Parametros invalidos |
| `NotFoundError` | 404 | Recurso nao encontrado |
| `RateLimitError` | 429 | Limite de requisicoes excedido (500 req/min) |
| `InternalServerError` | 500, 502, 503 | Erro interno do servidor Hotmart |
| `APIStatusError` | outros | Status HTTP inesperado |
| `HotmartError` | — | Classe base para todos os erros do SDK |

O SDK realiza retentativas automaticas em erros transitorios (5xx, 429) com backoff exponencial. Configure o numero de tentativas via `max_retries`:

```python
client = Hotmart(..., max_retries=5)
```

---

## Logging

O logging e desabilitado por padrao. Habilite-o passando `log_level` na inicializacao:

```python
import logging
from hotmart import Hotmart

client = Hotmart(
    client_id="...",
    client_secret="...",
    basic="Basic ...",
    log_level=logging.INFO,
)
```

Niveis de log disponiveis:

| Nivel | O que e registrado |
|-------|-------------------|
| `logging.DEBUG` | URLs das requisicoes, parametros (contem dados sensiveis — evite em producao) |
| `logging.INFO` | Resumos de operacoes em alto nivel |
| `logging.WARNING` | Avisos e condicoes inesperadas (padrao) |
| `logging.ERROR` | Erros durante interacoes com a API |
| `logging.CRITICAL` | Falhas criticas |

Segredos (tokens, credenciais) sao mascarados na saida de log.

---

## Gerenciador de Contexto

`Hotmart` suporta o protocolo de gerenciador de contexto para limpeza automatica do pool de conexoes HTTP:

```python
from hotmart import Hotmart

with Hotmart(
    client_id="...",
    client_secret="...",
    basic="Basic ...",
) as client:
    for venda in client.sales.history_autopaginate():
        print(venda.purchase.transaction)
```

---

## Parametros Extras (kwargs)

Todos os metodos de recursos aceitam `**kwargs` e repassam argumentos extras diretamente para a API como parametros de query. Isso permite usar parametros nao documentados ou recentemente adicionados sem precisar aguardar atualizacoes do SDK:

```python
# Passe qualquer parametro de query suportado pela Hotmart
pagina = client.sales.history(parametro_futuro="valor")
```

---

## Licenca

Apache License 2.0 — veja [LICENSE.txt](../LICENSE.txt) para detalhes.

Este pacote nao e afiliado nem oficialmente suportado pela Hotmart.
