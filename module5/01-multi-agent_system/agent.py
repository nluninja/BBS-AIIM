# =============================================================================
# CORNWALL TRAVEL ASSISTANT - MULTI-AGENT SYSTEM WITH LANGGRAPH
# =============================================================================
#
# This is a complete multi-agent system for travel assistance using:
# - LangGraph for agent orchestration
# - Google Gemini 2.0 Flash for language understanding
# - Chroma vector database for semantic search
# - WikiVoyage content as knowledge base
#
# Educational demonstration of modern AI agent architecture
# =============================================================================

# -----------------------------------------------------------------------------
# Import libraries
# -----------------------------------------------------------------------------

# Standard library imports
import os              # Environment variable access
import asyncio         # Asynchronous programming
import operator        # Operator functions for state management
import json           # JSON handling for tool messages
from typing import Annotated, Sequence, TypedDict  # Type hints

# Configuration management
from dotenv import load_dotenv  # Load environment variables from .env file

# Vector database and web scraping (modern standalone packages)
from langchain_chroma import Chroma                    # Vector database (replaces deprecated langchain_community)
import aiohttp                                         # Async HTTP client for web scraping
from bs4 import BeautifulSoup                         # HTML parsing and text extraction

# LangChain components for document processing and AI integration
from langchain_text_splitters import RecursiveCharacterTextSplitter  # Split documents into chunks
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings  # Google Gemini integration
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage  # Message types for agent communication
from langchain_core.documents import Document         # Document structure for knowledge base
from langchain_core.tools import tool                # Decorator for creating tools

# LangGraph for multi-agent orchestration
from langgraph.graph import StateGraph, END          # Graph-based agent framework
from langgraph.prebuilt import tools_condition       # Pre-built condition for tool execution

# -----------------------------------------------------------------------------
# CONFIGURATION: Load environment variables and define data sources
# -----------------------------------------------------------------------------

load_dotenv()  # Load API keys and configuration from .env file
# This loads GOOGLE_API_KEY and other environment variables

# -----------------------------------------------------------------------------
# KNOWLEDGE BASE CONFIGURATION
# -----------------------------------------------------------------------------
# Define the geographic regions we want to include in our travel knowledge base
# These correspond to WikiVoyage pages that will be scraped and embedded

UK_DESTINATIONS = [
    "Cornwall",        # Main Cornwall page - general information
    "North_Cornwall",  # Northern coastal region - surfing beaches
    "South_Cornwall",  # Southern coastal region - sheltered bays
    "West_Cornwall",   # Western peninsula - dramatic cliffs and coves
]
# Note: These map to URLs like https://en.wikivoyage.org/wiki/Cornwall

# -----------------------------------------------------------------------------
# CUSTOM WEB SCRAPER: Replace deprecated langchain_community.AsyncHtmlLoader
# -----------------------------------------------------------------------------
# Modern replacement for deprecated AsyncHtmlLoader using aiohttp and BeautifulSoup

async def load_html_documents(urls: list[str]) -> list[Document]:
    """
    Asynchronously load and parse HTML documents from WikiVoyage URLs.

    This is our custom implementation to replace the deprecated
    langchain_community.AsyncHtmlLoader. It provides better control
    over HTTP headers, error handling, and content processing.

    Args:
        urls: List of WikiVoyage URLs to scrape

    Returns:
        List of Document objects with parsed text content and metadata
    """
    documents = []

    # Configure HTTP headers to mimic a real browser and avoid blocking
    # Many websites block requests without proper user agent headers
    headers = {
        'User-Agent': os.environ.get('USER_AGENT', 'BBS-Travel-Assistant/1.0 (Educational Project)'),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',      # Prefer English content
        'Accept-Encoding': 'gzip, deflate',        # Support compression
        'DNT': '1',                                # Do Not Track header
        'Connection': 'keep-alive',                # Reuse connections
        'Upgrade-Insecure-Requests': '1'           # HTTPS preference
    }

    # Use async context manager for efficient connection pooling
    async with aiohttp.ClientSession(headers=headers) as session:
        # Create concurrent tasks for all URLs (parallel processing)
        tasks = []
        for url in urls:
            tasks.append(fetch_and_parse(session, url))

        # Execute all requests concurrently and handle any exceptions
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results and create Document objects
        for url, result in zip(urls, results):
            if isinstance(result, Exception):
                print(f"⚠️  Error loading {url}: {result}")
                continue  # Skip failed URLs, don't crash the entire process

            # Create LangChain Document with content and metadata
            documents.append(Document(
                page_content=result,           # The cleaned text content
                metadata={"source": url}       # Source URL for reference
            ))

    return documents


