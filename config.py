from pydantic import BaseSettings


class AzSettings(BaseSettings):
    azure_tenant_id: str
    azure_client_id: str
    azure_client_secret: str
    azure_subscription_id: str
    openai_key:str

    class Config:
        env_file = ".env"
