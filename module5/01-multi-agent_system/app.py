#!/usr/bin/env python3
"""
STREAMLIT WEB INTERFACE FOR CORNWALL TRAVEL ASSISTANT

This creates a modern, user-friendly web interface for the travel agent using Streamlit.
Features:
- Clean chat interface with message history
- Real-time status monitoring (API key, agent loading)
- Example questions to help users get started
- Responsive design that works on mobile and desktop

To run: streamlit run app.py
Access: http://localhost:8501

Educational demonstration of how to create production-ready AI applications
with proper error handling, user experience, and visual design.
"""

# Web framework and UI
import streamlit as st        # Modern web app framework for ML/AI applications

# System and configuration
import os                     # Operating system interface
from dotenv import load_dotenv  # Environment variable management

# LangChain integration
from langchain_core.messages import HumanMessage  # Message format for agent communication

# Load environment variables (API keys, etc.)
load_dotenv()

# -----------------------------------------------------------------------------
# STREAMLIT CONFIGURATION
# -----------------------------------------------------------------------------

# Configure the web page appearance and behavior
st.set_page_config(
    page_title="Cornwall Travel Assistant",  # Browser tab title
    page_icon="🏖️",                         # Browser tab icon
    layout="wide"                           # Use full width of browser
)

# -----------------------------------------------------------------------------
# AGENT INITIALIZATION WITH CACHING
# -----------------------------------------------------------------------------

@st.cache_resource
def load_agent():
    """
    Load the travel agent with Streamlit caching for performance.

    The @st.cache_resource decorator ensures that the expensive agent
    initialization (building vector database, loading models) only
    happens once, even when users refresh the page or multiple users
    access the app simultaneously.

    Returns:
        travel_info_agent: The initialized LangGraph agent, or None if loading fails

    Note:
        This is a key performance optimization for production deployment.
        Without caching, each page refresh would rebuild the entire
        knowledge base, taking 30+ seconds.
    """
    try:
        # Import the pre-built agent from agent.py
        # This triggers the full initialization process on first load
        from agent import travel_info_agent
        return travel_info_agent
    except Exception as e:
        # Display error in the web interface
        st.error(f"❌ Failed to load agent: {e}")
        return None

# -----------------------------------------------------------------------------
# MAIN APPLICATION INTERFACE
# -----------------------------------------------------------------------------

