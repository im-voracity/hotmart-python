# Hotmart Python

Este é um Wrapper Python para a API da Hotmart, que permite interagir com os recursos oferecidos pela plataforma:

## Funcionalidades:

- ✅ Autenticação
- ✅ Todos os filtros de Query são suportados
- ✅ Todos os endpoints de vendas
    - ✅ Histórico de vendas
    - ✅ Sumário de vendas
    - ✅ Participantes de vendas
    - ✅ Comissões de vendas
    - ✅ Detalhamentos de preços de vendas
    - ✅ Reembolso de vendas

- ⚠️ Endpoints de Assinaturas (Ainda não completo)
    - ✅ Obter assinaturas
    - ❌ Sumário de assinaturas
    - ❌ Obter compras de assinantes
    - ❌ Cancelar assinatura
    - ❌ Cancelar lista de assinaturas
    - ❌ Reativar e cobrar assinatura
    - ❌ Reativar e cobrar lista de assinaturas
    - ❌ Alterar dia de cobrança

## Roadmap

- 💡 Endpoints da **área de membros**
- 💡 Endpoints de **cupons de desconto**

## Instalação

```bash
pip install hotmart_python
```

## Uso

Abaixo temos um exemplo de implementação para obter o histórico de vendas:

```python
from hotmart_python import Hotmart

# Inicialize o cliente da Hotmart
hotmart = Hotmart(client_id='your_client_id',
                  client_secret='your_client_secret',
                  basic='your_basic_token')

# Exemplo de uso: Histórico de vendas
sales_history = hotmart.get_sales_history()
print(sales_history)
```

Por padrão, os logs são desativados. Você pode habilitar e ver o nível de log através do argumento `log_level`. As
possíveis opções de nível de log são:

- ️️☣️ `logging.DEBUG`: O nível de debug, que contém a maior quantidade de informações, que inclui informações
  detalhadas
  como as URLs utilizadas nas solicitações e os parâmetros que estão sendo utilizados(**Não recomendado para produção
  pois informações sensíveis como tokens de acesso são logadas no console**).
- `logging.INFO`: O nível de informações, que traz informações básicas sobre as operações sendo executadas.
- `logging.WARNING`: O nível de aviso, que indica problemas em potencial ou comportamento inesperado.
- `logging.ERROR`: O nível de erro, que indica somente os erros ou problemas críticos que ocorrem durante a interação
  com a API.
- `logging.CRITICAL` (Padrão): O nível crítico, que irá logar somente problemas que precisam de atenção imediata e
  impedem o funcionamento do programa.

```python
from hotmart_python import Hotmart
import logging

# Inicializa o cliente da hotmart com os logs ativados e o log_level configurado para logging.DEBUG
hotmart = Hotmart(client_id='your_client_id',
                  client_secret='your_client_secret',
                  basic='your_basic',
                  log_level=logging.DEBUG)

# Exemplo de uso: Histórico de vendas, filtrado pelo email do comprador
sales_history = hotmart.get_sales_history(buyer_email='johndoe@example.com')
print(sales_history)
```

## Parâmetros suportados

Estes são os parâmetros suportados para todos os métodos que interagem com a API da Hotmart:

- `paginate` (bool): Se deve paginar os resultados ou não (o padrão é False). Quando definido como True, o método irá
  buscar todas as páginas de dados para um ponto de extremidade paginado.
- `kwargs`: Quaisquer consultas suportadas pelo ponto de extremidade. Por exemplo, o método `get_sales_history` suporta
  os seguintes parâmetros:
    - `max_results` (int): O número máximo de itens por página que podem ser retornados.
    - `product_id` (int): Identificador único (ID) do produto vendido (número de 7 dígitos).
    - `start_date` (int): Data de início do período de filtro. A data deve estar em milissegundos, começando em
      1970-01-01 00:00:00 UTC.
    - `end_date` (int): Data de término do período de filtro. A data deve estar em milissegundos, começando em
      1970-01-01 00:00:00 UTC.
    - `sales_source` (str): Código SRC usado no link na página de pagamento do produto para rastrear a origem. (Por
      exemplo, `pay.hotmart.com/B00000000T?src=campaignname`)
    - `buyer_name` (str): Nome do comprador.
    - `buyer_email` (str): Endereço de e-mail do comprador. Você pode usar essa informação para procurar compras
      específicas.
    - `product_id` (str): O ID do produto.
    - `transaction` (str): Código de referência único para uma transação, por exemplo, HP17715690036014. Uma transação
      acontece quando um pedido é feito. Um pedido pode ser um boleto bancário gerado, uma compra aprovada, um pagamento
      recorrente, e mais.
    - `transaction_status` (str): O status da venda (por exemplo, 'aprovado', 'pendente', 'reembolsado', 'cancelado', '
      chargeback').
    - E outros.

Para mais informações sobre queries/filtros, por favor, veja
a [Documentação oficial da API da Hotmart](https://developers.hotmart.com/docs/pt-BR). Qualquer parâmetro de
query/filtro que é suportado pelo endpoint pode ser passado como um `kwarg` para o método.

## Contribuições

Contribuições são bem-vindas! Se você encontrar algum problema ou tiver sugestões de melhoria, por favor, abra uma issue
ou envie um pull request no repositório do GitHub.

## License
Este projeto está licenciado sob a Licença Apache 2.0 - veja a[LICENÇA](LICENSE.txt) para detalhes.