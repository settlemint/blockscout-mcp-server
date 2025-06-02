import httpx
from blockscout_mcp_server.config import config

async def make_blockscout_request(api_path: str, params: dict | None = None) -> dict:
    """
    Make a GET request to the Blockscout API.
    
    Args:
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

        url = f"{config.bs_url}{api_path}"
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