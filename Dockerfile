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
ENV BLOCKSCOUT_BENS_URL="https://bens.services.blockscout.com"

CMD ["python", "-m", "blockscout_mcp_server"] 