async def fetch_and_parse(session: aiohttp.ClientSession, url: str) -> str:
    """
    Fetch a single HTML page and extract clean text content.

    This function handles the HTTP request, HTML parsing, and text cleaning.
    It's designed to be respectful to servers and extract only meaningful content.

    Args:
        session: aiohttp session for HTTP requests
        url: URL to fetch

    Returns:
        Cleaned text content from the webpage

    Raises:
        Exception: If the request fails or returns non-200 status
    """
    try:
        # Be respectful to the server - add delay between requests
        # This prevents overwhelming WikiVoyage servers
        await asyncio.sleep(0.5)  # 500ms delay

        async with session.get(url) as response:
            if response.status == 200:
                # Get the HTML content
                html = await response.text()

                # Parse HTML with BeautifulSoup
                soup = BeautifulSoup(html, 'html.parser')

                # Remove non-content elements that would add noise
                # to our knowledge base (scripts, styles, navigation, etc.)
                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.extract()

                # Extract clean text content
                text = soup.get_text()

                # Clean up whitespace: remove extra spaces, newlines, tabs
                # This creates cleaner, more consistent text for embedding
                text = ' '.join(text.split())

                return text
            else:
                raise Exception(f"HTTP {response.status}")

    except Exception as e:
        raise Exception(f"Failed to fetch {url}: {e}")

async def build_vectorstore(destinations: Sequence[str]) -> Chroma:
    """
    Create a vector database from WikiVoyage travel content.

    This is the core knowledge base creation process:
    1. Download web pages from WikiVoyage
    2. Split content into manageable chunks
    3. Create embeddings using Google Gemini
    4. Store in Chroma vector database

    Args:
        destinations: List of WikiVoyage page names (e.g., "Cornwall")

    Returns:
        Chroma vector store ready for semantic search
    """
    # Step 1: Convert destination names to WikiVoyage URLs
    urls = [f"https://en.wikivoyage.org/wiki/{slug}" for slug in destinations]
    print(f"📥 Downloading {len(urls)} destination pages...")

    # Step 2: Download and parse HTML content asynchronously
    docs = await load_html_documents(urls)
    print(f"✅ Successfully loaded {len(docs)} pages")

    # Step 3: Split documents into chunks for better embedding and retrieval
    # Smaller chunks provide more focused, relevant results
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1024,        # Each chunk max 1024 characters
        chunk_overlap=128       # 128 character overlap to preserve context
    )

    # Apply splitter to all documents and flatten into single list
    chunks = sum([splitter.split_documents([d]) for d in docs], [])

    # Step 4: Create embeddings and store in vector database
    print(f"🧠 Creating embeddings for {len(chunks)} text chunks...")

    # Use Google Gemini's embedding model to convert text to vectors
    # These vectors capture semantic meaning for similarity search
    embedding_model = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"  # Latest Google embedding model
    )

    # Create Chroma vector database from documents and embeddings
    vectordb_client = Chroma.from_documents(
        chunks,                  # The text chunks to embed
        embedding=embedding_model # The embedding model to use
    )

    print("✅ Vector store ready for semantic search!\n")
    return vectordb_client


# -----------------------------------------------------------------------------
# SINGLETON PATTERN: Initialize vector database once at startup
# -----------------------------------------------------------------------------
# This implements the singleton pattern to ensure we only build the expensive
# vector database once, even if the module is imported multiple times.

# Global variable to cache the vector store instance
_ti_vectorstore_client: Chroma | None = None


