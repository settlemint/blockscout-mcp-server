from typing import Annotated, Optional
from pydantic import Field
from blockscout_mcp_server.tools.common import make_blockscout_request


async def get_transactions_by_address(
    address: Annotated[str, Field(description="Address which either sender or receiver of the transaction")],
    age_from: Annotated[Optional[str], Field(description="Start date and time (e.g 2025-05-22T23:00:00.00Z).")] = None,
    age_to: Annotated[Optional[str], Field(description="End date and time (e.g 2025-05-22T22:30:00.00Z).")] = None,
    methods: Annotated[Optional[str], Field(description="A method signature to filter transactions by (e.g 0x304e6ade)")] = None
) -> dict:
    """
    Get transactions for an address within a specific time range.
    Use cases:
      - `get_transactions_by_address(address, age_from)` - get all transactions to/from the address since the given date up to the current time
      - `get_transactions_by_address(address, age_from, age_to)` - get all transactions to/from the address between the given dates
      - `get_transactions_by_address(address, age_from, age_to, methods)` - get all transactions to/from the address between the given dates and invoking the given method signature
    Manipulating `age_from` and `age_to` allows you to paginate through results by time ranges.
    """
    api_path = "/api/v2/advanced-filters"
    query_params = {
        "to_address_hashes_to_include": address,
        "from_address_hashes_to_include": address
    }
    if age_from:
        query_params["age_from"] = age_from
    if age_to:
        query_params["age_to"] = age_to
    if methods:
        query_params["methods"] = methods

    response_data = await make_blockscout_request(api_path=api_path, params=query_params)
    return response_data 