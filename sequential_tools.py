"""Sequential Tools Server - Narrative and analytical mnemonic tools.

This MCP server provides Sequential Thinking and Sequential Story tools
that help with problem-solving, planning, and creating mnemonic narratives.

"""

import json
import sys

from src.server import SequentialToolsServer
from src.utils.logging import get_logger, setup_logging
from src.utils.settings import get_settings

# Set up logging
setup_logging()
logger = get_logger("sequential_tools")

# Create server instance
server = SequentialToolsServer()

# When running as a script directly
if __name__ == "__main__":
    try:
        settings = get_settings()
        logger.info("Starting Sequential Tools MCP Server...")
        logger.info("Server metadata: %s", json.dumps(settings.server_metadata, indent=2))
        logger.info("Enabled tools: %s", ", ".join(settings.enabled_tools))

        server.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception:
        logger.exception("Unhandled exception")
        sys.exit(1)