def get_travel_info_vectorstore() -> Chroma:
    """
    Get or create the travel information vector store.

    This function implements lazy initialization with singleton pattern:
    - First call: builds the vector database from WikiVoyage content
    - Subsequent calls: returns the cached instance

    Returns:
        Chroma vector store containing travel information

    Raises:
        RuntimeError: If GOOGLE_API_KEY environment variable is not set
    """
    global _ti_vectorstore_client

    # Check if we already have a built vector store (singleton check)
    if _ti_vectorstore_client is None:
        # Validate that we have the required API key
        if not os.environ.get("GOOGLE_API_KEY"):
            raise RuntimeError(
                "❌ GOOGLE_API_KEY environment variable is required!\n"
                "Please add your Google API key to the .env file:\n"
                "GOOGLE_API_KEY=your_actual_api_key_here"
            )

        print("🏗️  Initializing travel knowledge base...")
        # Build the vector store asynchronously (this takes time on first run)
        _ti_vectorstore_client = asyncio.run(
            build_vectorstore(UK_DESTINATIONS)
        )

    return _ti_vectorstore_client


# Initialize the vector store at module load time
# This happens when the agent.py file is imported
print("🚀 Starting Cornwall Travel Assistant...")
ti_vectorstore_client = get_travel_info_vectorstore()

# Create a retriever interface for semantic search
# This converts the vector store into a tool that can find relevant documents
ti_retriever = ti_vectorstore_client.as_retriever(
    search_kwargs={"k": 4}  # Return top 4 most relevant chunks
)


# -----------------------------------------------------------------------------
# TOOL DEFINITION: Semantic search capability for the agent
# -----------------------------------------------------------------------------
# Tools are functions that the AI agent can call to perform specific tasks.
# This tool enables the agent to search through our travel knowledge base.

@tool
def search_travel_info(query: str) -> str:
    """
    Search through WikiVoyage travel content using semantic similarity.

    This is the core tool that gives our agent access to travel knowledge.
    It uses vector similarity search to find the most relevant information
    from our embedded WikiVoyage content about Cornwall and surrounding areas.

    The @tool decorator automatically makes this function available to the
    LangGraph agent as a callable tool.

    Args:
        query (str): Natural language search query about travel destinations
                    Examples: "best beaches in Cornwall", "restaurants in St Ives"

    Returns:
        str: Combined text from the most relevant document chunks,
             separated by "---" dividers for clarity

    Example:
        >>> search_travel_info("surfing beaches Cornwall")
        Returns information about Fistral Beach, Watergate Bay, etc.
    """
    # Perform semantic search using the vector store retriever
    # This finds documents most similar to the query's meaning (not just keywords)
    docs = ti_retriever.invoke(query)

    # Ensure we have a list of documents (defensive programming)
    top_docs = docs[:4] if isinstance(docs, list) else docs

    # Combine the most relevant chunks into a single response
    # Use "---" as separator to help the AI distinguish between different sources
    combined_content = "\n---\n".join(
        doc.page_content for doc in top_docs
    )

    return combined_content

# -----------------------------------------------------------------------------
# LANGUAGE MODEL CONFIGURATION: Google Gemini with Tool Integration
# -----------------------------------------------------------------------------
# Configure the AI language model to work with our search tool.

# List of all tools available to the agent
# In this system, we have one tool for searching travel information
TOOLS = [search_travel_info]

# Initialize Google Gemini 2.0 Flash model
# This is Google's fast, efficient LLM suitable for conversational applications
llm_model = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",  # Latest version of Gemini Flash
    temperature=0                 # Deterministic responses (no randomness)
)

# Bind tools to the language model
# This tells Gemini what tools it can call and how to use them
# The model will automatically decide when to call tools based on user queries
llm_with_tools = llm_model.bind_tools(TOOLS)

print(f"🤖 Language model initialized: {llm_model.model}")
print(f"🛠️  Available tools: {[tool.name for tool in TOOLS]}")

# -----------------------------------------------------------------------------
# LANGGRAPH AGENT CONFIGURATION
# -----------------------------------------------------------------------------
# LangGraph uses a state-based approach where the agent's state flows through
# different nodes in a graph. Each node can modify the state and pass it along.

# -----------------------------------------------------------------------------
# Agent State Definition
# -----------------------------------------------------------------------------
class AgentState(TypedDict):
    """
    The state that flows through our LangGraph agent.

    In LangGraph, state represents all the information that needs to be
    passed between different nodes in the agent graph. Our agent state
    is simple: it just tracks the conversation messages.

    The Annotated type with operator.add means that when multiple nodes
    add to the messages list, they will be combined (not replaced).
    """
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # This creates a list of messages that grows as the conversation continues
    # - HumanMessage: User input
    # - AIMessage: Assistant responses
    # - ToolMessage: Results from tool calls

