# Changelog

Todas as mudanças notáveis neste projeto são documentadas aqui.

O formato segue [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) e o projeto adota [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.3] - 2026-03-26

### Fixed

- Smoke test no pipeline de publish corrigido (PEP 668 — usar venv em vez de `--system`)

---

## [1.0.2] - 2026-03-26

Versão de manutenção com melhorias de documentação. Nenhuma mudança no código da biblioteca.

### Changed

- Aviso de breaking change da v1.0 adicionado ao README
- Seção de documentação com tabela de todos os docs adicionada ao README
- CHANGELOG reescrito com narrativa e contexto histórico
- SANDBOX-GUIDE atualizado com bug conhecido do DNS (`sandbox.hotmart.com`)

---

## [1.0.1] - 2026-03-26

Versão de manutenção com melhorias de documentação. Nenhuma mudança no código da biblioteca.

### Changed

- README movido para a raiz do repositório para renderização correta no GitHub e no PyPI
- README reescrito com seção de features, princípios de design e documentação de DX melhorada
- Adicionados CONTRIBUTING.md (EN) e CONTRIBUTING-ptBR.md (PT-BR)
- `HOTMART_API.md` renomeado para `docs/HOTMART-API-REFERENCE.md`

---

## [1.0.0] - 2026-03-26

**Breaking change.** Esta versão é um rewrite completo da biblioteca — a v1.0 não é compatível com a v0.x. Veja o [guia de migração](MIGRATION.md) para atualizar seu código.

### Por que um rewrite?

A biblioteca ficou cerca de dois anos sem atualizações (a última versão da série v0.x foi publicada em março de 2024). Nesse período, o ecossistema Python evoluiu bastante: `httpx` se consolidou como alternativa moderna ao `requests`, Pydantic v2 trouxe validação muito mais rápida e tipagem mais expressiva, e ferramentas como `uv` e `ruff` tornaram o desenvolvimento consideravelmente mais ágil.

Aproveitamos a oportunidade para redesenhar a API da biblioteca do zero, com foco em developer experience, tipagem estrita e manutenibilidade a longo prazo. A intenção é manter o projeto ativo e atualizado daqui pra frente.

### Added

- API resource-based: `client.sales`, `client.subscriptions`, `client.products`, `client.coupons`, `client.club`, `client.events`, `client.negotiation`
- 27 endpoints da API Hotmart distribuídos em 7 grupos de recursos
- Modelos Pydantic v2 com `extra="allow"` para compatibilidade futura com novos campos da API
- Refresh automático de token com double-checked locking (thread-safe)
- Retry com backoff exponencial em erros transitórios (`max_retries` configurável, padrão 3)
- Controle proativo de rate limit (janela de 500 chamadas/min)
- Logging estruturado com mascaramento de segredos (parâmetro `log_level`)
- Iteradores de autopaginação: todo método paginado tem uma variante `*_autopaginate`
- Modo sandbox via flag `sandbox=True` no construtor
- Suporte a gerenciador de contexto (`with Hotmart(...) as client:`)
- Passthrough de `**kwargs` para parâmetros não documentados ou futuros da API
- Hierarquia de exceções tipadas: `HotmartError`, `AuthenticationError`, `BadRequestError`, `NotFoundError`, `RateLimitError`, `InternalServerError`, `APIStatusError`
- Documentação completa em EN + PT-BR
- Guia de migração da v0.x para v1.0
- Referência completa dos endpoints da API Hotmart em formato legível por agentes de IA (`docs/HOTMART-API-REFERENCE.md`)
- 67 testes unitários (respx, cobertura total dos recursos)
- 30 testes de integração contra a API real (pulados sem credenciais)
- 6 bugs conhecidos da API Hotmart documentados em `docs/HOTMART-API-BUGS.md`

### Changed

- Cliente HTTP migrado de `requests` para `httpx`
- Tooling migrado de `poetry` para `uv` + `hatchling`
- API resource-based substitui métodos planos na classe `Hotmart`
- Import path mudou de `hotmart_python` para `hotmart`
- `cancel_subscription` agora recebe uma lista de códigos (operação em lote)
- Suporte mínimo ao Python elevado de 3.9 para 3.11

### Removed

- Parâmetro `enhance` (todos os métodos)
- Dependência `coloredlogs`
- Decorador `@paginate` (substituído pelos métodos `*_autopaginate`)
- Métodos com nomes planos (`get_sales_history`, `get_subscriptions`, etc.)

---

## [0.5.0] - 2024-03-24

- Refatoração do handling de requisições para sempre retornar lista de dicts
- Adicionado `_handle_response` para saída padronizada
- Adicionado decorador `@paginate`
- Removido método antigo `_paginate`
- Corrigido `subscriber_code` não passado corretamente em `change_due_day`
- Type hints melhorados

---

## [0.4.1] - 2024-03-22

- Melhor tratamento de erros em `_make_request`
- Exceções customizadas removidas
- Testes atualizados

---

## [0.4.0] - 2024-03-21

- Adicionado endpoint de Cupons de Desconto
- Adicionados exemplos de código para sandbox

---

## [0.3.0] - 2024-03-21

- Suporte a Python <3.9 removido
- Adicionados linting com flake8 e GitHub Actions

---

## [0.2.2] - 2024-03-21

- Refatoração de métodos auxiliares para tratamento de erros
- Corrigida saída de paginação para retornar lista de dicts

---

## [0.2.1] - 2024-03-20

- Adicionado endpoint de assinaturas
- `get_sales_users` renomeado para `get_sales_participants`
- Migração para Poetry

---

## [0.1.x] - 2024-01-31 a 2024-03-18

- Versões iniciais de desenvolvimento e publicações de teste no PyPI
- Implementação inicial do wrapper com endpoints de vendas básicos
- Autenticação OAuth 2.0
- Logs coloridos via `coloredlogs`
