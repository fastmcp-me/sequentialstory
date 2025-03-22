#!/usr/bin/env python3
"""Sequential MCP Tools Server - Narrative and analytical mnemonic tools."""

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

# Create the server - this is the object we'll export for MCP dev and install
server = SequentialToolsServer()

# When running as a script directly
if __name__ == "__main__":
    try:
        logger.info("Starting Sequential Tools MCP Server...")
        server.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception:
        logger.exception("Unhandled exception")
        sys.exit(1)
