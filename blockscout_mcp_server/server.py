from mcp.server.fastmcp import FastMCP
from blockscout_mcp_server.tools.block_tools import get_block_info, get_latest_block
from blockscout_mcp_server.tools.ens_tools import get_address_by_ens_name
from blockscout_mcp_server.tools.transaction_tools import get_transactions_by_address, get_token_transfers_by_address, transaction_summary, get_transaction_info, get_transaction_logs
from blockscout_mcp_server.tools.get_instructions import __get_instructions__
from blockscout_mcp_server.tools.search_tools import lookup_token_by_symbol
from blockscout_mcp_server.tools.contract_tools import get_contract_abi
from blockscout_mcp_server.tools.address_tools import get_address_info, get_tokens_by_address, nft_tokens_by_address, get_address_logs

mcp = FastMCP(name="blockscout-mcp-server", instructions="Blockscout MCP Server v0.1.0")

# Register the tools
# The name of each tool will be its function name
# The description will be taken from the function's docstring
# The arguments (name, type, description) will be inferred from type hints
mcp.tool()(__get_instructions__)
mcp.tool()(get_block_info)
mcp.tool()(get_latest_block)
mcp.tool()(get_address_by_ens_name)
mcp.tool()(get_transactions_by_address)
mcp.tool()(get_token_transfers_by_address)
mcp.tool()(lookup_token_by_symbol)
mcp.tool()(get_contract_abi)
mcp.tool()(get_address_info)
mcp.tool()(get_tokens_by_address)
mcp.tool()(transaction_summary)
mcp.tool()(nft_tokens_by_address)
mcp.tool()(get_transaction_info)
mcp.tool()(get_transaction_logs)
mcp.tool()(get_address_logs)

def run_server_cli():
    """This function will be called by the script defined in pyproject.toml"""
    mcp.run()

if __name__ == "__main__":
    # This allows running the server directly with `python blockscout_mcp_server/server.py`
    mcp.run() 