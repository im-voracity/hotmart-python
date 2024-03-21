# Hotmart Python

Esse é um Wrapper desenvolvido em Python para a API da Hotmart que permite interagir com os recursos oferecidos pela API
Oficial da plataforma.:

**Note**: The english docs is available [here](README.md).

## Índice

- [Funcionalidades](#funcionalidades)
- [Instalação](#instalção)
- [Uso](#uso)
- [Parâmetros suportados](#parâmetros-suportados)
- [Referência da API](#referência-da-api)
- [Contribuição](#contribuição)
- [License](#license)

## Funcionalidades:

- ✅ Autenticação
- ✅ Todos os parâmetros de URL são suportados
- Vendas
    - ✅ Histórico de vendas
    - ✅ Sumário de vendas
    - ✅ Participantes de vendas
    - ✅ Comissões de vendas
    - ✅ Detalhamento de preços de vendas

- Assinaturas
    - ✅ Obter assinaturas
    - ✅ Sumário de assinaturas
    - ✅ Obter compras de assinantes
    - ✅ Cancelar assinatura
    - ✅ Reativar e cobrar assinatura

## Instalção

```bash
pip install hotmart_python
```

## Uso

Abaixo está um exmeplo de como usar a biblioteca Hotmart Python em seu código:

```python
from hotmart_python import Hotmart

# Inicialize o cliente da Hotmart
hotmart = Hotmart(client_id='your_client_id',
                  client_secret='your_client_secret',
                  basic='your_basic_token')

# Exemplo de uso: Obter histórico de vendas
sales_history = hotmart.get_sales_history()
print(sales_history)
```

Por padrão, os logs são desabilitados. Você pode ativá-los e configurar o nível dos logs passando o
parâmetro `log_level` quando inicializar a classe Hotmart. Os níveis de logs disponíveis são:

- ️️☣️ `logging.DEBUG`: Logs para debug, que inclui informações detalhadas como URLs de solicitações (requests),
  parâmetros de URL e itens do body (**não recomendado para uso em produção devido a informações sensíveis serem
  logadas**).
- `logging.INFO`: Logs de informação, permitem a visualização de informações simples sobre as configurações da classe.
- `logging.WARNING`: Logs de aviso, indicam potenciais problemas ou comportamentos inesperados.
- `logging.ERROR`: Logs de erro, indicam quando erros ocorrem durante a interação com a API.
- `logging.CRITICAL`: Logs críticos, indicam erros críticos que podem impedir o funcionamento esperado.

```python
import logging
from hotmart_python import Hotmart

# Inicialize o cliente da Hotmart
hotmart = Hotmart(client_id='your_client_id',
                  client_secret='your_client_secret',
                  basic='your_basic_token',
                  log_level=logging.INFO)
```

Você também pode usar o parâmetro `sandbox` para ativar o modo Sandbox, que deve ser criado préviamente usando as
credenciais Hotmart. Por padrão, o modo sandbox é desabilitado.

```python
import logging
from hotmart_python import Hotmart

# Inicialize o cliente da Hotmart
hotmart = Hotmart(client_id='your_sandbox_client_id',
                  client_secret='your_sandbox_client_secret',
                  basic='your_sandbox_basic_token',
                  log_level=logging.INFO,
                  sandbox=True)
```

Exemplo de uso: Obter histórico de vendas com logs ativados e configurados para nível "INFO", filtrando por e-mail do
comprador:

```python
from hotmart_python import Hotmart
import logging

# Initialize the Hotmart client with logging enabled and log level set to DEBUG
hotmart = Hotmart(client_id='your_client_id',
                  client_secret='your_client_secret',
                  basic='your_basic',
                  log_level=logging.INFO)

# Example usage: Get sales history
sales_history = hotmart.get_sales_history(buyer_email='johndoe@example.com')
print(sales_history)
```

## Parâmetros Suportados

Pelo formato de desenvolvimento da biblioteca, todos os parâmetros (tanto de URL quando de body) devem ser suportados
por padrão, eles deverão ser passados como argumentos de palavra-chave (`**kwargs`) para os métodos.

Esses são alguns dos parâmetros suportados pela classe `Hotmart`:

- `paginate` (`bool`): Se deve paginar os resultados ou não (o padrão é `False`). Quando definido como `True`, o método
  irá buscar todas as páginas de dados para um endpoint paginado.
- `kwargs`: Quaisquer consultas suportadas pelo endpoint. Por exemplo, o método `get_sales_history` suporta os seguintes
  parâmetros:
    - `max_results` (`int`): O número máximo de itens por página que podem ser retornados.
    - `product_id` (`int`): Identificador único (ID) do produto vendido (número de 7 dígitos).
    - `start_date` (`int`): Data de início do período de filtragem. A data deve estar em milissegundos, começando em
      01/01/1970 00:00:00 UTC.
    - `end_date` (`int`): Data final do período de filtro. A data deve estar em milissegundos, começando em 01-01-1970
      00:00:00 UTC.
    - `sales_source` (`str`): Código SRC utilizado no link da página de pagamento do produto para rastreamento da
      origem. (
      Por exemplo: `pay.hotmart.com/B00000000T?src=campaignname`)
    - `buyer_name` (`str`): Nome do comprador.
    - `buyer_email` (`str`): Endereço de e-mail do comprador. Você pode usar essas informações para pesquisar compras
      específicas.
    - `product_id` (`str`): O ID do produto.
    - `transaction` (`str`): Código de referência exclusivo para uma transação, por exemplo, HP17715690036014. Uma
      transação acontece quando um pedido é feito. Um pedido pode ser um boleto bancário gerado, uma compra aprovada, um
      pagamento recorrente e mais.
    - `transaction_status` (`str`): O status da compra (Por exemplo: 'approved', 'pending', 'refunded', 'canceled', '
      chargeback').
    - E outros.

Para mais informações sobre consultas ou parâmetros, consulte
a [documentação da API da Hotmart](https://developers.hotmart.com/docs/en/).

## Referência da API

Aqui está uma breve visão geral dos métodos suportados pela classe `Hotmart`:

- `get_sales_history(**kwargs)`: Recupera o histórico de vendas. Aceita argumentos de palavras-chave opcionais para
  filtrar o resultados. [Referência](https://developers.hotmart.com/docs/pt-BR/v1/sales/sales-history/)

- `get_sales_summary(**kwargs)`: Recupera o resumo de vendas. Aceita argumentos de palavras-chave opcionais para filtrar
  os resultados. [Referência](https://developers.hotmart.com/docs/pt-BR/v1/sales/sales-summary/)

- `get_sales_participants(**kwargs)`: Recupera os participantes de vendas. Aceita argumentos de palavras-chave opcionais
  para filtrar os resultados. [Referência](https://developers.hotmart.com/docs/pt-BR/v1/sales/sales-users/)

- `get_sales_commissions(**kwargs)`: Recupera as comissões de vendas. Aceita argumentos de palavras-chave opcionais para
  filtrar os resultados. [Referência](https://developers.hotmart.com/docs/pt-BR/v1/sales/sales-commissions/)

- `get_sales_price_details(**kwargs)`: Recupera os detalhes do preço de venda. Aceita argumentos de palavras-chave
  opcionais para filtrar os
  resultados. [Referência](https://developers.hotmart.com/docs/pt-BR/v1/sales/sales-price-details/)

- `get_subscriptions(paginate=False, **kwargs)`: Recupera as assinaturas. Aceita um argumento opcional `paginate` e
  argumentos adicionais de palavras-chave para filtrar os
  resultados. [Referência](https://developers.hotmart.com/docs/pt-BR/v1/subscription/get-subscribers/)

- `get_subscription_summary(paginate=False, **kwargs)`: Recupera o sumário da assinatura. Aceita um argumento
  opcional `paginate` e argumentos de palavras-chave adicionais para filtrar os
  resultados. [Referência](https://developers.hotmart.com/docs/pt-BR/v1/subscription/get-subscription-summary/)

- `get_subscription_purchases(subscriber_code, paginate=False, **kwargs)`: Recupera as compras de assinatura para um
  assinante específico. Requer um argumento `subscriber_code` e aceita um argumento opcional `paginate` argumentos de
  palavra-chave adicionais para filtrar os
  resultados. [Referência](https://developers.hotmart.com/docs/pt-BR/v1/subscription/get-subscription-purchases/)

- `cancel_subscription(subscriber_code, send_email=True)`: Cancela uma assinatura. Requer um argumento `subscriber_code`
  e aceita um `send_email` como argumento
  opcional. [Referência](https://developers.hotmart.com/docs/pt-BR/v1/subscription/cancel-subscriptions/)

- `reactivate_and_charge_subscription(subscriber_code, charge=True)`: Reativa e cobra uma assinatura. Requer um
  argumento `subscriber_code` e aceita um argumento
  opcional `charge`. [Referência](https://developers.hotmart.com/docs/pt-BR/v1/subscription/reactivate-subscription/)

Para uma informação mais detalhada sobre os endpoints aos quais esses métodos se referem e os parâmetros aceitos, por
favor, visite
[documentação oficial da API da Hotmart](https://developers.hotmart.com/docs/pt-BR/).

## Contribuição

Contribuições são bem-vindas! Para contribuir com este projeto, por favor, leia
o [guia de contribuição](CONTRIBUTING.md) (disponível somente em inglês) para saber como começar.

## Licença

This project is licensed under the Apache License 2.0 - see the [LICENSE](../LICENSE.txt) file for details.

This package is not affiliated with Hotmart. It is an open-source project that is not officially supported by Hotmart.
