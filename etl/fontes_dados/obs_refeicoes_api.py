import gspread
from google.oauth2.service_account import Credentials
from typing import Any, List, Dict

from etl.utils.config import GOOGLE_CREDENTIALS_PATH

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SHEET_ID = '1HUnVGxkhkwRcynG4ED3JyCIFYGTr01dchZDEz94mCYc'  
SHEET_NAME = 'OBS_REFEICOES'


def fetch_obs_refeicao_data() -> List[Dict[Any, Any]]:
    try:
        creds = Credentials.from_service_account_file(
            GOOGLE_CREDENTIALS_PATH,
            scopes=SCOPES
        )
        client = gspread.authorize(creds)

        sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

        data = sheet.get_all_records()

        return data

    except gspread.exceptions.SpreadsheetNotFound:
        print("[!] Erro: Planilha não encontrada. Verifique o SHEET_ID.")
        return []
    except gspread.exceptions.WorksheetNotFound:
        print(f"[!] Erro: Aba '{SHEET_NAME}' não encontrada na planilha.")
        return []
    except FileNotFoundError:
        print(f"[!] Erro: Arquivo de credenciais não encontrado em {GOOGLE_CREDENTIALS_PATH}.")
        return []
    except Exception as e:
        print(f"[!] Erro inesperado: {e}")
        return []