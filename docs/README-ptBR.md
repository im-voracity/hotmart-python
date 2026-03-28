# hotmart-python — SDK Python para a API Hotmart

![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![PyPI version](https://img.shields.io/pypi/v/hotmart-python)
![Licença Apache 2.0](https://img.shields.io/badge/licen%C3%A7a-Apache%202.0-green)

**hotmart-python** é um SDK Python tipado para a [API Hotmart](https://developers.hotmart.com/docs/en/).
O [Hotmart](https://www.hotmart.com) é uma plataforma brasileira de produtos digitais — cursos, ebooks, assinaturas e áreas de membros — com suporte a PIX, boleto, cartão de crédito/débito e PayPal.

Este SDK cuida de autenticação OAuth, refresh de token, retentativas, rate limit e paginação automaticamente. Você escreve regra de negócio; o SDK gerencia a API.

**English documentation available at [README.md](../README.md).**

---

## Recursos

- **Respostas totalmente tipadas** — cada resposta da API é um modelo Pydantic v2. Seu IDE completa os campos; sem dicts crus, sem adivinhações.
- **Iteradores de autopaginação** — todo endpoint paginado tem uma variante `*_autopaginate` que percorre todas as páginas automaticamente. Um `for`, todos os registros.
- **Gerenciamento automático de token** — o token OAuth é obtido, armazenado em cache e renovado proativamente 5 minutos antes do vencimento. Thread-safe com double-checked locking.
- **Retry com backoff exponencial** — erros transitórios (5xx, 429) são reprocessados automaticamente com jitter e respeito ao `RateLimit-Reset`. Configurável via `max_retries`.
- **Controle proativo de rate limit** — monitora as requisições restantes por janela e recua antes de atingir o limite.
- **Hierarquia de exceções clara** — capture apenas o que interessa: `AuthenticationError`, `RateLimitError`, `NotFoundError`, `BadRequestError`, entre outros.
- **httpx por baixo** — pool de conexões persistente, timeouts configuráveis, suporte a gerenciador de contexto.
- **kwargs forward-compatible** — `**kwargs` extras são repassados diretamente como query params, permitindo usar parâmetros novos ou não documentados da Hotmart sem aguardar atualizações do SDK.

---

## Princípios de Design

- **Um objeto, todos os recursos.** Instancie `Hotmart` uma vez e acesse cada grupo de recursos como atributo: `client.sales`, `client.subscriptions`, `client.products`, etc.
- **Falhe alto.** Erros são exceções tipadas, nunca suprimidos silenciosamente ou escondidos em valores de retorno.
- **Sem boilerplate.** Autenticação, paginação, retentativas e gerenciamento de conexão são invisíveis por padrão. Configuração é opt-in.
- **Tipagem estrita.** `mypy --strict` passa. Todas as APIs públicas são totalmente anotadas. Modelos usam `extra="allow"` para que novos campos da API não quebrem seu código.

---

## Índice

- [Instalação](#instalação)
- [Início Rápido](#início-rápido)
- [Autenticação](#autenticação)
- [Recursos da API](#recursos-da-api)
  - [Vendas](#vendas)
  - [Assinaturas](#assinaturas)
  - [Produtos](#produtos)
  - [Cupons de Desconto](#cupons-de-desconto)
  - [Club (Área de Membros)](#club-área-de-membros)
  - [Eventos](#eventos)
  - [Negociação de Parcelas](#negociação-de-parcelas)
- [Paginação](#paginação)
- [Modo Sandbox](#modo-sandbox)
- [Tratamento de Erros](#tratamento-de-erros)
- [Logging](#logging)
- [Gerenciador de Contexto](#gerenciador-de-contexto)
- [Parâmetros Extras (kwargs)](#parâmetros-extras-kwargs)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

---

## Instalação

```bash
pip install hotmart-python
```

Ou com [uv](https://github.com/astral-sh/uv):

```bash
uv add hotmart-python
```

**Requisito:** Python 3.11+

---

## Início Rápido

```python
from hotmart import Hotmart

client = Hotmart(
    client_id="seu_client_id",
    client_secret="seu_client_secret",
    basic="Basic suas_credenciais_base64",
)

# Página única
pagina = client.sales.history(buyer_name="Paula")
for venda in pagina.items:
    print(venda.purchase.transaction, venda.buyer.email)

# Todas as páginas — um iterador, sem paginação manual
for venda in client.sales.history_autopaginate(transaction_status="APPROVED"):
    print(venda.purchase.transaction)
```

---

## Autenticação

A Hotmart utiliza **OAuth 2.0 Client Credentials**. O SDK gerencia a obtenção e o refresh do token automaticamente — você apenas precisa fornecer três valores na inicialização.

### Onde encontrar suas credenciais

1. Acesse o [Hotmart](https://app.hotmart.com) e faça login.
2. Vá em **Ferramentas → Ferramentas para Desenvolvedores → Credenciais**.
3. Gere um novo conjunto de credenciais. Você receberá:
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

Os tokens são válidos por 24 horas. O SDK armazena o token em cache e o renova proativamente 5 minutos antes do vencimento com thread safety, de forma que requisições concorrentes nunca disputem pela renovação.

---

## Recursos da API

### Vendas

A Hotmart suporta PIX, boleto bancário, cartão de crédito (parcelado ou à vista), cartão de débito, PayPal, entre outros métodos de pagamento.

```python
# Página única
pagina = client.sales.history(buyer_name="Paula", transaction_status="APPROVED")
pagina = client.sales.summary(start_date=1700000000000, end_date=1710000000000)
pagina = client.sales.participants(buyer_email="paula@exemplo.com.br")
pagina = client.sales.commissions(commission_as="PRODUCER")
pagina = client.sales.price_details(product_id=1234567)

# Solicitar reembolso
client.sales.refund("HP17715690036014")

# Autopaginação — percorre todas as páginas automaticamente
for venda in client.sales.history_autopaginate(buyer_name="Paula"):
    print(venda.purchase.transaction)
```

| Método | Descrição |
|--------|-----------|
| `history(**kwargs)` | Lista todas as vendas com informações detalhadas |
| `history_autopaginate(**kwargs)` | Iterador sobre todas as páginas |
| `summary(**kwargs)` | Total de comissões por moeda |
| `summary_autopaginate(**kwargs)` | Iterador sobre todas as páginas |
| `participants(**kwargs)` | Dados de participantes por venda |
| `participants_autopaginate(**kwargs)` | Iterador sobre todas as páginas |
| `commissions(**kwargs)` | Detalhamento de comissões por venda |
| `commissions_autopaginate(**kwargs)` | Iterador sobre todas as páginas |
| `price_details(**kwargs)` | Detalhes de preço e taxas por venda |
| `price_details_autopaginate(**kwargs)` | Iterador sobre todas as páginas |
| `refund(transaction_code)` | Solicita reembolso de uma transação |

---

### Assinaturas

Ideal para planos mensais, anuais e cobranças recorrentes.

```python
# Listar assinantes
pagina = client.subscriptions.list(status="ACTIVE", product_id=1234567)

# Resumo de assinaturas
pagina = client.subscriptions.summary()

# Compras e transações de um assinante específico
compras = client.subscriptions.purchases("SUB-ABC123")
transacoes = client.subscriptions.transactions("SUB-ABC123")

# Cancelar uma ou mais assinaturas
resultado = client.subscriptions.cancel(["SUB-ABC123", "SUB-DEF456"], send_mail=True)

# Reativar assinaturas (em lote)
resultado = client.subscriptions.reactivate(["SUB-ABC123"], charge=False)

# Reativar uma única assinatura
resultado = client.subscriptions.reactivate_single("SUB-ABC123", charge=True)

# Alterar data de vencimento
client.subscriptions.change_due_day("SUB-ABC123", due_day=15)

# Autopaginação
for assinante in client.subscriptions.list_autopaginate(status="ACTIVE"):
    print(assinante.subscriber_code)
```

| Método | Descrição |
|--------|-----------|
| `list(**kwargs)` | Lista assinaturas com filtros |
| `list_autopaginate(**kwargs)` | Iterador sobre todas as páginas |
| `summary(**kwargs)` | Resumo de assinaturas |
| `summary_autopaginate(**kwargs)` | Iterador sobre todas as páginas |
| `purchases(subscriber_code)` | Histórico de compras de um assinante |
| `transactions(subscriber_code)` | Transações de um assinante |
| `cancel(subscriber_code, send_mail)` | Cancela uma ou mais assinaturas |
| `reactivate(subscriber_code, charge)` | Reativa assinaturas (em lote) |
| `reactivate_single(subscriber_code, charge)` | Reativa uma única assinatura |
| `change_due_day(subscriber_code, due_day)` | Altera o dia de vencimento da cobrança |

---

### Produtos

```python
# Listar produtos
pagina = client.products.list(status="ACTIVE")

# Ofertas de um produto
pagina = client.products.offers("ucode-do-produto")

# Planos de um produto
pagina = client.products.plans("ucode-do-produto")

# Autopaginação
for produto in client.products.list_autopaginate():
    print(produto.name)
```

| Método | Descrição |
|--------|-----------|
| `list(**kwargs)` | Lista todos os produtos |
| `list_autopaginate(**kwargs)` | Iterador sobre todas as páginas |
| `offers(ucode, **kwargs)` | Ofertas de um produto |
| `offers_autopaginate(ucode, **kwargs)` | Iterador sobre todas as páginas |
| `plans(ucode, **kwargs)` | Planos de um produto |
| `plans_autopaginate(ucode, **kwargs)` | Iterador sobre todas as páginas |

---

### Cupons de Desconto

```python
# Criar cupom de 10% de desconto para o produto 1234567
client.coupons.create("1234567", "VERAO10", discount=10.0)

# Listar cupons de um produto
pagina = client.coupons.list("1234567")

# Excluir cupom por ID
client.coupons.delete("id-do-cupom")

# Autopaginação
for cupom in client.coupons.list_autopaginate("1234567"):
    print(cupom.code)
```

| Método | Descrição |
|--------|-----------|
| `create(product_id, coupon_code, discount)` | Cria um cupom de desconto |
| `list(product_id, **kwargs)` | Lista cupons de um produto |
| `list_autopaginate(product_id, **kwargs)` | Iterador sobre todas as páginas |
| `delete(coupon_id)` | Exclui um cupom |

---

### Club (Área de Membros)

O recurso Club requer o argumento `subdomain` — o subdomínio da sua Área de Membros.

```python
# Módulos da área de membros
modulos = client.club.modules("subdominio-do-curso")

# Páginas de um módulo
paginas = client.club.pages("subdominio-do-curso", module_id="uuid-do-modulo")

# Alunos matriculados
alunos = client.club.students("subdominio-do-curso")

# Progresso dos alunos
progresso = client.club.student_progress(
    "subdominio-do-curso",
    student_email="aluno@exemplo.com.br",
)
```

| Método | Descrição |
|--------|-----------|
| `modules(subdomain, **kwargs)` | Lista módulos da área de membros |
| `pages(subdomain, module_id, **kwargs)` | Lista páginas de um módulo |
| `students(subdomain, **kwargs)` | Lista alunos matriculados |
| `student_progress(subdomain, **kwargs)` | Dados de progresso dos alunos |

---

### Eventos

```python
# Obter detalhes de um evento
evento = client.events.get("id-do-evento")

# Listar ingressos de um produto
pagina = client.events.tickets(product_id=1234567)

# Autopaginação
for ingresso in client.events.tickets_autopaginate(product_id=1234567):
    print(ingresso.name)
```

| Método | Descrição |
|--------|-----------|
| `get(event_id)` | Retorna detalhes de um evento |
| `tickets(product_id, **kwargs)` | Lista ingressos de um produto |
| `tickets_autopaginate(product_id, **kwargs)` | Iterador sobre todas as páginas |

---

### Negociação de Parcelas

```python
# Criar negociação de parcelas para um assinante
resultado = client.negotiation.create("SUB-ABC123")
```

| Método | Descrição |
|--------|-----------|
| `create(subscriber_code)` | Cria uma negociação de parcelas |

---

## Paginação

A API Hotmart usa paginação baseada em cursor. Cada resposta paginada contém um objeto `page_info` com `next_page_token`.

### Chamada de página única

Retorna um `PaginatedResponse[T]` com `.items` e `.page_info`:

```python
pagina = client.sales.history(max_results=50)
print(f"Recebidos {len(pagina.items)} itens")
print(f"Próximo token: {pagina.page_info.next_page_token}")

# Buscar próxima página manualmente
proxima_pagina = client.sales.history(page_token=pagina.page_info.next_page_token)
```

### Autopaginação (recomendado)

Cada método paginado possui uma variante `*_autopaginate` que gerencia todas as páginas automaticamente:

```python
for venda in client.sales.history_autopaginate(buyer_name="Paula"):
    print(venda.purchase.transaction)
```

O iterador para automaticamente quando não há mais páginas — sem gerenciamento de token, sem condições de loop.

### Processamento página a página

Se você precisar agir ao final de cada página — salvar um checkpoint, enviar um batch para o banco, atualizar uma barra de progresso — use o método de página única e controle o loop manualmente:

```python
page_token = None
while True:
    pagina = client.sales.history(start_date=1700000000000, page_token=page_token)

    for venda in pagina.items:
        processar(venda)

    salvar_checkpoint(page_token)  # efeito colateral por página

    if not pagina.page_info or not pagina.page_info.next_page_token:
        break
    page_token = pagina.page_info.next_page_token
```

Use `*_autopaginate` quando precisar apenas iterar todos os registros. Use o loop manual quando precisar agir entre páginas.

---

## Modo Sandbox

Use `sandbox=True` para apontar todas as requisições para o ambiente sandbox da Hotmart. Credenciais de produção e sandbox não são intercambiáveis — gere as credenciais sandbox no painel da Hotmart na mesma seção de Credenciais de Desenvolvedor, selecionando "Sandbox" como ambiente.

```python
from hotmart import Hotmart

client = Hotmart(
    client_id="seu_client_id_sandbox",
    client_secret="seu_client_secret_sandbox",
    basic="Basic suas_credenciais_sandbox_base64",
    sandbox=True,
)
```

> **Observação:** Alguns endpoints se comportam de forma diferente ou não são totalmente suportados no sandbox. Consulte o [SANDBOX-GUIDE.md](SANDBOX-GUIDE.md) e o [HOTMART-API-BUGS.md](HOTMART-API-BUGS.md) para problemas conhecidos.

---

## Tratamento de Erros

Todos os erros do SDK herdam de `HotmartError`. Importe e capture apenas as exceções que você precisa:

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

try:
    pagina = client.sales.history()
except AuthenticationError:
    print("Verifique suas credenciais.")
except RateLimitError as e:
    print(f"Limite de requisições atingido. Tente novamente em {e.retry_after} segundos.")
except NotFoundError:
    print("Recurso não encontrado.")
except HotmartError as e:
    print(f"Erro da API: {e}")
```

Hierarquia de exceções:

| Exceção | Status HTTP | Significado |
|---------|------------|-------------|
| `AuthenticationError` | 401, 403 | Credenciais inválidas ou ausentes |
| `BadRequestError` | 400 | Parâmetros inválidos |
| `NotFoundError` | 404 | Recurso não encontrado |
| `RateLimitError` | 429 | Limite de requisições excedido (500 req/min) |
| `InternalServerError` | 500, 502, 503 | Erro interno do servidor Hotmart |
| `APIStatusError` | outros | Status HTTP inesperado |
| `HotmartError` | — | Classe base para todos os erros do SDK |

### Comportamento de retentativas

Nem todos os erros são tratados da mesma forma — o SDK age diferente antes de lançar cada um:

| Comportamento | Exceções |
|---------------|---------|
| **Reprocessado com backoff exponencial** — lançado apenas após esgotar todas as tentativas | `RateLimitError` (429), `InternalServerError` (500, 502, 503) |
| **Dispara renovação de token + uma nova tentativa automática** — nunca lançado por token expirado | `AuthenticationError` originado de 401 |
| **Lançado imediatamente, sem retentativa** | `BadRequestError` (400), `AuthenticationError` de 403, `NotFoundError` (404), `APIStatusError` |

Na prática: um `RateLimitError` no seu `except` significa que a Hotmart continuou retornando 429 mesmo após todas as tentativas. Um `AuthenticationError` indica credenciais genuinamente inválidas — não simplesmente um token expirado no meio da execução.

Fórmula do backoff: `0.5s × 2^attempt + jitter` (jitter 0–0.5s, cap 30s). Para 429, o header `RateLimit-Reset` é usado diretamente quando presente. Configure o número de tentativas via `max_retries`:

```python
client = Hotmart(..., max_retries=5)
```

---

## Logging

O logging é desabilitado por padrão. Habilite-o passando `log_level` na inicialização:

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

| Nível | O que é registrado |
|-------|-------------------|
| `logging.DEBUG` | URLs das requisições, parâmetros — **contém dados sensíveis, evite em produção** |
| `logging.INFO` | Resumos de operações em alto nível |
| `logging.WARNING` | Avisos e condições inesperadas |
| `logging.ERROR` | Erros durante interações com a API |
| `logging.CRITICAL` | Falhas críticas |

Tokens e credenciais são mascarados em toda saída de log.

---

## Gerenciador de Contexto

`Hotmart` suporta o protocolo de gerenciador de contexto para limpeza automática do pool de conexões HTTP:

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

## Parâmetros Extras (kwargs)

Todos os métodos de recursos aceitam `**kwargs` e repassam os argumentos diretamente para a API como query params. Isso permite usar parâmetros não documentados ou recentemente adicionados pela Hotmart sem aguardar atualizações do SDK:

```python
# Passe qualquer query param que a Hotmart suporte, mesmo sem estar na assinatura do método
pagina = client.sales.history(parametro_novo="valor")
```

---

## Contribuindo

Contribuições são bem-vindas. Veja o [CONTRIBUTING-ptBR.md](CONTRIBUTING-ptBR.md) para configuração do ambiente, estilo de código, como adicionar um novo endpoint e o checklist de PR.

---

## Licença

Apache License 2.0 — veja [LICENSE.txt](../LICENSE.txt) para detalhes.

Este pacote não é afiliado nem oficialmente suportado pela Hotmart.
