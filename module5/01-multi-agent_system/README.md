# Multi-Agent Travel Assistant

LangGraph-based travel assistant for Cornwall, England using vector search on WikiVoyage content.

## Quick Start

```bash
# 1. Create environment
python3 -m venv myagent
source myagent/bin/activate  # Linux/Mac
# myagent\Scripts\activate   # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set API key
cp .env.example .env
# Edit .env and add your OpenAI API key

# 4. Test
python test_agent.py

# 5. Run Web UI
./start_ui.sh        # Linux/Mac
# start_ui.bat       # Windows

# Alternative: Command line
python run_agent.py
```

## What it does

- Downloads WikiVoyage pages for Cornwall regions
- Creates vector embeddings for semantic search
- Answers travel questions using LangGraph agent
- Provides information about beaches, attractions, activities

## Files

- `agent.py` - Main multi-agent implementation
- `app.py` - Streamlit web UI
- `start_ui.sh/.bat` - Web UI startup scripts
- `test_agent.py` - Verify setup and dependencies
- `run_agent.py` - Single query test
- `quick_test.py` - Basic functionality test
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection (for WikiVoyage downloads)

## Example Usage

**Web Interface**: Clean chat interface at `http://localhost:8501`
- Real-time conversation with the travel agent
- Example questions provided in the sidebar
- Status indicators for API key and agent loading

**Command Line**: Direct agent interaction
```python
User: "What are the best beaches in Cornwall?"
Agent: Lists 10 top Cornwall beaches with descriptions
```

## Customization

Add destinations in `agent.py`:
```python
UK_DESTINATIONS = [
    "Cornwall",
    "Devon",  # Add new regions
]
```

## Architecture

- **Vector Store**: Chroma with OpenAI embeddings
- **Search Tool**: Semantic similarity search
- **Agent**: LangGraph state management
- **Data**: WikiVoyage travel content

## Troubleshooting

- Check OpenAI API key in `.env`
- Ensure internet connection for downloads
- First run downloads and processes content (takes time)
- Use `test_agent.py` to verify setup

Educational project for BBS-AIIM NLP course.