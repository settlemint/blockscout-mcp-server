from typing import Annotated, Dict
from pydantic import Field
from blockscout_mcp_server.tools.common import make_blockscout_request, get_blockscout_base_url

async def get_contract_abi(
    chain_id: Annotated[str, Field(description="The ID of the blockchain")],
    address: Annotated[str, Field(description="Smart contract address")]
) -> Dict:
    """
    Get smart contract ABI (Application Binary Interface).
    An ABI defines all functions, events, their parameters, and return types. The ABI is required to format function calls or interpret contract data.
    """
    api_path = f"/api/v2/smart-contracts/{address}"
    
    base_url = await get_blockscout_base_url(chain_id)
    response_data = await make_blockscout_request(base_url=base_url, api_path=api_path)
    
    # Extract the ABI from the response as per responseTemplate: {"abi": "{{.abi}}"}
    return {"abi": response_data.get("abi")} 