def main():
    """
    Main Streamlit application interface.

    This function creates the complete web interface including:
    - Header with branding
    - Sidebar with status information and help
    - Main chat interface
    - Example questions for user guidance
    """

    # -----------------------------------------------------------------------------
    # PAGE HEADER
    # -----------------------------------------------------------------------------
    st.title("🏖️ Cornwall Travel Assistant")
    st.markdown("*Your AI-powered guide to Cornwall, England*")
    st.markdown("---")

    # -----------------------------------------------------------------------------
    # SIDEBAR: Status monitoring and information
    # -----------------------------------------------------------------------------
    with st.sidebar:
        # About section - explain the technology
        st.header("ℹ️ About This System")
        st.markdown("""
        **Educational AI Travel Assistant** demonstrating:

        🧠 **Google Gemini 2.0 Flash**
        Advanced language model for natural conversation

        🔍 **Semantic Vector Search**
        Find relevant travel info using meaning, not just keywords

        📊 **LangGraph Multi-Agent**
        Orchestrated AI system with tool calling capabilities

        📚 **WikiVoyage Knowledge Base**
        Real travel content about Cornwall destinations

        🌐 **Streamlit Web Interface**
        Production-ready user experience
        """)

        st.markdown("---")

        # System status monitoring
        st.header("🔧 System Status")

        # Check API key configuration
        api_key = os.environ.get('GOOGLE_API_KEY')
        if api_key and api_key != "your_google_api_key_here":
            st.success("✅ Google API Key configured")
        else:
            st.error("❌ No Google API Key found")
            st.info("💡 Add GOOGLE_API_KEY to .env file")
            st.stop()  # Stop execution if no API key

        # Load and validate agent
        with st.spinner("🏗️ Initializing AI agent..."):
            agent = load_agent()

        if agent:
            st.success("✅ Travel agent ready")
        else:
            st.error("❌ Agent initialization failed")
            st.stop()  # Stop execution if agent fails

    # -----------------------------------------------------------------------------
    # MAIN CHAT INTERFACE
    # -----------------------------------------------------------------------------
    st.header("💬 Chat with Your Travel Agent")

    # Initialize chat history using Streamlit session state
    # Session state persists data across user interactions within the same browser session
    if "messages" not in st.session_state:
        st.session_state.messages = []

        # Add a welcoming first message to guide users
        welcome_message = (
            "Hello! I'm your Cornwall travel assistant powered by AI. "
            "I have access to comprehensive travel information about Cornwall, England. "
            "\n\n🏖️ Ask me about beaches, surfing spots, and coastal attractions"
            "\n🏛️ Discover historic sites, museums, and cultural experiences"
            "\n🍽️ Find restaurants, local cuisine, and dining recommendations"
            "\n🚗 Get advice on transportation, accommodation, and trip planning"
            "\n\nWhat would you like to know about Cornwall?"
        )

        st.session_state.messages.append({
            "role": "assistant",
            "content": welcome_message
        })

    # Display conversation history
    # Streamlit's chat_message creates properly formatted chat bubbles
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # -----------------------------------------------------------------------------
    # CHAT INPUT AND PROCESSING
    # -----------------------------------------------------------------------------

    # Streamlit's chat_input creates a text input at the bottom of the page
    if prompt := st.chat_input("Ask me about Cornwall... 🏖️"):

        # Add user message to conversation history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display the user's message immediately
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display AI response
        with st.chat_message("assistant"):
            # Show thinking indicator while processing
            with st.spinner("🔍 Searching travel information..."):
                try:
                    # Create agent state with user's question
                    # Note: Each query starts fresh - we don't maintain conversation context
                    # This is a design choice for this demo; production systems might maintain history
                    state = {"messages": [HumanMessage(content=prompt)]}

                    # Invoke the LangGraph agent
                    # This triggers the full agent pipeline:
                    # 1. AI analyzes the question
                    # 2. AI decides if it needs to search for information
                    # 3. If needed, search tool is called to query WikiVoyage content
                    # 4. AI synthesizes the information into a comprehensive response
                    result = agent.invoke(state)

                    # Extract the final response from the agent
                    response_msg = result["messages"][-1]

                    # Handle Google Gemini's structured response format
                    # Gemini returns responses as structured data that we need to extract
                    content = response_msg.content
                    if isinstance(content, list) and len(content) > 0:
                        # Extract text from Gemini's structured response
                        if isinstance(content[0], dict) and 'text' in content[0]:
                            response = content[0]['text']
                        else:
                            response = str(content[0])
                    else:
                        response = str(content)

                    # Display the response in the chat interface
                    st.markdown(response)

                    # Add assistant's response to conversation history
                    st.session_state.messages.append({"role": "assistant", "content": response})

                except Exception as e:
                    # Handle errors gracefully with user-friendly messages
                    error_msg = f"❌ Sorry, I encountered a technical issue: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

    # -----------------------------------------------------------------------------
    # EXAMPLE QUESTIONS: Help users get started
    # -----------------------------------------------------------------------------
    st.header("💡 Example Questions to Get You Started")
    st.markdown("Click on any question below to see how the AI assistant works:")

    # Create two columns for better layout
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **🏖️ Beaches & Coastal Activities**
        - "What are the best beaches in Cornwall?"
        - "Tell me about surfing spots near Newquay"
        - "Which beaches are safest for families with children?"
        - "Where can I find secluded, quiet beaches?"
        """)

        st.markdown("""
        **🏛️ Attractions & Culture**
        - "What should I visit in St Ives?"
        - "Tell me about the Eden Project"
        - "What are Cornwall's must-see historic sites?"
        - "Where can I see traditional Cornish culture?"
        """)

    with col2:
        st.markdown("""
        **🍽️ Food & Dining**
        - "Where can I find the best seafood in Cornwall?"
        - "What is traditional Cornish cuisine?"
        - "Best restaurants in Falmouth with sea views?"
        - "Where should I try a proper Cornish pasty?"
        """)

        st.markdown("""
        **🚗 Travel Planning**
        - "What's the best way to get around Cornwall?"
        - "When is the best time to visit Cornwall?"
        - "Which towns should I include in a 5-day itinerary?"
        - "How do I plan a Cornwall road trip?"
        """)

    # -----------------------------------------------------------------------------
    # UTILITY FUNCTIONS
    # -----------------------------------------------------------------------------
    st.markdown("---")

    # Clear conversation button
    if st.button("🗑️ Clear Conversation", help="Start a fresh conversation"):
        st.session_state.messages = []
        st.rerun()  # Refresh the page to show cleared state

# -----------------------------------------------------------------------------
# APPLICATION ENTRY POINT
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    """
    Entry point when running the Streamlit app.

    Usage:
        streamlit run app.py

    This creates a web server accessible at http://localhost:8501
    with the full travel assistant interface.

    The app demonstrates:
    - Modern web UI for AI applications
    - Real-time status monitoring
    - Error handling and user feedback
    - Production-ready design patterns
    """
    main()