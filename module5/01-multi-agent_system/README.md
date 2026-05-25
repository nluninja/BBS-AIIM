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

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
# Create .env file
OPENAI_API_KEY=your_openai_api_key_here
```

3. Download spaCy models (if needed):
```bash
python -m spacy download en_core_web_sm
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