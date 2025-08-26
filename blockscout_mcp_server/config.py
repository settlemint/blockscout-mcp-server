from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerConfig(BaseSettings):
    # Load environment variables from a local .env file (current working directory)
    # and require the BLOCKSCOUT_ prefix for all settings
    model_config = SettingsConfigDict(env_prefix="BLOCKSCOUT_", env_file=".env", env_file_encoding="utf-8")

    bs_api_key: str = ""  # Default to empty, can be set via env
    bs_timeout: float = 120.0  # Default timeout in seconds
    bs_request_max_retries: int = 3  # Conservative retries for transient transport errors

    bens_url: str = "https://bens.services.blockscout.com"  # Add this now for Phase 2
    bens_timeout: float = 30.0  # Default timeout for BENS requests

    chainscout_url: str = "https://chains.blockscout.com"  # Updated to https
    chainscout_timeout: float = 15.0  # Default timeout for Chainscout requests

    # Metadata service configuration
    metadata_url: str = "https://metadata.services.blockscout.com"
    metadata_timeout: float = 30.0

    chain_cache_ttl_seconds: int = 1800  # Default 30 minutes
    chains_list_ttl_seconds: int = 300  # Default 5 minutes
    progress_interval_seconds: float = 15.0  # Default interval for periodic progress updates

    contracts_cache_max_number: int = 10  # Default 10 contracts
    contracts_cache_ttl_seconds: int = 3600  # Default 1 hour

    nft_page_size: int = 10
    logs_page_size: int = 10
    advanced_filters_page_size: int = 10

    # RPC connection pool configuration
    rpc_request_timeout: float = 60.0
    rpc_pool_per_host: int = 50

    # Base name used in the User-Agent header sent to Blockscout RPC
    mcp_user_agent: str = "Blockscout MCP"

    # Analytics configuration
    mixpanel_token: str = ""
    mixpanel_api_host: str = ""  # Optional custom API host (e.g., EU region)

    # Composite client name configuration
    intermediary_header: str = "Blockscout-MCP-Intermediary"
    intermediary_allowlist: str = "ClaudeDesktop,HigressPlugin"
    
    # SettleMint custom deployment configuration
    settlemint_chain_id: str = ""
    settlemint_blockscout_url: str = ""
    settlemint_rpc_url: str = ""


config = ServerConfig()
