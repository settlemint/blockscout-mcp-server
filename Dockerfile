FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml pyproject.toml
# Install uv for dependency management
RUN pip install uv
RUN uv pip install --system . # Install dependencies from pyproject.toml

COPY blockscout_mcp_server /app/blockscout_mcp_server

ENV PYTHONUNBUFFERED=1

# Expose environment variables that can be set at runtime
# Set defaults here to document expected environment variables
ENV BLOCKSCOUT_BS_URL="https://eth.blockscout.com"
ENV BLOCKSCOUT_BS_API_KEY=""
ENV BLOCKSCOUT_BS_TIMEOUT="120.0"
ENV BLOCKSCOUT_BENS_URL="https://bens.services.blockscout.com"
ENV BLOCKSCOUT_BENS_TIMEOUT="30.0"
ENV BLOCKSCOUT_CHAINSCOUT_URL="http://chains.blockscout.com"
ENV BLOCKSCOUT_CHAINSCOUT_TIMEOUT="15.0"

CMD ["python", "-m", "blockscout_mcp_server"] 