from typing import Annotated, Dict
from pydantic import Field
from blockscout_mcp_server.tools.common import make_blockscout_request

async def get_contract_abi(
    address: Annotated[str, Field(description="Smart contract address")]
) -> Dict:
    """
    Get smart contract ABI (Application Binary Interface).
    An ABI defines all functions, events, their parameters, and return types. The ABI is required to format function calls or interpret contract data.
    """
    api_path = f"/api/v2/smart-contracts/{address}"
    
    response_data = await make_blockscout_request(api_path=api_path)
    
    # Extract the ABI from the response as per responseTemplate: {"abi": "{{.abi}}"}
    return {"abi": response_data.get("abi")} 