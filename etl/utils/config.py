from dotenv import load_dotenv
import os

load_dotenv()

#gambiarra para resolver erro do pylance
def get_env_var(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise ValueError(f'Variável de ambiente {name} não definida')
    return value

IFRACTAL_API_URL: str = get_env_var('IFRACTAL_API_URL')
IFRACTAL_API_USER: str = get_env_var('IFRACTAL_API_USER')
IFRACTAL_API_TOKEN: str = get_env_var('IFRACTAL_API_TOKEN')
DATABASE_URL: str = get_env_var('DATABASE_URL')
GOOGLE_CREDENTIALS_PATH: str = get_env_var('GOOGLE_CREDENTIALS_PATH')