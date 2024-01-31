import logging
from hotmart import Hotmart
from dotenv import load_dotenv
import os

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carregando variáveis de ambiente
load_dotenv()

client_id = os.getenv('HOTMART_CLIENT_ID')
client_secret = os.getenv('HOTMART_CLIENT_SECRET')
basic = os.getenv('HOTMART_BASIC')

hotmart = Hotmart(client_id=client_id, client_secret=client_secret, basic=basic, sandbox=True, log_level=logging.INFO)

print(hotmart.get_sales_history(paginate=False))
print(hotmart.get_sales_summary(paginate=True))
