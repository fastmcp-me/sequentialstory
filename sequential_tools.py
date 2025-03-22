"""Sequential Tools Server - Narrative and analytical mnemonic tools.

This MCP server provides Sequential Thinking and Sequential Story tools
that help with problem-solving, planning, and creating mnemonic narratives.

The server follows the Model Context Protocol (MCP) standard and
is intended to be registered with Smithery.ai.

Project Repository: https://github.com/dhkts1/sequentialStory
"""

import json
import logging
import sys

from src.server import SequentialToolsServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("sequential_tools")

# Server metadata for Smithery registry
SERVER_METADATA = {
    "name": "sequential-tools",
    "display_name": "Sequential Tools & Sequential Story",
    "version": "0.1.0",
    "description": "MCP tools for dynamic problem-solving through Sequential Thinking and Sequential Story",
    "author": "dhkts1",
    "repository": "https://github.com/dhkts1/sequentialStory",
    "documentation": "https://github.com/dhkts1/sequentialStory/README.md",
}

# Create the server with metadata - this is the object we'll export for MCP
server = SequentialToolsServer(metadata=SERVER_METADATA)

# When running as a script directly
if __name__ == "__main__":
    try:
        logger.info("Starting Sequential Tools MCP Server...")
        logger.info("Server metadata: %s", json.dumps(SERVER_METADATA, indent=2))
        logger.info("Using stdin/stdout transport (not websockets)")
        server.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception:
        logger.exception("Unhandled exception")
        sys.exit(1)
