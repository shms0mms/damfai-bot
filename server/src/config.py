from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR  = Path(__file__).parent.parent

class AuthData(BaseModel):
    private_key :Path = BASE_DIR  / "src" / "app_auth" / "tokens" / "private_key.pem"
    
    public_key :Path = BASE_DIR  /  "src" / "app_auth"  / "tokens" / "public_key.pem"
    
    algorithm:str = "RS256"

    
    days:int = 7
    

class EnvData(BaseSettings):
    # DB_DATA
    DB_URL:str
    DB_URL_ASYNC:str
    

class EnvGigaChat(BaseSettings):
    # GIGACHAT
    AUTH_KEY_KIRIL:str
    AUTH_KEY_DENIS:str
    SCOPE:str

class TgBotEnv(BaseSettings):
    # TG BOT   
    TOKEN:str
    POSTGRES_DB:str
    POSTGRES_USER:str
    POSTGRES_PASSWORD:str
    SITE_URL:str
    DATABASE_URL:str


class Config(BaseModel):
    
    
    
    gigachat_data:EnvGigaChat = EnvGigaChat()

    auth_data:AuthData = AuthData()

    env_data:EnvData = EnvData()
    
    
config = Config()