from blockscout_mcp_server.tools.common import make_chainscout_request

async def get_chains_list() -> str:
    """
    Get the list of known blockchain chains with their IDs.
    Useful for getting a chain ID when the chain name is known. This information can be used in other tools that require a chain ID to request information.
    """
    api_path = "/api/chains/list"
    response_data = await make_chainscout_request(api_path=api_path)
    
    # Format the response as a text output
    output_lines = ["The list of known chains with their ids:"]
    
    # Check if response_data is a list and has entries
    if isinstance(response_data, list) and response_data:
        # Sort chains by name for better readability
        sorted_chains = sorted(response_data, key=lambda x: x.get("name", ""))
        
        for chain in sorted_chains:
            name = chain.get("name")
            chain_id = chain.get("chainid")
            if name is not None and chain_id is not None:
                output_lines.append(f"{name}: {chain_id}")
    else:
        output_lines.append("No chains found or invalid response format.")
    
    # Join all lines with newlines
    return "\n".join(output_lines) 