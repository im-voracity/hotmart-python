# Hotmart API — Bugs & Inconsistências Documentados

Bugs encontrados durante testes de integração com a API real (março de 2026).
Credenciais usadas: conta de produção (não sandbox).

---

## Bug #1 — `sandbox.hotmart.com` não existe no DNS

**Endpoint:** qualquer endpoint com `sandbox=True`
**Esperado:** requests roteadas para `https://sandbox.hotmart.com/...`
**Observado:** `[Errno -5] No address associated with hostname` — o domínio não tem registro DNS
**Impacto:** Ambiente sandbox completamente inacessível. Qualquer desenvolvedor que tente usar `sandbox=True` recebe erro de conexão imediatamente.
**Reprodução:**
```bash
curl https://sandbox.hotmart.com/payments/api/v1/sales/history
# curl: (6) Could not resolve host: sandbox.hotmart.com
```

---

## Bug #2 — `subscriptions.list(status="CANCELLED_BY_BUYER")` retorna HTTP 400

**Endpoint:** `GET /payments/api/v1/subscriptions?status=CANCELLED_BY_BUYER`
**Esperado:** Lista de assinaturas canceladas pelo comprador (ou lista vazia)
**Observado:** `HTTP 400 invalid_parameter`
**Outros status testados:** `ACTIVE`, `CANCELLED_BY_SELLER` → funcionam normalmente
**Impacto:** Impossível filtrar assinaturas canceladas pelo comprador via API.
**Reprodução:**
```bash
curl "https://developers.hotmart.com/payments/api/v1/subscriptions?status=CANCELLED_BY_BUYER" \
  -H "Authorization: Bearer $TOKEN"
# {"error":"invalid_parameter","error_description":"The request was unacceptable..."}
```

---

## Bug #3 — `products.plans(ucode)` retorna HTTP 400 para produtos sem planos

**Endpoint:** `GET /products/api/v1/products/{ucode}/plans`
**Esperado:** Lista vazia `{"items": []}` quando o produto não possui planos
**Observado:** `HTTP 400 invalid_parameter`
**Testado em:** 2 produtos diferentes — ambos retornaram 400
**Impacto:** Impossível distinguir "produto sem planos" de "requisição inválida".
**Reprodução:**
```bash
curl "https://developers.hotmart.com/products/api/v1/products/{ucode}/plans" \
  -H "Authorization: Bearer $TOKEN"
# {"error":"invalid_parameter","error_description":"The request was unacceptable..."}
```

---

## Bug #4 — `coupons.list(product_id)` retorna HTTP 200 com body vazio

**Endpoint:** `GET /payments/api/v1/coupon/product/{product_id}`
**Esperado:** `{"items": [], "page_info": {...}}` quando não há cupons
**Observado:** HTTP 200 com body completamente vazio (não é JSON válido)
**Impacto:** Clientes que fazem `response.json()` recebem erro de parsing. Nossa SDK trata com `model_validate({})` como workaround.
**Reprodução:**
```bash
curl "https://developers.hotmart.com/payments/api/v1/coupon/product/{product_id}" \
  -H "Authorization: Bearer $TOKEN"
# (resposta vazia — sem body)
```

---

## Bug #5 — Token OAuth retornado em formato não documentado

**Endpoint:** `POST https://api-sec-vlc.hotmart.com/security/oauth/token`
**Esperado:** JWT padrão (string `header.payload.signature`)
**Observado:** JWT comprimido com gzip e depois codificado em base64url + URL-encoding
**Payload do JWT:** contém apenas `exp` e `jti` — sem `sub`, `scope`, ou `client_id`
**Impacto:** Clientes que tentam inspecionar o token (e.g. para verificar escopos) não conseguem sem descompressão prévia.
**Detalhe técnico:**
```python
import urllib.parse, base64, gzip
raw = urllib.parse.unquote(token)
jwt = gzip.decompress(base64.b64decode(raw + "==")).decode()
# eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## Bug #6 — Club API retorna HTTP 200 com body vazio para endpoints de alunos

**Endpoints afetados:**
- `GET /club/api/v1/students`
- `GET /club/api/v1/student/progress`
- `GET /club/api/v1/pages`
- `GET /club/api/v1/membership`

**Esperado:** Lista de alunos / dados de progresso
**Observado:** HTTP 200 com body vazio, mesmo com subdomain válido (`mme10`) que possui 31 membros confirmados no painel
**`club.modules` funciona normalmente** (retornou 11 módulos corretamente)
**Hipótese:** Escopo "Club / Área de Membros" não habilitado nas credenciais, porém a API deveria retornar 401/403 nesse caso — não 200 vazio.
**Impacto:** Impossível determinar se o endpoint está funcionando ou se a credencial não tem acesso.

---

## Resumo para email à Hotmart

| # | Endpoint | HTTP Esperado | HTTP Recebido | Severidade |
|---|----------|---------------|---------------|------------|
| 1 | `sandbox.hotmart.com` (DNS) | resolvível | sem registro DNS | 🔴 Crítico |
| 2 | `subscriptions?status=CANCELLED_BY_BUYER` | 200 | 400 | 🟠 Alto |
| 3 | `products/{ucode}/plans` (sem planos) | 200 `[]` | 400 | 🟠 Alto |
| 4 | `coupon/product/{id}` (sem cupons) | 200 `{"items":[]}` | 200 vazio | 🟡 Médio |
| 5 | Token OAuth formato não documentado | JWT padrão | gzip+base64 JWT | 🟡 Médio |
| 6 | `club/students`, `club/pages` etc. | 200 ou 403 | 200 vazio | 🟡 Médio |
