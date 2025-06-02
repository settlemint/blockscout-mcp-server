from typing import Annotated, List, Dict
from pydantic import Field
from blockscout_mcp_server.tools.common import make_blockscout_request

async def lookup_token_by_symbol(
    symbol: Annotated[str, Field(description="Token symbol or name to search for")]
) -> List[Dict]:
    """
    Search for token addresses by symbol or name. Returns multiple potential matches based on symbol or token name similarity.
    """
    api_path = "/api/v2/search"
    params = {"q": symbol}
    
    response_data = await make_blockscout_request(api_path=api_path, params=params)
    
    # Extract and format items from the response
    items = response_data.get("items", [])
    formatted_items = []
    
    for item in items:
        formatted_item = {
            "address": item.get("address_hash", ""),
            "name": item.get("name", ""),
            "symbol": item.get("symbol", ""),
            "token_type": item.get("token_type", ""),
            "total_supply": item.get("total_supply", ""),
            "circulating_market_cap": item.get("circulating_market_cap", ""),
            "exchange_rate": item.get("exchange_rate", ""),
            "is_smart_contract_verified": item.get("is_smart_contract_verified", False),
            "is_verified_via_admin_panel": item.get("is_verified_via_admin_panel", False)
        }
        formatted_items.append(formatted_item)
    
    return formatted_items 