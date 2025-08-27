#!/usr/bin/env python3
"""
Test script to verify SettleMint Blockscout MCP server connection
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the parent directory to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

try:
    from blockscout_mcp_server.config import config
    from blockscout_mcp_server.tools.common import get_blockscout_base_url, make_blockscout_request
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("   Please run: pip3 install -e .")
    sys.exit(1)


async def test_settlemint_connection():
    """Test the connection to SettleMint Blockscout instance."""
    
    print("====================================")
    print(" SettleMint Connection Test")
    print("====================================")
    print()
    
    # Check configuration
    print("📋 Configuration Check:")
    print(f"   Chain ID: {config.settlemint_chain_id or '❌ Not configured'}")
    print(f"   Blockscout URL: {config.settlemint_blockscout_url or '❌ Not configured'}")
    print(f"   Access Token: {'✅ Configured' if config.settlemint_application_access_token else '❌ Not configured'}")
    print()
    
    if not all([config.settlemint_chain_id, config.settlemint_blockscout_url, config.settlemint_application_access_token]):
        print("❌ Missing SettleMint configuration!")
        print("   Please configure your .env file with:")
        print("   - BLOCKSCOUT_SETTLEMINT_CHAIN_ID")
        print("   - BLOCKSCOUT_SETTLEMINT_BLOCKSCOUT_URL")
        print("   - BLOCKSCOUT_SETTLEMINT_APPLICATION_ACCESS_TOKEN")
        return False
    
    # Test 1: Get Blockscout URL
    print("🧪 Test 1: Resolving Blockscout URL...")
    try:
        base_url = await get_blockscout_base_url(config.settlemint_chain_id)
        print(f"   ✅ Resolved URL: {base_url}")
    except Exception as e:
        print(f"   ❌ Failed to resolve URL: {e}")
        return False
    
    # Test 2: Get latest block
    print()
    print("🧪 Test 2: Fetching latest block...")
    try:
        result = await make_blockscout_request(base_url, "/api/v2/blocks", {"type": "block"})
        if result and "items" in result and len(result["items"]) > 0:
            latest_block = result["items"][0]
            print(f"   ✅ Latest block: #{latest_block.get('height', 'Unknown')}")
            print(f"      Timestamp: {latest_block.get('timestamp', 'Unknown')}")
            print(f"      Transactions: {latest_block.get('tx_count', 0)}")
        else:
            print("   ⚠️  No blocks found (empty blockchain?)")
    except Exception as e:
        print(f"   ❌ Failed to fetch blocks: {e}")
        print("      This may indicate an authentication issue.")
        return False
    
    # Test 3: API Stats (if available)
    print()
    print("🧪 Test 3: Fetching network stats...")
    try:
        stats = await make_blockscout_request(base_url, "/api/v2/stats")
        if stats:
            print(f"   ✅ Network stats retrieved:")
            print(f"      Total blocks: {stats.get('total_blocks', 'Unknown')}")
            print(f"      Total addresses: {stats.get('total_addresses', 'Unknown')}")
            print(f"      Total transactions: {stats.get('total_transactions', 'Unknown')}")
    except Exception as e:
        print(f"   ⚠️  Stats endpoint not available: {e}")
        print("      (This is okay - not all instances have this endpoint)")
    
    print()
    print("====================================")
    print(" ✅ Connection Test Successful!")
    print("====================================")
    print()
    print("Your SettleMint Blockscout MCP server is properly configured and working.")
    print("You can now use it with Cursor, Claude Desktop, or other MCP clients.")
    
    return True


async def main():
    """Main entry point."""
    try:
        success = await test_settlemint_connection()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())