# -----------------------------------------------------------------------------
# TOOL EXECUTION NODE: Custom node for executing tools called by the AI
# -----------------------------------------------------------------------------

class ToolsExecutionNode:
    """
    Custom LangGraph node that executes tools requested by the AI model.

    When the AI decides it needs information to answer a question, it will
    generate tool calls. This node intercepts those calls, executes the
    actual tools, and returns the results as ToolMessages.

    This is a key component of the agent architecture: it bridges the gap
    between the AI's decision to use a tool and the actual tool execution.
    """

    def __init__(self, tools: Sequence):
        """
        Initialize the tool execution node with available tools.

        Args:
            tools: List of tools that can be executed by this node
        """
        # Create a lookup dictionary for fast tool access by name
        self._tools_by_name = {tool.name: tool for tool in tools}
        print(f"🔧 Tool execution node initialized with: {list(self._tools_by_name.keys())}")

    def __call__(self, state: dict) -> dict:
        """
        Execute tools requested in the last AI message.

        This method is called by LangGraph when the agent flow reaches
        this node. It examines the last message for tool calls and
        executes them.

        Args:
            state: Current agent state containing conversation messages

        Returns:
            dict: Updated state with tool execution results
        """
        # Extract messages from the current state
        messages: Sequence[BaseMessage] = state.get("messages", [])

        # Get the most recent message (should be an AI message with tool calls)
        last_msg = messages[-1]

        # Prepare list to collect tool execution results
        tool_messages: list[ToolMessage] = []

        # Extract tool calls from the AI's message
        # The AI model puts tool calls in the 'tool_calls' attribute
        tool_calls = getattr(last_msg, "tool_calls", [])

        print(f"🔍 Executing {len(tool_calls)} tool calls...")

        # Execute each tool call
        for tool_call in tool_calls:
            tool_name = tool_call["name"]           # Which tool to call
            tool_args = tool_call["args"]           # Arguments for the tool
            tool_call_id = tool_call["id"]          # Unique ID for this call

            # Get the actual tool function
            tool = self._tools_by_name[tool_name]

            print(f"  🛠️  Calling {tool_name} with args: {tool_args}")

            # Execute the tool with the provided arguments
            result = tool.invoke(tool_args)

            # Create a ToolMessage with the result
            # This will be added to the conversation history
            tool_messages.append(
                ToolMessage(
                    content=result,              # The actual tool result
                    name=tool_name,             # Tool that produced this result
                    tool_call_id=tool_call_id,  # Link back to the original call
                )
            )

        print(f"✅ Tool execution completed, returning {len(tool_messages)} results")

        # Return the new messages to be added to state
        return {"messages": tool_messages}


# Create the tool execution node instance
# This will be used as a node in our LangGraph
tools_execution_node = ToolsExecutionNode(TOOLS)


# -----------------------------------------------------------------------------
# LLM NODE: The brain of our agent
# -----------------------------------------------------------------------------

def llm_node(state: AgentState) -> dict:
    """
    The main reasoning node where the AI model processes messages and decides actions.

    This is where the "intelligence" happens. The AI model:
    1. Reads all the conversation messages
    2. Decides whether it needs more information (tool calls)
    3. Either calls tools or provides a final answer

    This node is called repeatedly until the AI decides it has enough
    information to provide a complete answer.

    Args:
        state: Current agent state with conversation messages

    Returns:
        dict: Updated state with AI's response (may include tool calls)
    """
    # Get the full conversation history
    current_messages = state["messages"]

    print(f"🧠 AI processing {len(current_messages)} messages...")

    # Let the AI model process the conversation and decide what to do
    # The model has access to tools and will decide whether to:
    # 1. Call the search_travel_info tool to get more information
    # 2. Provide a final answer based on available information
    response_message = llm_with_tools.invoke(current_messages)

    # Check what the AI decided to do
    if hasattr(response_message, 'tool_calls') and response_message.tool_calls:
        print(f"🔧 AI requested {len(response_message.tool_calls)} tool calls")
    else:
        print("💬 AI provided final answer")

    # Return the AI's response as part of the updated state
    return {"messages": [response_message]}

