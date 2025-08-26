# SettleMint Blockchain Analysis - AI Integration Guide

> **Note:** This guide uses the **SettleMint-enhanced Blockscout MCP server** with support for private SettleMint networks. The enhanced version is available at [github.com/settlemint/blockscout-mcp-server](https://github.com/settlemint/blockscout-mcp-server).

## 🎯 What You'll Get
Transform your SettleMint blockchain analysis with AI! Ask questions in natural language:
- *"What's the latest block on my network?"*
- *"Show me details for address 0x..."*
- *"Analyze recent transaction patterns"*

---

## 📥 Step 1: Install the MCP Server

### **Option A: Quick Clone (Recommended)**
```bash
# 1. Clone the SettleMint-enabled version
git clone https://github.com/settlemint/blockscout-mcp-server.git
cd blockscout-mcp-server

# 2. Install dependencies
pip install -e .

# 3. Verify installation
python -m blockscout_mcp_server --help
```

### **Option B: Docker (Alternative)**
```bash
# Note: Uses original Blockscout image (doesn't include SettleMint modifications)
# For full SettleMint support, use Option A above

# Pull the image
docker pull ghcr.io/blockscout/mcp-server:latest

# Test it works
docker run --rm ghcr.io/blockscout/mcp-server:latest python -m blockscout_mcp_server --help
```

---

## 📋 Step 2: Get Your SettleMint Info

You need **3 pieces of information** from your SettleMint platform:

1. **Chain ID**: Your network ID (e.g., `YOUR_CHAIN_ID`)
2. **Blockscout URL**: Your block explorer URL with PAT token  
3. **PAT Token**: Your SettleMint Personal Access Token

**📍 How to Find These:**
- **Chain ID**: SettleMint Platform → Your Blockchain → Network Details
- **Blockscout URL**: SettleMint Platform → Block Explorer → Copy full URL
- **PAT Token**: Usually visible in the Blockscout URL (format: `sm_pat_xxxxx`)

---

## 🚀 Step 3: Configure Your AI Platform

### **Option 1: Cursor IDE (Recommended)**

1. **Open Cursor → Settings → Extensions → MCP**

2. **Edit `~/.cursor/mcp.json`** (create if doesn't exist):
```json
{
  "mcpServers": {
    "settlemint-blockscout": {
      "command": "python3",
      "args": [
        "-m", "blockscout_mcp_server",
        "--stdio"
      ],
      "cwd": "/path/to/your/blockscout-mcp-server",
      "env": {
        "BLOCKSCOUT_SETTLEMINT_CHAIN_ID": "YOUR_CHAIN_ID",
        "BLOCKSCOUT_SETTLEMINT_BLOCKSCOUT_URL": "https://your-explorer-url.settlemint.com/YOUR_PAT_TOKEN",
        "BLOCKSCOUT_BS_API_KEY": "YOUR_PAT_TOKEN"
      }
    }
  }
}
```

3. **Replace the placeholders:**
   - `"cwd"` → Full path to where you cloned the blockscout-mcp-server repo
   - `YOUR_CHAIN_ID` → Your Chain ID
   - URL and token → Your own Blockscout URL and PAT token

4. **Restart Cursor** → Check for green MCP status

5. **Test:** *"What's the latest block on chain YOUR_CHAIN_ID?"*

---

### **Option 2: Claude Desktop**

1. **Open Claude Desktop → Settings → Developer → Edit Config**

2. **Add to `claude_desktop_config.json`:**
```json
{
  "mcpServers": {
    "settlemint-blockscout": {
      "command": "python3",
      "args": [
        "-m", "blockscout_mcp_server",
        "--stdio"
      ],
      "cwd": "/path/to/your/blockscout-mcp-server",
      "env": {
        "BLOCKSCOUT_SETTLEMINT_CHAIN_ID": "YOUR_CHAIN_ID",
        "BLOCKSCOUT_SETTLEMINT_BLOCKSCOUT_URL": "https://your-explorer-url.settlemint.com/YOUR_PAT_TOKEN",
        "BLOCKSCOUT_BS_API_KEY": "YOUR_PAT_TOKEN"
      }
    }
  }
}
```

3. **Update placeholders** (same as above)

4. **Restart Claude Desktop** → Look for 🔌 connection indicator

---

### **Option 3: Docker Configuration**
If you prefer Docker, use this config instead:
```json
{
  "mcpServers": {
    "settlemint-blockscout": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-e", "BLOCKSCOUT_SETTLEMINT_CHAIN_ID=YOUR_CHAIN_ID",
        "-e", "BLOCKSCOUT_SETTLEMINT_BLOCKSCOUT_URL=https://your-explorer-url.settlemint.com/YOUR_PAT_TOKEN",
        "-e", "BLOCKSCOUT_BS_API_KEY=YOUR_PAT_TOKEN",
        "ghcr.io/blockscout/mcp-server:latest"
      ]
    }
  }
}
```

---

## 🧪 Step 4: Start Querying!

### **🔍 Network Overview**
```
"What's happening on my SettleMint network?"
"Show me the latest 5 blocks"
"What's the current transaction volume?"
```

### **📊 Address Analysis**
```
"Get details for address 0x..."
"What tokens does address 0x... hold?"
"Show me all transactions for address 0x... today"
```

### **💰 Transaction Investigation**
```
"Analyze transaction 0x..."
"Show me large value transfers in the last 24 hours"
"Find failed transactions and explain why they failed"
```