from typing import Annotated
from pydantic import Field
from blockscout_mcp_server.tools.common import make_bens_request


async def get_address_by_ens_name(
    name: Annotated[str, Field(description="ENS domain name to resolve")]
) -> dict:
    """
    Useful for when you need to convert an ENS domain name (e.g. "blockscout.eth")
    to its corresponding Ethereum address.
    """
    api_path = f"/api/v1/1/domains/{name}"
    response_data = await make_bens_request(api_path=api_path)

    # Extract data as per responseTemplate: {"resolved_address": "{{.resolved_address.hash}}"}
    resolved_address_info = response_data.get("resolved_address", {})
    address_hash = resolved_address_info.get("hash")

    return {"resolved_address": address_hash} 