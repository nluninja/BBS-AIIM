#!/usr/bin/env python3
"""
DEMONSTRATION SCRIPT: Single Query Test for Cornwall Travel Agent

This script demonstrates the complete agent system with a single test query.
It shows the full pipeline from question to answer, including:
- Vector database initialization
- WikiVoyage content processing
- AI reasoning and tool usage
- Response formatting

Educational purpose: Show how the agent works end-to-end
Usage: python run_agent.py
"""

# Environment and configuration
from dotenv import load_dotenv          # Load API keys and settings

# LangChain message types
from langchain_core.messages import HumanMessage  # User message format

# Load environment variables (GOOGLE_API_KEY, etc.)
load_dotenv()

def test_agent_query():
    """
    Test the complete agent system with a sample travel query.

    This function demonstrates the full agent pipeline:
    1. Import and initialize the agent (builds knowledge base)
    2. Create a user question as a HumanMessage
    3. Invoke the LangGraph agent
    4. Process and display the response

    Returns:
        bool: True if test succeeds, False if it fails

    Educational Value:
        Shows how to programmatically interact with the agent system
        and handle the various response formats from Google Gemini.
    """
    print("🤖 Initializing Cornwall Travel Agent...")
    print("⏳ This may take a moment on first run (building knowledge base)")

    try:
        # Import the pre-built agent from agent.py
        # This triggers the entire initialization process:
        # - Loading environment variables
        # - Downloading WikiVoyage pages
        # - Creating vector embeddings
        # - Building the LangGraph agent
        from agent import travel_info_agent

        print("✅ Agent loaded successfully!")
        print("📚 Knowledge base ready with Cornwall travel information")

        # Define a test query that will trigger tool usage
        # This question requires searching through the travel content
        test_query = "What are the best beaches in Cornwall?"
        print(f"\n🗣️ User: {test_query}")

        # Create the initial conversation state
        # In LangGraph, state flows through nodes as a dictionary
        state = {"messages": [HumanMessage(content=test_query)]}

        # Invoke the agent graph with our question
        # This starts the agent flow:
        # 1. LLM node processes the question
        # 2. LLM decides it needs travel information
        # 3. Tools node executes search_travel_info
        # 4. LLM node synthesizes the search results into an answer
        print("🔍 Agent is processing your question...")
        print("   • AI analyzing query")
        print("   • Searching travel database")
        print("   • Generating comprehensive response")

        result = travel_info_agent.invoke(state)

        # Extract the final response from the completed conversation
        response_msg = result["messages"][-1]

        # Handle Google Gemini's response format
        # Gemini returns structured responses that need to be parsed
        if hasattr(response_msg, 'content'):
            content = response_msg.content

            # Google Gemini returns responses as lists with structured data
            if isinstance(content, list) and len(content) > 0:
                # Extract text from the structured response
                if isinstance(content[0], dict) and 'text' in content[0]:
                    text_content = content[0]['text']
                else:
                    text_content = str(content[0])
            else:
                # Fallback for simple string responses
                text_content = str(content)
        else:
            # Fallback if content attribute is missing
            text_content = str(response_msg)

        # Display the agent's response
        print(f"\n🤖 Assistant: {text_content}")

        return True

    except Exception as e:
        print(f"❌ Error during agent test: {e}")

        # Print detailed error information for debugging
        import traceback
        print("\n🔍 Debug information:")
        traceback.print_exc()

        return False

# -----------------------------------------------------------------------------
# MAIN EXECUTION: Demonstration script entry point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    """
    Entry point for the agent demonstration script.

    Usage:
        python run_agent.py

    This script provides a quick way to:
    - Test that the agent system is working correctly
    - Demonstrate the agent's capabilities
    - Verify that all dependencies and configurations are correct

    Ideal for:
    - Classroom demonstrations
    - Quick system validation
    - Testing after configuration changes
    """

    # Display header for the demonstration
    print("🚀 CORNWALL TRAVEL ASSISTANT - DEMONSTRATION")
    print("=" * 50)
    print("Educational AI Agent System Demo")
    print("Built with LangGraph + Google Gemini + Vector Search")
    print("=" * 50)

    # Run the test and provide appropriate feedback
    if test_agent_query():
        print("\n" + "="*50)
        print("🎉 DEMONSTRATION SUCCESSFUL!")
        print("="*50)
        print("✅ Agent system is working correctly")
        print("✅ Knowledge base is functioning")
        print("✅ AI responses are properly formatted")
        print("\n💡 Next steps:")
        print("   • Try the interactive version: python agent.py")
        print("   • Launch the web interface: streamlit run app.py")
        print("   • Explore the code in agent.py for implementation details")

    else:
        print("\n" + "="*50)
        print("❌ DEMONSTRATION FAILED")
        print("="*50)
        print("⚠️  The agent system encountered an error")
        print("💡 Troubleshooting:")
        print("   • Check that GOOGLE_API_KEY is set in .env file")
        print("   • Ensure all dependencies are installed (pip install -r requirements.txt)")
        print("   • Verify internet connection for WikiVoyage access")
        print("   • Check the error details above for specific issues")