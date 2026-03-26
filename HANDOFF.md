# Handoff — hotmart-python v1.0 SDK Rewrite

## Estado atual

- **Branch de trabalho:** `feature/v1-rewrite`
- **Worktree:** `~/.config/superpowers/worktrees/hotmart-python/v1-rewrite`
- **Tarefa concluída:** Task 1 (pyproject.toml + skeleton) — commit `dac5933`
- **Próxima tarefa:** Task 2 (`_config.py`)

## Arquivos chave

| Arquivo | Descrição |
|---------|-----------|
| `docs/superpowers/plans/2026-03-25-hotmart-sdk-v1-rewrite.md` | **Plano de implementação completo** — 21 tarefas com código completo |
| `docs/superpowers/specs/2026-03-25-hotmart-sdk-rework-design.md` | Design spec |
| `HOTMART_API.md` | Referência de todos os endpoints (source of truth) |

## Como continuar

1. O agente deve usar o skill `superpowers:subagent-driven-development`
2. Ler o plano em `docs/superpowers/plans/2026-03-25-hotmart-sdk-v1-rewrite.md`
3. Tasks 1 já está concluída — continuar da **Task 2** em diante
4. Todo trabalho deve ser feito no worktree: `~/.config/superpowers/worktrees/hotmart-python/v1-rewrite`
5. Commits e pushes após cada task (branch: `feature/v1-rewrite`)

## Regras importantes

- **Sem Co-Authored-By** nos commits
- **Sem nested ifs** — guard clauses e early returns
- **Commits frequentes** — um por task no mínimo
- Código estilo: conforme `docs/superpowers/plans/` (seção "Code style")

## Resumo das 21 tasks

| # | Task | Status |
|---|------|--------|
| 1 | pyproject.toml + skeleton | ✅ Concluída |
| 2 | `_config.py` | ⏳ Próxima |
| 3 | `_exceptions.py` + tests | ⏳ Pendente |
| 4 | `_logging.py` + tests | ⏳ Pendente |
| 5 | `_retry.py` + tests | ⏳ Pendente |
| 6 | `_rate_limit.py` + tests | ⏳ Pendente |
| 7 | `_auth.py` + tests | ⏳ Pendente |
| 8 | `_base_client.py` + tests | ⏳ Pendente |
| 9 | Models — enums, common, pagination | ⏳ Pendente |
| 10 | Domain models — Sales | ⏳ Pendente |
| 11 | Domain models — Subscriptions, Products, Coupons, Club, Events, Negotiation | ⏳ Pendente |
| 12 | `resources/_base.py` | ⏳ Pendente |
| 13 | `resources/sales.py` + tests | ⏳ Pendente |
| 14 | `resources/subscriptions.py` + tests | ⏳ Pendente |
| 15 | `resources/products.py` + tests | ⏳ Pendente |
| 16 | `resources/coupons.py` + tests | ⏳ Pendente |
| 17 | `resources/club.py` + tests | ⏳ Pendente |
| 18 | `resources/events.py` + `resources/negotiation.py` + tests | ⏳ Pendente |
| 19 | `_client.py` + `__init__.py` + `conftest.py` | ⏳ Pendente |
| 20 | Cleanup — remover arquivos antigos | ⏳ Pendente |
| 21 | Documentação (EN + PT-BR) | ⏳ Pendente |
