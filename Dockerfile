FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install uv package manager
RUN pip install uv

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src/ ./src/
COPY main.py ./

# Create virtual environment and install dependencies
# Note: We install only the base dependencies, not the dev dependencies
RUN uv venv && \
    uv sync

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=info

# Command to run the server
CMD ["python", "main.py"]