# -----------------------------------------------------------------------------
# LANGGRAPH CONSTRUCTION: Building the Agent Flow
# -----------------------------------------------------------------------------
# This section creates the actual agent by defining how different nodes
# connect and how information flows between them.

print("🏗️  Building LangGraph agent architecture...")

# Initialize the graph builder with our state structure
builder = StateGraph(AgentState)

# Add nodes to the graph
# Each node is a function that processes the state and returns updates
builder.add_node("llm_node", llm_node)                    # AI reasoning node
builder.add_node("tools", tools_execution_node)           # Tool execution node

# Define conditional flow from LLM node
# The tools_condition function (from LangGraph) automatically decides:
# - If AI made tool calls → go to "tools" node
# - If AI gave final answer → go to END (finish conversation)
builder.add_conditional_edges(
    "llm_node",           # Start from the AI reasoning node
    tools_condition       # Built-in condition that checks for tool calls
)

# Define flow from tools back to LLM
# After tools execute, always return to AI for processing results
builder.add_edge("tools", "llm_node")

# Set the entry point
# Every conversation starts with the AI reasoning node
builder.set_entry_point("llm_node")

# Compile the graph into an executable agent
# This creates the final agent that can process conversations
travel_info_agent = builder.compile()

print("✅ LangGraph agent successfully built!")
print("📊 Agent flow: llm_node → [tools_condition] → tools → llm_node → END")

# -----------------------------------------------------------------------------
# COMMAND-LINE INTERFACE: Interactive chat with the travel agent
# -----------------------------------------------------------------------------

def chat_loop():
    """
    Interactive command-line interface for the Cornwall Travel Assistant.

    This provides a simple way to test and demonstrate the agent.
    Users can ask questions about Cornwall and get AI-powered responses
    backed by real travel information from WikiVoyage.
    """
    # Welcome message
    print("\n" + "="*60)
    print("🏖️  CORNWALL TRAVEL ASSISTANT")
    print("="*60)
    print("Welcome! I can help you discover the best of Cornwall, England.")
    print("Ask me about beaches, attractions, restaurants, or activities.")
    print("Type 'exit' or 'quit' when you're done.")
    print("="*60 + "\n")

    while True:
        # Get user input
        user_input = input("🗣️  You: ").strip()

        # Check for exit conditions
        if user_input.lower() in {"exit", "quit", "bye", "goodbye"}:
            print("\n👋 Thanks for using Cornwall Travel Assistant! Safe travels!")
            break

        # Skip empty inputs
        if not user_input:
            continue

        # Create initial conversation state
        # Each conversation starts fresh with just the user's question
        state = {"messages": [HumanMessage(content=user_input)]}

        try:
            print("🔍 Searching travel information...")

            # Invoke the agent graph with the user's question
            # This triggers the full agent flow:
            # 1. LLM processes the question
            # 2. LLM decides if it needs to search for information
            # 3. If yes, tools are called to search WikiVoyage content
            # 4. LLM synthesizes the information into a helpful response
            result = travel_info_agent.invoke(state)

            # Extract the final response from the conversation
            response_msg = result["messages"][-1]

            # Handle Google Gemini's response format
            # Gemini returns structured responses that we need to extract
            content = response_msg.content
            if isinstance(content, list) and len(content) > 0:
                # Look for text content in the response structure
                if isinstance(content[0], dict) and 'text' in content[0]:
                    text_content = content[0]['text']
                else:
                    text_content = str(content[0])
            else:
                text_content = str(content)

            # Display the assistant's response
            print(f"\n🤖 Assistant: {text_content}\n")
            print("-" * 60 + "\n")

        except Exception as e:
            print(f"\n❌ Sorry, I encountered an error: {e}")
            print("Please try asking your question differently.\n")


# -----------------------------------------------------------------------------
# MAIN EXECUTION: Run the interactive chat when script is executed directly
# -----------------------------------------------------------------------------


if __name__ == "__main__":
    """
    Entry point when running the agent directly from command line.

    Usage:
        python agent.py

    This starts the interactive chat interface where users can ask
    questions about Cornwall travel destinations.
    """
    chat_loop()