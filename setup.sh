#!/bin/bash

# SettleMint Blockscout MCP Server Setup Script
# This script helps you set up the SettleMint-enhanced Blockscout MCP server

set -e

echo "======================================"
echo " SettleMint Blockscout MCP Setup"
echo "======================================"
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
REQUIRED_VERSION="3.11"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then 
    echo "❌ Error: Python $REQUIRED_VERSION or higher is required. You have Python $PYTHON_VERSION"
    exit 1
fi
echo "✅ Python $PYTHON_VERSION found"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -e . || {
    echo "❌ Failed to install dependencies. Please check your Python environment."
    exit 1
}
echo "✅ Dependencies installed"

# Check if .env exists, if not copy from example
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env configuration file..."
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file with your SettleMint configuration:"
    echo "   - BLOCKSCOUT_SETTLEMINT_CHAIN_ID"
    echo "   - BLOCKSCOUT_SETTLEMINT_BLOCKSCOUT_URL" 
    echo "   - BLOCKSCOUT_SETTLEMINT_APPLICATION_ACCESS_TOKEN"
    echo ""
    read -p "Would you like to configure these now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        read -p "Enter your SettleMint Chain ID: " chain_id
        read -p "Enter your SettleMint Blockscout URL: " blockscout_url
        read -p "Enter your SettleMint Application Access Token: " access_token
        
        # Update .env file
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s|BLOCKSCOUT_SETTLEMINT_CHAIN_ID=YOUR_CHAIN_ID|BLOCKSCOUT_SETTLEMINT_CHAIN_ID=$chain_id|g" .env
            sed -i '' "s|BLOCKSCOUT_SETTLEMINT_BLOCKSCOUT_URL=https://your-explorer-url.settlemint.com|BLOCKSCOUT_SETTLEMINT_BLOCKSCOUT_URL=$blockscout_url|g" .env
            sed -i '' "s|BLOCKSCOUT_SETTLEMINT_APPLICATION_ACCESS_TOKEN=sm_aat_xxxxx|BLOCKSCOUT_SETTLEMINT_APPLICATION_ACCESS_TOKEN=$access_token|g" .env
        else
            # Linux
            sed -i "s|BLOCKSCOUT_SETTLEMINT_CHAIN_ID=YOUR_CHAIN_ID|BLOCKSCOUT_SETTLEMINT_CHAIN_ID=$chain_id|g" .env
            sed -i "s|BLOCKSCOUT_SETTLEMINT_BLOCKSCOUT_URL=https://your-explorer-url.settlemint.com|BLOCKSCOUT_SETTLEMINT_BLOCKSCOUT_URL=$blockscout_url|g" .env
            sed -i "s|BLOCKSCOUT_SETTLEMINT_APPLICATION_ACCESS_TOKEN=sm_aat_xxxxx|BLOCKSCOUT_SETTLEMINT_APPLICATION_ACCESS_TOKEN=$access_token|g" .env
        fi
        echo "✅ Configuration updated"
    fi
else
    echo "✅ .env file already exists"
fi

# Test the installation
echo ""
echo "🧪 Testing installation..."
python3 -m blockscout_mcp_server --help > /dev/null 2>&1 || {
    echo "❌ Failed to run MCP server. Please check the installation."
    exit 1
}
echo "✅ MCP server is ready!"

# Configure Cursor if requested
echo ""
read -p "Would you like to configure Cursor IDE? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    CURSOR_MCP_FILE="$HOME/.cursor/mcp.json"
    CURRENT_DIR=$(pwd)
    
    # Create .cursor directory if it doesn't exist
    mkdir -p "$HOME/.cursor"
    
    # Check if mcp.json exists
    if [ -f "$CURSOR_MCP_FILE" ]; then
        echo "⚠️  Cursor MCP config already exists. Creating backup..."
        cp "$CURSOR_MCP_FILE" "$CURSOR_MCP_FILE.backup.$(date +%Y%m%d_%H%M%S)"
    fi
    
    # Create or update Cursor MCP configuration
    cat > "$CURSOR_MCP_FILE" << EOF
{
  "mcpServers": {
    "settlemint-blockscout": {
      "command": "python3",
      "args": ["-m", "blockscout_mcp_server"],
      "cwd": "$CURRENT_DIR"
    }
  }
}
EOF
    
    echo "✅ Cursor configuration updated at: $CURSOR_MCP_FILE"
    echo "   Please restart Cursor to apply changes."
fi

echo ""
echo "======================================"
echo " Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Ensure your .env file has correct SettleMint credentials"
echo "2. Test the connection: python3 test_connection.py"
echo "3. Restart your IDE (Cursor/Claude Desktop) to load the MCP server"
echo ""
echo "For more information, see SETTLEMINT_SETUP.md"