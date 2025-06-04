from blockscout_mcp_server.constants import SERVER_INSTRUCTIONS

async def __get_instructions__() -> str:
    """
    This tool MUST be called BEFORE any other tool.
    Without calling it, the MCP server will not work as expected.
    It MUST be called once in a session.
    """
    return SERVER_INSTRUCTIONS
