from typing import Annotated
from pydantic import Field
from blockscout_mcp_server.tools.common import make_blockscout_request

async def get_block_info(
    number_or_hash: Annotated[str, Field(description="Block number or hash")]
) -> dict:
    """
    Get block information like timestamp, gas used, burnt fees, transaction count etc.
    """
    api_path = f"/api/v2/blocks/{number_or_hash}"
    response_data = await make_blockscout_request(api_path=api_path)
    return response_data 