"""Tests for the story_processor module."""

from rich.panel import Panel
from src.story_processor import ContentItem, ProcessResult, SequentialStoryProcessor, StoryElementData


class TestStoryElementData:
    """Tests for the StoryElementData model."""

    def test_model_validation(self) -> None:
        """Test basic model validation."""
        # Valid data should create a model instance
        data = StoryElementData(
            element="Test element",
            element_number=1,
            total_elements=3,
            next_element_needed=True,
        )
        assert data.element == "Test element"
        assert data.element_number == 1
        assert data.total_elements == 3
        assert data.next_element_needed is True
        assert data.is_revision is None
        assert data.character is None

    def test_model_validator_adjust_total_elements(self) -> None:
        """Test the adjust_total_elements validator."""
        # When element_number > total_elements, total_elements should be adjusted
        data = StoryElementData(
            element="Test element",
            element_number=5,
            total_elements=3,
            next_element_needed=True,
        )
        assert data.total_elements == 5

        # When element_number <= total_elements, total_elements should not change
        data = StoryElementData(
            element="Test element",
            element_number=3,
            total_elements=5,
            next_element_needed=True,
        )
        assert data.total_elements == 5


class TestContentItem:
    """Tests for the ContentItem model."""

    def test_text_content(self) -> None:
        """Test creation with text content."""
        item = ContentItem(type="text", text="Plain text")
        assert item.type == "text"
        assert item.text == "Plain text"

    def test_dict_content(self) -> None:
        """Test creation with dictionary content."""
        item = ContentItem(type="text", text={"key": "value"})
        assert item.type == "text"
        assert item.text == {"key": "value"}


class TestProcessResult:
    """Tests for the ProcessResult model."""

    def test_create_success(self) -> None:
        """Test creating a success result."""
        element = StoryElementData(
            element="Test element",
            element_number=1,
            total_elements=3,
            next_element_needed=True,
        )
        result = ProcessResult.create_success(element, ["branch1"], 5)
        assert result.is_error is None
        assert len(result.content) == 1
        assert result.content[0].type == "text"
        assert isinstance(result.content[0].text, dict)
        assert result.content[0].text["element_number"] == 1
        assert result.content[0].text["total_elements"] == 3
        assert result.content[0].text["next_element_needed"] is True
        assert result.content[0].text["branches"] == ["branch1"]
        assert result.content[0].text["element_history_length"] == 5

    def test_create_error(self) -> None:
        """Test creating an error result."""
        error = ValueError("Test error")
        result = ProcessResult.create_error(error)
        assert result.is_error is True
        assert len(result.content) == 1
        assert result.content[0].type == "text"
        assert isinstance(result.content[0].text, dict)
        assert result.content[0].text["error"] == "Test error"
        assert result.content[0].text["status"] == "failed"


class TestSequentialStoryProcessor:
    """Tests for the SequentialStoryProcessor class."""

    def test_init(self) -> None:
        """Test initialization."""
        processor = SequentialStoryProcessor()
        assert processor.element_history == []
        assert processor.branches == {}

    def test_format_element(self) -> None:
        """Test formatting an element."""
        processor = SequentialStoryProcessor()
        element = StoryElementData(
            element="Test element",
            element_number=1,
            total_elements=3,
            next_element_needed=True,
        )
        panel = processor.format_element(element)
        assert isinstance(panel, Panel)
        # Check that the panel contains our text (without using .plain)
        assert str(panel.renderable) == "Test element"

    def test_process_element(self) -> None:
        """Test processing an element."""
        processor = SequentialStoryProcessor()
        element = StoryElementData(
            element="Test element",
            element_number=1,
            total_elements=3,
            next_element_needed=True,
        )
        result = processor.process_element(element)
        assert len(processor.element_history) == 1
        assert processor.element_history[0] == element
        assert result.is_error is None
        assert len(result.content) == 1
        assert result.content[0].type == "text"
        assert isinstance(result.content[0].text, dict)
        assert result.content[0].text["element_number"] == 1
        assert result.content[0].text["element_history_length"] == 1

    def test_branch_handling(self) -> None:
        """Test branch handling."""
        processor = SequentialStoryProcessor()
        element = StoryElementData(
            element="Branch element",
            element_number=2,
            total_elements=3,
            next_element_needed=True,
            branch_from_element=1,
            branch_id="test-branch",
        )
        processor.process_element(element)
        assert "test-branch" in processor.branches
        assert len(processor.branches["test-branch"]) == 1
        assert processor.branches["test-branch"][0] == element
