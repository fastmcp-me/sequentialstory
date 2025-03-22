"""Sequential Tools Server - Narrative and analytical mnemonic tools.

This MCP server provides Sequential Thinking and Sequential Story tools
that help with problem-solving, planning, and creating mnemonic narratives.

The server follows the Model Context Protocol (MCP) standard and
is intended to be registered with Smithery.ai.

Project Repository: https://github.com/dhkts1/sequentialStory
"""

import json
import sys

from src.server import SequentialToolsServer
from src.utils.logging import get_logger, setup_logging
from src.utils.settings import get_settings

# Set up logging
setup_logging()
logger = get_logger("sequential_tools")


def create_server() -> SequentialToolsServer:
    """Create and configure the Sequential Tools server.

    Uses pydantic Settings to configure the server, with settings loaded from
    environment variables with the SEQUENTIAL_TOOLS_ prefix.

    Returns:
        Configured SequentialToolsServer instance

    """
    settings = get_settings()

    # Create server with settings
    return SequentialToolsServer(metadata=settings.server_metadata, config=settings.server_config)


# Create server instance with configuration from settings
server = create_server()

# When running as a script directly
if __name__ == "__main__":
    try:
        settings = get_settings()
        logger.info("Starting Sequential Tools MCP Server...")
        logger.info("Server metadata: %s", json.dumps(settings.server_metadata, indent=2))
        logger.info("Server configuration: %s", json.dumps({"enabled_tools": server.get_enabled_tools()}, indent=2))
        logger.info("Enabled tools: %s", ", ".join(server.get_enabled_tools()))
        logger.info("Using stdin/stdout transport (not websockets)")
        server.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception:
        logger.exception("Unhandled exception")
        sys.exit(1)
