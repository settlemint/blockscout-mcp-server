from pydantic_settings import BaseSettings

class ServerConfig(BaseSettings):
    bs_url: str = "https://eth.blockscout.com"  # Default value
    bs_api_key: str = ""  # Default to empty, can be set via env

    bens_url: str = "https://bens.services.blockscout.com"  # Add this now for Phase 2

    class Config:
        env_prefix = "BLOCKSCOUT_"  # e.g., BLOCKSCOUT_BS_URL

config = ServerConfig() 