# SettleMint Blockchain Analysis - AI Integration Guide

> **Note:** This is the **SettleMint-enhanced Blockscout MCP server** with native support for permissioned SettleMint networks including authentication via token query parameters.

## 🎯 What You'll Get
Transform your SettleMint blockchain analysis with AI! Ask questions in natural language:
- *"What's the latest block on chain 40319?"*
- *"Show me details for address 0x..."*
- *"Analyze recent transaction patterns"*
- *"Get the balance and token holdings of an address"*

---

## 🚀 Quick Setup (Recommended)

### **Automatic Installation**
```bash
# 1. Clone the SettleMint-enhanced MCP server
git clone https://github.com/settlemint/blockscout-mcp-server.git
cd blockscout-mcp-server

# 2. Run the setup script
./setup.sh

# 3. Test your connection
python3 test_connection.py
```

The setup script will:
- Install all dependencies
- Create and configure your .env file securely
- Set up Cursor IDE integration (optional)
- Verify everything works

---

## 📥 Manual Installation

### **Step 1: Install the MCP Server**
```bash
# Clone the SettleMint-enhanced MCP server
git clone https://github.com/settlemint/blockscout-mcp-server.git
cd blockscout-mcp-server

# Install dependencies
pip install -e .

# Verify installation
python3 -m blockscout_mcp_server --help
```

### **Step 2: Configure Your SettleMint Network**

Create a `.env` file from the template:
```bash
cp .env.example .env
```

Edit `.env` with your SettleMint details:
```bash
# Required SettleMint Configuration
BLOCKSCOUT_SETTLEMINT_CHAIN_ID=YOUR_CHAIN_ID
BLOCKSCOUT_SETTLEMINT_BLOCKSCOUT_URL=https://your-explorer-url.settlemint.com/
BLOCKSCOUT_SETTLEMINT_APPLICATION_ACCESS_TOKEN=sm_aat_xxxxx

# Leave other settings as defaults
```

**📍 Where to find your values:**
- **Chain ID**: SettleMint Platform → Your Blockchain → Network Details
- **Blockscout URL**: SettleMint Platform → Insights → Block Explorer → Connect (copy URL without token)
- **Access Token**: SettleMint Platform → Access Tokens → Create new token

**🔒 Security Best Practices:** 
- **NEVER commit your .env file** to version control
- Add `.env` to your `.gitignore` file
- Use Application Access Tokens (`sm_aat_`) for production
- Platform Access Tokens (`sm_pat_`) also work but have broader permissions
- The server passes tokens as query parameters (`?token=`) for SettleMint authentication

### **Step 3: Configure Your AI Platform**

#### **Option 1: Cursor IDE (Recommended)**

1. **Edit `~/.cursor/mcp.json`**:
```json
{
  "mcpServers": {
    "settlemint-blockscout": {
      "command": "python3",
      "args": ["-m", "blockscout_mcp_server", "--http"],
      "cwd": "/path/to/your/mcp-server"
    }
  }
}
```

**⚠️ Important Configuration Notes:**
- The `--http` flag is **required** for Cursor integration
- Update the `"cwd"` path to your mcp-server directory
- **DO NOT** add environment variables to this file
- The server automatically loads configuration from your `.env` file

2. **Restart Cursor** → Look for green MCP indicator

3. **Test:** Ask Cursor: *"What's the latest block on chain 40319?"* (use your chain ID)

#### **Option 2: Claude Desktop**

1. **Edit Claude Desktop config**:
   - Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. **Add configuration**:
```json
{
  "mcpServers": {
    "settlemint-blockscout": {
      "command": "python3",
      "args": ["-m", "blockscout_mcp_server"],
      "cwd": "/path/to/your/mcp-server"
    }
  }
}
```

**Note:** Claude Desktop doesn't require the `--http` flag. Update the `"cwd"` path to your mcp-server directory.

3. **Restart Claude Desktop** → Look for 🔌 connection indicator

---

## 🧪 Verify Your Setup

Run the test script to verify everything works:
```bash
python3 test_connection.py
```

You should see:
```
✅ Configuration Check
   Chain ID: 40319
   Blockscout URL: https://your-explorer.settlemint.com/
   Access Token: ✅ Configured
✅ Resolved URL
✅ Latest block: #12345
✅ Connection Test Successful!
```

If you see any errors:
1. Check your .env file has correct values
2. Verify your access token is valid
3. Ensure your SettleMint network is running
4. Confirm the Blockscout URL doesn't include the token

---

## 🔍 Example Queries

### **Network Overview**
- "What's happening on chain 40319?" (use your chain ID)
- "Show me the latest 5 blocks with their transaction counts"
- "What's the current gas price?"

### **Address Analysis**
- "Get balance and tokens for address 0x..."
- "Show all transactions for address 0x... in the last 24 hours"
- "What NFTs does address 0x... own?"

### **Transaction Investigation**
- "Analyze transaction 0x..."
- "Find all token transfers in block 12345"
- "Show me failed transactions and why they failed"

### **Smart Contract Interaction**
- "Get the ABI for contract 0x..."
- "Read the totalSupply from token contract 0x..."
- "Show the source code for verified contract 0x..."

---

## 🛠️ Troubleshooting

### **"Connection refused" or authentication errors**
- Verify your access token is correct and active
- Check the Blockscout URL doesn't include trailing slashes or tokens
- Ensure you're using the correct token type (sm_aat_ or sm_pat_)
- The server passes tokens as `?token=` query parameters, not headers

### **"Chain not found" errors**
- Confirm your CHAIN_ID matches your SettleMint network exactly
- Clear any cached responses: The server caches "not found" errors for 5 minutes
- Restart the MCP server if you changed the chain ID

### **Cursor not detecting the MCP server**
- **Ensure you included the `--http` flag** in the args array
- Check the `cwd` path in mcp.json points to the correct directory
- Ensure Python 3.11+ is in your PATH
- Completely quit Cursor (Cmd+Q on Mac) and restart after configuration changes

### **Testing without AI**
Test the server directly:
```bash
# Start in stdio mode (for debugging)
python3 -m blockscout_mcp_server

# Start HTTP API mode (what Cursor uses)
python3 -m blockscout_mcp_server --http --rest
# Then test: curl "http://localhost:8000/v1/get_latest_block?chain_id=40319"
```

---

## 📚 Additional Resources

- **MCP Protocol**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Blockscout API**: [docs.blockscout.com](https://docs.blockscout.com)
- **SettleMint Platform**: [console.settlemint.com](https://console.settlemint.com)

---

## 🔐 Security Notes

- **Never commit your .env file** - it contains sensitive tokens
- Use Application Access Tokens with minimal required permissions
- Rotate tokens regularly for production use
- The server only makes read-only API calls

---

## 🤝 Support

- **Issues**: [GitHub Issues](https://github.com/settlemint/blockscout-mcp-server/issues)
- **SettleMint Support**: Contact your SettleMint representative
- **Community**: Join the MCP Discord server

---

*Built with ❤️ for the SettleMint ecosystem*