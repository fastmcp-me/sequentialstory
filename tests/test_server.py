"""Tests for the server module."""

from unittest.mock import MagicMock, patch

from src.server import SequentialToolsServer
from src.utils.settings import ToolType


@patch("src.server.settings")
class TestSequentialToolsServer:
    """Tests for the SequentialToolsServer class."""

    @patch("src.server.FastMCP")
    def test_init(self, mock_fast_mcp: MagicMock, mock_settings: MagicMock) -> None:
        """Test server initialization."""
        # Setup mock settings with both tools enabled
        mock_settings.enabled_tools = [ToolType.STORY, ToolType.THINKING]
        mock_settings.server_metadata = {
            "name": "test-name",
            "version": "test-version",
        }

        # Initialize server
        server = SequentialToolsServer()

        # Verify FastMCP was initialized with correct parameters
        mock_fast_mcp.assert_called_once()
        _, kwargs = mock_fast_mcp.call_args
        assert kwargs["name"] == "test-name"
        assert kwargs["version"] == "test-version"
        assert "Sequential Thinking and Sequential Story" in kwargs["description"]

        # Verify the MCP instance was created
        assert server.mcp is mock_fast_mcp.return_value

    def test_get_description_both_tools(self, mock_settings: MagicMock) -> None:
        """Test description with both tools enabled."""
        # Setup mock settings
        mock_settings.enabled_tools = [ToolType.STORY, ToolType.THINKING]

        # Assert directly on initialization params
        with patch("src.server.FastMCP") as mock_fast_mcp:
            SequentialToolsServer()
            _, kwargs = mock_fast_mcp.call_args
            assert "Sequential Thinking and Sequential Story" in kwargs["description"]

    def test_get_description_thinking_only(self, mock_settings: MagicMock) -> None:
        """Test description with only thinking tool enabled."""
        # Setup mock settings
        mock_settings.enabled_tools = [ToolType.THINKING]

        # Assert directly on initialization params
        with patch("src.server.FastMCP") as mock_fast_mcp:
            SequentialToolsServer()
            _, kwargs = mock_fast_mcp.call_args
            assert "Sequential Thinking tool" in kwargs["description"]
            assert "Sequential Story" not in kwargs["description"]

    def test_get_description_story_only(self, mock_settings: MagicMock) -> None:
        """Test description with only story tool enabled."""
        # Setup mock settings
        mock_settings.enabled_tools = [ToolType.STORY]

        # Assert directly on initialization params
        with patch("src.server.FastMCP") as mock_fast_mcp:
            SequentialToolsServer()
            _, kwargs = mock_fast_mcp.call_args
            assert "Sequential Story tool" in kwargs["description"]
            assert "Sequential Thinking" not in kwargs["description"]

    def test_get_description_no_tools(self, mock_settings: MagicMock) -> None:
        """Test description with no tools enabled."""
        # Setup mock settings
        mock_settings.enabled_tools = []

        # Assert directly on initialization params
        with patch("src.server.FastMCP") as mock_fast_mcp:
            SequentialToolsServer()
            _, kwargs = mock_fast_mcp.call_args
            assert "no tools enabled" in kwargs["description"]

    @patch("src.server.SequentialStoryProcessor")
    @patch("src.server.SequentialThinkingProcessor")
    def test_initialize_tools_both(
        self,
        mock_thinking_processor: MagicMock,
        mock_story_processor: MagicMock,
        mock_settings: MagicMock,
    ) -> None:
        """Test tool initialization with both tools enabled."""
        # Setup mock settings
        mock_settings.enabled_tools = [ToolType.STORY, ToolType.THINKING]

        # Create server instance with mocked MCP
        mock_mcp = MagicMock()
        with patch("src.server.FastMCP", return_value=mock_mcp):
            # Create server (initialization will call _initialize_tools)
            SequentialToolsServer()

        # Verify both processors were created and registered with MCP
        mock_story_processor.assert_called_once()
        mock_thinking_processor.assert_called_once()
        mock_story_processor.return_value.register_with_mcp.assert_called_once_with(mock_mcp)
        mock_thinking_processor.return_value.register_with_mcp.assert_called_once_with(mock_mcp)

    @patch("src.server.SequentialStoryProcessor")
    @patch("src.server.SequentialThinkingProcessor")
    def test_initialize_tools_story_only(
        self,
        mock_thinking_processor: MagicMock,
        mock_story_processor: MagicMock,
        mock_settings: MagicMock,
    ) -> None:
        """Test tool initialization with only story tool enabled."""
        # Setup mock settings
        mock_settings.enabled_tools = [ToolType.STORY]

        # Create server instance with mocked MCP
        mock_mcp = MagicMock()
        with patch("src.server.FastMCP", return_value=mock_mcp):
            # Create server (initialization will call _initialize_tools)
            SequentialToolsServer()

        # Verify only story processor was created and registered with MCP
        mock_story_processor.assert_called_once()
        mock_thinking_processor.assert_not_called()
        mock_story_processor.return_value.register_with_mcp.assert_called_once_with(mock_mcp)

    @patch("src.server.SequentialStoryProcessor")
    @patch("src.server.SequentialThinkingProcessor")
    def test_initialize_tools_thinking_only(
        self,
        mock_thinking_processor: MagicMock,
        mock_story_processor: MagicMock,
        mock_settings: MagicMock,
    ) -> None:
        """Test tool initialization with only thinking tool enabled."""
        # Setup mock settings
        mock_settings.enabled_tools = [ToolType.THINKING]

        # Create server instance with mocked MCP
        mock_mcp = MagicMock()
        with patch("src.server.FastMCP", return_value=mock_mcp):
            # Create server (initialization will call _initialize_tools)
            SequentialToolsServer()

        # Verify only thinking processor was created and registered with MCP
        mock_story_processor.assert_not_called()
        mock_thinking_processor.assert_called_once()
        mock_thinking_processor.return_value.register_with_mcp.assert_called_once_with(mock_mcp)

    @patch("src.server.SequentialStoryProcessor")
    @patch("src.server.SequentialThinkingProcessor")
    def test_initialize_tools_none(
        self,
        mock_thinking_processor: MagicMock,
        mock_story_processor: MagicMock,
        mock_settings: MagicMock,
    ) -> None:
        """Test tool initialization with no tools enabled."""
        # Setup mock settings
        mock_settings.enabled_tools = []

        # Create server instance with mocked MCP
        mock_mcp = MagicMock()
        with patch("src.server.FastMCP", return_value=mock_mcp):
            # Create server (initialization will call _initialize_tools)
            SequentialToolsServer()

        # Verify no processors were created or registered
        mock_story_processor.assert_not_called()
        mock_thinking_processor.assert_not_called()

    def test_run(self, mock_settings: MagicMock) -> None:
        """Test run method."""
        # Setup mock settings
        mock_settings.enabled_tools = []

        # Create mocked MCP
        mock_mcp = MagicMock()

        # Create server instance with mocked MCP
        with patch("src.server.FastMCP", return_value=mock_mcp):
            server = SequentialToolsServer()
            server.run()

        # Verify MCP run was called
        mock_mcp.run.assert_called_once()


class TestBackwardCompatibility:
    """Tests for backward compatibility."""

    def test_sequential_story_server_alias(self) -> None:
        """Test that SequentialStoryServer is an alias for SequentialToolsServer."""
        from src.server import SequentialStoryServer, SequentialToolsServer

        assert SequentialStoryServer == SequentialToolsServer
