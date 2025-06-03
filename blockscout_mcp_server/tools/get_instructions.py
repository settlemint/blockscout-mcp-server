async def __get_instructions__() -> str:
    """
    This tool MUST be called BEFORE any other tool.
    Without calling it, the MCP server will not work as expected.
    It MUST be called once in a session.
    """
    return """
Blockscout MCP server version: 0.1.0

If you receive an error "500 Internal Server Error" for any tool, retry calling this tool up to 3 times until successful.

All Blockscout API tools require a chain_id parameter:
- If the chain ID to be used in the tools is not clear, use the tool `get_chains_list` to get chain IDs of all known chains.
- Here is the list of IDs of most popular chains:
  * Ethereum: 1
  * Polygon PoS: 137
  * Base: 8453
  * Arbitrum One: 42161
  * OP Mainnet: 10
  * ZkSync Era: 324
  * Polygon zkEVM: 1101
  * Gnosis: 100
  * Celo: 42220
  * Scroll: 534352
""" 