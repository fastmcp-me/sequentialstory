# Sequential Story MCP Server

A Model Context Protocol (MCP) server for sequential storytelling as a mnemonic technique for problem-solving.

## Overview

Sequential Story is a narrative-based approach to sequential thinking. Instead of tracking abstract thoughts, it structures problems as story elements with characters, settings, and plot developments to make them more memorable and engaging. This approach leverages the mnemonic power of storytelling to enhance memory retention and problem understanding.

## Features

- Build problem solutions as narrative sequences
- Revise and branch story elements as needed
- Track characters, settings, tones, and plot points
- Formatted, color-coded display of story elements
- Full MCP protocol support for integration with AI systems

## Installation

```bash
# Clone the repository
git clone https://github.com/dhkts1/sequentialStory
cd sequential-story

# Install just the base dependencies using uv
uv venv
source .venv/bin/activate
uv sync

# Install with development dependencies
uv sync --group dev

# Or install in development mode
uv pip install -e .
```

## Usage

### Running the server

```bash
# Run directly using the main script
python main.py
```

### Installing with MCP

```bash
# Install in the Claude desktop app
mcp install -e . -n "Sequential Story Server" main.py:server

# For development with the MCP Inspector
mcp dev main.py:server
```

### Example story element

```json
{
  "element": "Our protagonist, a data scientist named Alex, encounters a mysterious pattern in the customer behavior data.",
  "elementNumber": 1,
  "totalElements": 5,
  "nextElementNeeded": true,
  "character": "Alex (data scientist)",
  "setting": "Data analysis lab",
  "tone": "Mysterious",
  "plotPoint": "Discovery of pattern"
}
```

## Development

```bash
# Install pre-commit hooks
uv run pre-commit install

# Run all pre-commit checks
poe pre
```

## Credits

This project is inspired by the Sequential Thinking MCP tool, adapting its approach to use narrative structures for enhanced memory and problem-solving.