from typing import Annotated, Dict
from pydantic import Field
from blockscout_mcp_server.tools.common import make_blockscout_request

async def get_block_info(
    number_or_hash: Annotated[str, Field(description="Block number or hash")]
) -> Dict:
    """
    Get block information like timestamp, gas used, burnt fees, transaction count etc.
    """
    api_path = f"/api/v2/blocks/{number_or_hash}"
    response_data = await make_blockscout_request(api_path=api_path)
    return response_data

async def get_latest_block() -> Dict:
    """
    Get the latest indexed block number and timestamp, which represents the most recent state of the blockchain. 
    No transactions or token transfers can exist beyond this point, making it useful as a reference timestamp for other API calls.
    """
    api_path = "/api/v2/main-page/blocks"
    response_data = await make_blockscout_request(api_path=api_path)
    
    # The API returns a list. Extract data from the first item as per responseTemplate
    if response_data and isinstance(response_data, list) and len(response_data) > 0:
        first_block = response_data[0]
        return {
            "block_number": first_block.get("height"),
            "timestamp": first_block.get("timestamp")
        }
    
    # Return empty values if no data is available
    return {"block_number": None, "timestamp": None} 