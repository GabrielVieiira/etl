import hashlib
from datetime import datetime
from .config import IFRACTAL_API_URL

def get_ifractal_token()->str:
    today = datetime.today().strftime("%d/%m/%Y")
    token_string = f"{IFRACTAL_API_URL}{today}"
    return hashlib.sha256(token_string.encode()).hexdigest()