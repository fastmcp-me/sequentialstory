"""Tests for the sequential_thinking_processor module."""

from unittest.mock import MagicMock, patch

from src.sequential_thinking_processor import (
    ContentItem,
    ProcessResult,
    SequentialThinkingProcessor,
    SequentialThoughtData,
)


class TestSequentialThoughtData:
    """Tests for the SequentialThoughtData class."""

    def test_model_validation(self) -> None:
        """Test model validation."""
        # Create a valid instance
        data = SequentialThoughtData(
            thought="Test thought",
            thought_number=1,
            total_thoughts=3,
            next_thought_needed=True,
        )
        # Check all fields are set correctly
        assert data.thought == "Test thought"
        assert data.thought_number == 1
        assert data.total_thoughts == 3
        assert data.next_thought_needed is True
        assert data.is_revision is None
        assert data.revises_thought is None
        assert data.branch_from_thought is None
        assert data.branch_id is None
        assert data.needs_more_thoughts is None

    def test_model_validator_adjust_total_thoughts(self) -> None:
        """Test adjust_total_thoughts model validator."""
        # Create a thought with thought_number > total_thoughts
        data = SequentialThoughtData(
            thought="Test thought",
            thought_number=5,
            total_thoughts=3,
            next_thought_needed=True,
        )
        # Check that total_thoughts was adjusted to 5
        assert data.total_thoughts == 5


class TestContentItem:
    """Tests for the ContentItem class."""

    def test_text_content(self) -> None:
        """Test ContentItem with text content."""
        content = ContentItem(type="text", text="Test content")
        assert content.type == "text"
        assert content.text == "Test content"

    def test_dict_content(self) -> None:
        """Test ContentItem with dict content."""
        content_dict = {"key": "value", "number": 42}
        content = ContentItem(type="json", text=content_dict)
        assert content.type == "json"
        assert content.text == content_dict


class TestProcessResult:
    """Tests for the ProcessResult class."""

    def test_create_success(self) -> None:
        """Test create_success class method."""
        data = SequentialThoughtData(
            thought="Test thought",
            thought_number=1,
            total_thoughts=3,
            next_thought_needed=True,
        )
        branches = ["branch1", "branch2"]
        history_length = 5

        result = ProcessResult.create_success(data, branches, history_length)

        assert len(result.content) == 1
        assert result.content[0].type == "json"
        assert isinstance(result.content[0].text, dict)
        content_text = result.content[0].text
        assert content_text.get("thought_number") == 1
        assert content_text.get("total_thoughts") == 3
        assert content_text.get("next_thought_needed") is True
        assert content_text.get("branches") == branches
        assert content_text.get("thought_history_length") == history_length

    def test_create_error(self) -> None:
        """Test create_error class method."""
        error = Exception("Test error")
        result = ProcessResult.create_error(error)

        assert len(result.content) == 1
        assert result.content[0].type == "json"
        assert isinstance(result.content[0].text, dict)
        content_text = result.content[0].text
        assert content_text.get("error") == "Test error"
        assert content_text.get("status") == "failed"
        assert result.is_error is True


class TestSequentialThinkingProcessor:
    """Tests for the SequentialThinkingProcessor class."""

    def test_init(self) -> None:
        """Test processor initialization."""
        processor = SequentialThinkingProcessor()
        assert processor.thought_history == []
        assert processor.branches == {}
        assert processor.thinking_needs_more_thoughts is True

    def test_format_thought(self) -> None:
        """Test format_thought method."""
        processor = SequentialThinkingProcessor()

        # Use patch to mock the Panel creation so we can test its inputs
        with patch("src.sequential_thinking_processor.Panel") as mock_panel:
            # Configure the mock
            mock_panel_instance = MagicMock()
            mock_panel.return_value = mock_panel_instance

            # Test standard thought
            thought_data = SequentialThoughtData(
                thought="Test thought",
                thought_number=1,
                total_thoughts=3,
                next_thought_needed=True,
            )
            processor.format_thought(thought_data)

            # Check that Panel was called with the right content
            args, kwargs = mock_panel.call_args
            # The first argument should be a Text object with the thought content
            assert args[0].plain == "Test thought"
            # Check the title parameter contains the expected text
            assert "💭 Thought 1/3" in kwargs["title"].plain

            # Reset mock for next test
            mock_panel.reset_mock()

            # Test revision thought
            revision_data = SequentialThoughtData(
                thought="Revision thought",
                thought_number=2,
                total_thoughts=3,
                next_thought_needed=True,
                is_revision=True,
                revises_thought=1,
            )
            processor.format_thought(revision_data)

            # Check that Panel was called with the right content
            args, kwargs = mock_panel.call_args
            assert args[0].plain == "Revision thought"
            title_text = kwargs["title"].plain
            assert "🔄 Revision 2/3" in title_text
            assert "revising thought 1" in title_text

            # Reset mock for next test
            mock_panel.reset_mock()

            # Test branch thought
            branch_data = SequentialThoughtData(
                thought="Branch thought",
                thought_number=3,
                total_thoughts=3,
                next_thought_needed=False,
                branch_from_thought=1,
                branch_id="branch1",
            )
            processor.format_thought(branch_data)

            # Check that Panel was called with the right content
            args, kwargs = mock_panel.call_args
            assert args[0].plain == "Branch thought"
            title_text = kwargs["title"].plain
            assert "🌿 Branch 3/3" in title_text
            assert "from thought 1" in title_text
            assert "ID: branch1" in title_text

    def test_process_thought(self) -> None:
        """Test process_thought method."""
        # Create processor with mocked console
        with patch("src.sequential_thinking_processor.Panel"), patch("src.sequential_thinking_processor.Text"):
            processor = SequentialThinkingProcessor()
            processor.console = MagicMock()

            # We need to mock is_thinking_complete to make it always return False
            # so the warning message is always printed
            processor.is_thinking_complete = MagicMock(return_value=False)

            # Test processing a thought
            thought_data = SequentialThoughtData(
                thought="Test thought",
                thought_number=1,
                total_thoughts=3,
                next_thought_needed=True,
            )

            result = processor.process_thought(thought_data)

            # Check that the thought was added to history
            assert len(processor.thought_history) == 1
            assert processor.thought_history[0] == thought_data

            # Check the console output - should be called twice
            # Once for the panel, once for the completion message
            assert processor.console.print.call_count == 2

            # Check the result
            assert isinstance(result, ProcessResult)
            assert len(result.content) == 1
            assert result.content[0].type == "json"
            content_text = result.content[0].text
            assert isinstance(content_text, dict)
            assert content_text.get("thought_number") == 1
            assert content_text.get("thought_history_length") == 1
