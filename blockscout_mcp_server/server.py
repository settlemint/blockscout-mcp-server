from mcp.server.fastmcp import FastMCP
from blockscout_mcp_server.tools.block_tools import get_block_info
from blockscout_mcp_server.tools.ens_tools import get_address_by_ens_name
from blockscout_mcp_server.tools.transaction_tools import get_transactions_by_address

mcp = FastMCP(name="blockscout-mcp-server", instructions="Blockscout MCP Server v0.1.0")

# Register the tools
# The name of each tool will be its function name
# The description will be taken from the function's docstring
# The arguments (name, type, description) will be inferred from type hints
mcp.tool()(get_block_info)
mcp.tool()(get_address_by_ens_name)
mcp.tool()(get_transactions_by_address)

def run_server_cli():
    """This function will be called by the script defined in pyproject.toml"""
    mcp.run()

if __name__ == "__main__":
    # This allows running the server directly with `python blockscout_mcp_server/server.py`
    mcp.run() 