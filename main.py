#========================================================================================================================================================================
# Bibliotecas
#========================================================================================================================================================================

import pandas as pd
import requests
import dotenv
import os
import json
from datetime import datetime
from urllib.parse import urljoin
import logging

#========================================================================================================================================================================
# Logger
#========================================================================================================================================================================
logger = logging.getLogger(__name__)

#========================================================================================================================================================================
# Carregando as variáveis do arquivo .env
#========================================================================================================================================================================
dotenv.load_dotenv(override=True)

api_url = os.getenv('API_URL')
api_username = os.getenv('API_USERNAME')
api_password = os.getenv('API_PASSWORD')


#========================================================================================================================================================================
# Variáveis globais
#========================================================================================================================================================================
timeout = 10

#========================================================================================================================================================================
# Iniciando a sessão
#========================================================================================================================================================================
def iniciar_sessao():
    session_payload = {
        "nome": api_username,
        "password": api_password
    }

    auth_headers = {
        "Content-Type": "application/json"
    }

    session_url = urljoin(api_url, "sessions")
    try:
        response = requests.request(
                method="POST",
                url=session_url,
                headers=auth_headers,
                json = session_payload, 
                timeout = timeout
            )
        
        response.raise_for_status() # Verifica se a resposta foi bem-sucedida (status code 200-299)
        
        #Recuperar o cookie de autenticação
        auth_cookie = response.cookies.get("userId")
        
        if not auth_cookie:
            logger.error("Cookie de autenticação não encontrado na resposta.")
            return None # Indica que houve um erro ao iniciar a sessão
        
        logger.info("Sessão iniciada com sucesso.") # Log de sucesso
        
        return {"Cookie": f"userId={auth_cookie}"} # Retorna o cookie de autenticação para uso em outras requisições
    
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"Erro HTTP ao logar: {http_err}")
    except Exception as err:
        logger.error(f"Erro inesperado no login: {err}")
    
    return None 
    
    #=========================================================================================================================================================================
    # Executar iniciar_sessao
    #=========================================================================================================================================================================
if __name__ == "__main__":
    headers_autenticados = iniciar_sessao()
    if headers_autenticados:
        # Agora você pode usar 'headers_autenticados' em qualquer requests.get()
        logger.info("Pronto para extrair dados.")
    else:
        logger.error("Finalizando script devido a falha na autenticação.")