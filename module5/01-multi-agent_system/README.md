# Multi-Agent Travel Assistant System

A LangGraph-based multi-agent system that provides travel information about Cornwall, England using vector-based knowledge retrieval from WikiVoyage pages.

## Overview

This system demonstrates a complete implementation of a conversational AI agent that can:
- Search travel information about Cornwall destinations
- Use vector similarity search for relevant content retrieval
- Maintain conversation state through LangGraph
- Execute tools dynamically based on user queries

## Architecture

**Components:**
- **Vector Knowledge Base**: Chroma vector store with WikiVoyage content
- **Search Tool**: Semantic search through embedded travel information  
- **LangGraph Agent**: State management and conversation flow
- **Tool Execution Node**: Dynamic tool calling and result handling

**Data Sources:**
- Cornwall travel information from WikiVoyage
- North Cornwall, South Cornwall, West Cornwall regions
- Embedded using OpenAI embeddings for semantic search

## Prerequisites

- Python 3.8+
- OpenAI API key
- Internet connection for downloading WikiVoyage content

## Setup

### 1. Create Virtual Environment

Create and activate a dedicated Python environment:

```bash
# Create virtual environment
python -m venv myagent

# Activate environment (Linux/Mac)
source myagent/bin/activate

# Activate environment (Windows)
myagent\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up Environment Variables

Copy the example environment file and configure your API key:
```bash
# Copy example environment file
cp .env.example .env
```

Then edit `.env` file and replace the placeholder with your actual OpenAI API key:
```env
OPENAI_API_KEY=sk-your_actual_openai_api_key_here
```

**Alternative setup methods:**
```bash
# Quick setup via command line
echo "OPENAI_API_KEY=sk-your_actual_key_here" > .env

# Or export as environment variable (temporary)
export OPENAI_API_KEY=sk-your_actual_key_here
```

### 4. Download Language Models (if needed)

```bash
python -m spacy download en_core_web_sm
```

### 5. Verify Installation

Test that everything is working:
```bash
python -c "import langchain, langgraph, chromadb; print('All dependencies installed successfully!')"
```

## Usage

Run the travel assistant:
```bash
python agent.py
```

**Example interactions:**
- "What are the best beaches in Cornwall?"
- "Tell me about attractions in North Cornwall"
- "Where can I find good seafood restaurants?"
- "What should I visit in Penzance?"

## How It Works

1. **Initialization**: Downloads and embeds WikiVoyage pages for Cornwall regions
2. **Query Processing**: User input is processed through the LangGraph agent
3. **Tool Selection**: Agent decides whether to use the travel search tool
4. **Information Retrieval**: Semantic search finds relevant travel content
5. **Response Generation**: Agent synthesizes search results into helpful responses

## Technical Details

**Vector Store:**
- Uses Chroma for vector storage and retrieval
- OpenAI embeddings for semantic similarity
- Chunk size: 1024 characters with 128 overlap

**LangGraph Configuration:**
- State-based conversation management
- Tool condition routing for dynamic tool usage
- Message history preservation

**Search Tool:**
- Returns top 4 most relevant content chunks
- Searches across all embedded Cornwall travel content
- Handles queries about destinations, attractions, activities

## File Structure

```
01-multi-agent_system/
├── agent.py           # Main multi-agent system implementation
├── requirements.txt   # Python dependencies
├── .env.example      # Environment variables template
├── .env              # Your environment variables (create from .env.example)
└── README.md         # This documentation
```

## Key Features

- **Vector-based Search**: Semantic similarity for relevant content retrieval
- **Conversational Interface**: Natural language interaction with travel queries
- **Tool Integration**: Dynamic tool selection and execution
- **State Management**: Maintains conversation context across interactions
- **Extensible Architecture**: Easy to add new tools and capabilities

## Customization

**Adding New Destinations:**
```python
UK_DESTINATIONS = [
    "Cornwall",
    "Devon",      # Add new regions
    "Somerset",   # Add new regions
]
```

**Adding New Tools:**
```python
@tool
def weather_forecast(location: str) -> str:
    # Implement weather tool
    pass

TOOLS = [search_travel_info, weather_forecast]
```

## Troubleshooting

**Common Issues:**
- Ensure OpenAI API key is set correctly
- Check internet connection for WikiVoyage downloads
- Verify all dependencies are installed
- Allow time for initial vector store creation

**Performance Notes:**
- Initial setup downloads and processes WikiVoyage pages
- Vector store creation happens once and is cached
- Subsequent queries are fast using cached embeddings

## Dependencies

Core libraries used:
- `langchain` - LLM framework and tools
- `langgraph` - Multi-agent orchestration
- `chromadb` - Vector database
- `openai` - OpenAI API integration
- `beautifulsoup4` - HTML content parsing

See `requirements.txt` for complete dependency list.

## License

Educational purposes. Part of the BBS-AIIM Natural Language Processing course materials.