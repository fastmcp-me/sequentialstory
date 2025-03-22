FROM ghcr.io/astral-sh/uv:python3.11-alpine

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/
COPY sequential_tools.py ./

# Create virtual environment and install dependencies
# Note: We install only the base dependencies, not the dev dependencies
RUN uv venv && \
    uv sync

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run the server
CMD ["uv", "run", "sequential_tools.py"]