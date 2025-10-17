import hashlib
from datetime import datetime
from .config import API_TOKEN_BASE

def get_ifractal_token()->str:
    today = datetime.today().strftime("%d/%m/%Y")
    token_string = f"{API_TOKEN_BASE}{today}"
    return hashlib.sha256(token_string.encode()).hexdigest()