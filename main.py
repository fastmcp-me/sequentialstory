#!/usr/bin/env python3
"""Sequential Story MCP Server - A narrative-based mnemonic tool."""

import logging
import sys

from src.server import SequentialStoryServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("sequential_story")

# Create the server - this is the object we'll export for MCP dev and install
server = SequentialStoryServer()

# When running as a script directly
if __name__ == "__main__":
    try:
        logger.info("Starting Sequential Story MCP Server...")
        server.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception:
        logger.exception("Unhandled exception")
        sys.exit(1)
