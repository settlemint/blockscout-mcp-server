from mcp.server.fastmcp import FastMCP
from blockscout_mcp_server.tools.block_tools import get_block_info

mcp = FastMCP(name="blockscout-mcp-server", instructions="Blockscout MCP Server v0.1.0")

# Register the tool
# The name of the tool will be 'get_block_info' (from the function name)
# The description will be taken from the function's docstring
# The arguments (name, type, description) will be inferred from type hints
mcp.tool()(get_block_info)

def run_server_cli():
    """This function will be called by the script defined in pyproject.toml"""
    mcp.run()

if __name__ == "__main__":
    # This allows running the server directly with `python blockscout_mcp_server/server.py`
    mcp.run() 