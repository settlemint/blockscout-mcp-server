from typing import Annotated, Dict
from pydantic import Field
from blockscout_mcp_server.tools.common import make_blockscout_request, get_blockscout_base_url

async def get_block_info(
    chain_id: Annotated[str, Field(description="The ID of the blockchain")],
    number_or_hash: Annotated[str, Field(description="Block number or hash")]
) -> Dict:
    """
    Get block information like timestamp, gas used, burnt fees, transaction count etc.
    """
    api_path = f"/api/v2/blocks/{number_or_hash}"
    base_url = await get_blockscout_base_url(chain_id)
    response_data = await make_blockscout_request(base_url=base_url, api_path=api_path)
    return response_data

async def get_latest_block(
    chain_id: Annotated[str, Field(description="The ID of the blockchain")]
) -> Dict:
    """
    Get the latest indexed block number and timestamp, which represents the most recent state of the blockchain. 
    No transactions or token transfers can exist beyond this point, making it useful as a reference timestamp for other API calls.
    """
    api_path = "/api/v2/main-page/blocks"
    base_url = await get_blockscout_base_url(chain_id)
    response_data = await make_blockscout_request(base_url=base_url, api_path=api_path)
    
    # The API returns a list. Extract data from the first item as per responseTemplate
    if response_data and isinstance(response_data, list) and len(response_data) > 0:
        first_block = response_data[0]
        return {
            "block_number": first_block.get("height"),
            "timestamp": first_block.get("timestamp")
        }
    
    # Return empty values if no data is available
    return {"block_number": None, "timestamp": None} 