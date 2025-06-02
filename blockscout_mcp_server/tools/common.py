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
    """
    async with httpx.AsyncClient() as client:
        if params is None:
            params = {}
        if config.bs_api_key:
            params["apikey"] = config.bs_api_key

        url = f"{config.bs_url}{api_path}"
        response = await client.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json() 