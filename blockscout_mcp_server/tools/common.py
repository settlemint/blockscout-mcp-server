import httpx
import time
import json
from typing import Optional
from blockscout_mcp_server.config import config

class ChainNotFoundError(ValueError):
    """Exception raised when a chain ID cannot be found or resolved to a Blockscout URL."""
    pass

# Cache: chain_id -> (blockscout_url_or_none, expiry_timestamp)
# Note: This cache is simple and not thread-safe for concurrent writes for the same new key.
# This is acceptable for the typical MCP server use case (local, one server per client).
_chain_cache: dict[str, tuple[Optional[str], float]] = {}

async def get_blockscout_base_url(chain_id: str) -> str:
    """
    Fetches the Blockscout base URL for a given chain_id from Chainscout,
    caches it, and handles errors.
    
    Args:
        chain_id: The blockchain chain ID to look up
        
    Returns:
        The Blockscout instance URL for the chain
        
    Raises:
        ChainNotFoundError: If no Blockscout instance is found for the chain
    """
    current_time = time.time()
    cached_entry = _chain_cache.get(chain_id)

    if cached_entry:
        cached_url, expiry_timestamp = cached_entry
        if current_time < expiry_timestamp:
            if cached_url is None:  # Cached "not found"
                raise ChainNotFoundError(
                    f"Blockscout instance hosted by Blockscout team for chain ID '{chain_id}' is unknown (cached)."
                )
            return cached_url
        else:
            _chain_cache.pop(chain_id, None)  # Cache expired

    chain_api_url = f"{config.chainscout_url}/api/chains/{chain_id}"
    
    # Note: We're not using make_chainscout_request here because we need:
    # 1. Custom error handling for different HTTP status codes (like 404)
    # 2. Special caching behavior for error cases
    # 3. Direct access to handle JSON parsing errors
    # 4. Chain-specific context in error messages
    try:
        async with httpx.AsyncClient(timeout=config.chainscout_timeout) as client:
            response = await client.get(chain_api_url)
        response.raise_for_status()
        chain_data = response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            _chain_cache[chain_id] = (None, current_time + config.chain_cache_ttl_seconds)
            raise ChainNotFoundError(f"Chain with ID '{chain_id}' not found on Chainscout.") from e
        raise ChainNotFoundError(f"Error fetching data for chain ID '{chain_id}' from Chainscout: {e}") from e
    except (httpx.RequestError, json.JSONDecodeError) as e:
        raise ChainNotFoundError(f"Could not retrieve or parse data for chain ID '{chain_id}' from Chainscout.") from e

    if not chain_data or "explorers" not in chain_data:
        _chain_cache[chain_id] = (None, current_time + config.chain_cache_ttl_seconds)
        raise ChainNotFoundError(f"No explorer data found for chain ID '{chain_id}' on Chainscout.")

    blockscout_url = None
    for explorer in chain_data.get("explorers", []):
        if isinstance(explorer, dict) and explorer.get("hostedBy") == "blockscout":
            blockscout_url = explorer.get("url")
            if blockscout_url:
                break
    
    expiry = current_time + config.chain_cache_ttl_seconds
    if blockscout_url:
        _chain_cache[chain_id] = (blockscout_url, expiry)
        return blockscout_url.rstrip('/')
    else:
        _chain_cache[chain_id] = (None, expiry)
        raise ChainNotFoundError(
            f"Blockscout instance hosted by Blockscout team for chain ID '{chain_id}' is unknown."
        )

async def make_blockscout_request(base_url: str, api_path: str, params: dict | None = None) -> dict:
    """
    Make a GET request to the Blockscout API.
    
    Args:
        base_url: The base URL of the Blockscout API instance
        api_path: The API path to request, e.g. '/api/v2/blocks/19000000'
        params: Optional query parameters
        
    Returns:
        The JSON response as a dictionary
        
    Raises:
        httpx.HTTPStatusError: If the HTTP request returns an error status code
        httpx.TimeoutException: If the request times out
    """
    async with httpx.AsyncClient(timeout=config.bs_timeout) as client:
        if params is None:
            params = {}
        if config.bs_api_key:
            params["apikey"] = config.bs_api_key

        url = f"{base_url.rstrip('/')}/{api_path.lstrip('/')}"
        response = await client.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()

async def make_bens_request(api_path: str, params: dict | None = None) -> dict:
    """
    Make a GET request to the BENS API.
    
    Args:
        api_path: The API path to request, e.g. '/api/v1/1/domains/blockscout.eth'
        params: Optional query parameters
        
    Returns:
        The JSON response as a dictionary
        
    Raises:
        httpx.HTTPStatusError: If the HTTP request returns an error status code
        httpx.TimeoutException: If the request times out
    """
    async with httpx.AsyncClient(timeout=config.bens_timeout) as client:
        url = f"{config.bens_url}{api_path}"
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()

async def make_chainscout_request(api_path: str, params: dict | None = None) -> dict:
    """
    Make a GET request to the Chainscout API.
    
    Args:
        api_path: The API path to request, e.g. '/api/chains/list'
        params: Optional query parameters
        
    Returns:
        The JSON response as a dictionary
        
    Raises:
        httpx.HTTPStatusError: If the HTTP request returns an error status code
        httpx.TimeoutException: If the request times out
    """
    async with httpx.AsyncClient(timeout=config.chainscout_timeout) as client:
        url = f"{config.chainscout_url}{api_path}"
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json() 