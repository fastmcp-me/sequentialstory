"""Tests for the server module."""

from unittest.mock import MagicMock, patch

from src.sequential_thinking_processor import SequentialThoughtData
from src.server import SequentialToolsServer
from src.story_processor import ContentItem, ProcessResult, StoryElementData


class TestSequentialToolsServer:
    """Tests for the SequentialToolsServer class."""

    def test_init(self) -> None:
        """Test server initialization."""
        with (
            patch("src.server.FastMCP") as mock_fastmcp,
            patch("src.server.SequentialStoryProcessor") as mock_story_processor,
            patch("src.server.SequentialThinkingProcessor") as mock_thinking_processor,
        ):
            # Setup mock
            mock_instance = mock_fastmcp.return_value

            # Create server
            server = SequentialToolsServer()

            # Check initialization
            mock_fastmcp.assert_called_once_with(
                name="sequential-tools-server",
                version="0.1.0",
            )
            mock_story_processor.assert_called_once()
            mock_thinking_processor.assert_called_once()
            assert server.mcp == mock_instance
            assert server.story_processor == mock_story_processor.return_value
            assert server.thinking_processor == mock_thinking_processor.return_value

    def test_create_sequentialstory_tool(self) -> None:
        """Test creation of the sequentialstory tool."""
        with patch("src.server.FastMCP"):
            # Setup mocks
            server = SequentialToolsServer()
            server.mcp = MagicMock()
            mock_tool_decorator = MagicMock()
            server.mcp.tool.return_value = mock_tool_decorator

            # Mock the processor's process_element method
            server.story_processor = MagicMock()
            server.story_processor.process_element.return_value = ProcessResult(
                content=[ContentItem(type="text", text="Test")]
            )

            # Call the method to test
            result = server.create_sequentialstory_tool()

            # Verify it returns a callable
            assert callable(result)

            # Check that the tool decorator was used
            server.mcp.tool.assert_called_once()

    def test_create_sequentialthinking_tool(self) -> None:
        """Test creation of the sequentialthinking tool."""
        with patch("src.server.FastMCP"):
            # Setup mocks
            server = SequentialToolsServer()
            server.mcp = MagicMock()
            mock_tool_decorator = MagicMock()
            server.mcp.tool.return_value = mock_tool_decorator

            # Mock the processor's process_thought method
            server.thinking_processor = MagicMock()
            server.thinking_processor.process_thought.return_value = ProcessResult(
                content=[ContentItem(type="text", text="Test")]
            )

            # Call the method to test
            result = server.create_sequentialthinking_tool()

            # Verify it returns a callable
            assert callable(result)

            # Check that the tool decorator was used
            server.mcp.tool.assert_called_once()

    def test_sequentialstory_function(self) -> None:
        """Test the sequentialstory function."""
        # Setup server with mocked components
        with patch("src.server.SequentialStoryProcessor") as mock_processor_class:
            # Setup the processor mock
            mock_processor = MagicMock()
            mock_processor_class.return_value = mock_processor

            # Create test data
            expected_result = ProcessResult(content=[ContentItem(type="text", text="Test result")])
            mock_processor.process_element.return_value = expected_result

            # Create server - this will use our mocked processor
            server = SequentialToolsServer()

            # Get the sequentialstory function
            sequentialstory = server.create_sequentialstory_tool()

            # Create test input
            test_input = StoryElementData(
                element="Test element",
                element_number=1,
                total_elements=3,
                next_element_needed=True,
            )

            # Call the function
            result = sequentialstory(test_input)

            # Verify the result
            mock_processor.process_element.assert_called_once_with(test_input)
            assert result == expected_result

    def test_sequentialthinking_function(self) -> None:
        """Test the sequentialthinking function."""
        # Setup server with mocked components
        with patch("src.server.SequentialThinkingProcessor") as mock_processor_class:
            # Setup the processor mock
            mock_processor = MagicMock()
            mock_processor_class.return_value = mock_processor

            # Create test data
            expected_result = ProcessResult(content=[ContentItem(type="text", text="Test result")])
            mock_processor.process_thought.return_value = expected_result

            # Create server - this will use our mocked processor
            server = SequentialToolsServer()

            # Get the sequentialthinking function
            sequentialthinking = server.create_sequentialthinking_tool()

            # Create test input
            test_input = SequentialThoughtData(
                thought="Test thought",
                thought_number=1,
                total_thoughts=3,
                next_thought_needed=True,
            )

            # Call the function
            result = sequentialthinking(test_input)

            # Verify the result
            mock_processor.process_thought.assert_called_once_with(test_input)
            assert result == expected_result


# For backward compatibility in tests
class TestSequentialStoryServer(TestSequentialToolsServer):
    """Tests for the SequentialStoryServer class (alias for SequentialToolsServer)."""
