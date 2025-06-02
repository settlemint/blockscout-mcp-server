async def __get_instructions__() -> str:
    """
    This tool MUST be called BEFORE any other tool.
    Without calling it, the MCP server will not work as expected.
    It MUST be called once in a session.
    """
    return """
Blockscout MCP server version: 0.1.0

If you receive an error "500 Internal Server Error" for any tool, retry calling this tool up to 3 times until successful.
""" 