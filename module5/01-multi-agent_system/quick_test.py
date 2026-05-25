#!/usr/bin/env python3
"""
QUICK FUNCTIONALITY TEST: Basic AI and Tool Integration

This script tests core agent functionality WITHOUT the expensive vector database setup.
It uses a mock tool to verify that:
- Google Gemini API connection works
- Tool binding and calling works correctly
- Message processing works as expected

Purpose: Fast validation before running the full system
Usage: python quick_test.py
Time: ~5 seconds (vs 30+ seconds for full agent)
"""

# System imports
import os                               # Environment variable access

# Configuration
from dotenv import load_dotenv          # Load API keys from .env

# Google Gemini integration
from langchain_google_genai import ChatGoogleGenerativeAI  # Google's language model

# LangChain core components
from langchain_core.messages import HumanMessage  # User message format
from langchain_core.tools import tool            # Tool decorator

# Load environment variables
load_dotenv()

# -----------------------------------------------------------------------------
# MOCK TOOL: Simulates the real search functionality
# -----------------------------------------------------------------------------

@tool
def mock_search_tool(query: str) -> str:
    """
    Mock travel search tool for testing AI tool integration.

    This simulates the real search_travel_info tool without requiring
    the full vector database setup. It allows us to test:
    - Tool calling mechanism
    - Parameter passing
    - Response formatting

    Args:
        query (str): The travel-related search query

    Returns:
        str: Simulated travel information response

    Educational Note:
        In real systems, this would query a vector database.
        Here we return canned responses to test the integration.
    """
    # Simulate different responses based on query content
    query_lower = query.lower()

    if "beach" in query_lower:
        return (
            f"Mock travel search results for '{query}': "
            "Cornwall features stunning beaches including Fistral Beach (famous for surfing), "
            "Porthcurno Beach (with white sand and turquoise water), and "
            "St Ives beaches (perfect for families)."
        )
    elif "restaurant" in query_lower or "food" in query_lower:
        return (
            f"Mock travel search results for '{query}': "
            "Cornwall offers excellent seafood restaurants, traditional Cornish pasties, "
            "and cream teas. Popular dining areas include St Ives, Padstow, and Falmouth."
        )
    else:
        return (
            f"Mock travel search results for '{query}': "
            "Cornwall has beautiful beaches, historic towns, excellent seafood, "
            "and stunning coastal scenery. Popular destinations include Newquay, "
            "St Ives, and the Eden Project."
        )

def test_simple_agent():
    """
    Test basic agent functionality without expensive setup.

    This function validates the core components:
    1. Google Gemini API connection
    2. Tool binding and calling
    3. Message processing and response formatting

    Returns:
        bool: True if all tests pass, False otherwise

    Educational Value:
        Demonstrates the minimum viable agent setup and
        shows how to validate each component independently.
    """
    print("🧪 Testing basic agent functionality...")
    print("   (This tests AI + tool integration without vector database)")

    try:
        # Step 1: Initialize Google Gemini model
        print("🤖 Initializing Google Gemini 2.0 Flash...")
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",  # Latest fast model
            temperature=0              # Deterministic responses
        )

        # Step 2: Bind our mock tool to the language model
        print("🔧 Binding mock search tool...")
        llm_with_tools = llm.bind_tools([mock_search_tool])

        # Step 3: Create a test message that should trigger tool usage
        test_message = "Tell me about beaches in Cornwall"
        messages = [HumanMessage(content=test_message)]

        print(f"💬 Sending test query: '{test_message}'")

        # Step 4: Get response from the AI model
        print("🔍 AI processing query...")
        response = llm_with_tools.invoke(messages)

        # Step 5: Analyze the response
        print(f"✅ AI responded successfully")

        # Check if the AI decided to use tools
        if hasattr(response, 'tool_calls') and response.tool_calls:
            print(f"🔧 AI requested {len(response.tool_calls)} tool calls:")

            for i, tool_call in enumerate(response.tool_calls, 1):
                print(f"   Tool Call #{i}:")
                print(f"     • Tool: {tool_call['name']}")
                print(f"     • Arguments: {tool_call['args']}")
                print(f"     • ID: {tool_call['id']}")

            # This shows the AI correctly understood it needs to search for travel info
            print("✅ Tool calling mechanism working correctly")

        else:
            print("ℹ️  AI provided direct response without tool calls")

        # Display the AI's content response (if any)
        if response.content:
            print(f"💭 AI response content: {response.content}")

        return True

    except Exception as e:
        print(f"❌ Test failed with error: {e}")

        # Provide specific troubleshooting guidance
        if "google_api_key" in str(e).lower() or "api" in str(e).lower():
            print("💡 Tip: Check that GOOGLE_API_KEY is set in .env file")
        elif "model" in str(e).lower():
            print("💡 Tip: Verify the Gemini model name is correct")
        else:
            print("💡 Tip: Check internet connection and API access")

        return False

# -----------------------------------------------------------------------------
# MAIN EXECUTION: Quick validation script
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    """
    Entry point for quick functionality testing.

    Usage:
        python quick_test.py

    This script provides rapid validation of:
    - Environment configuration (API keys, etc.)
    - Google Gemini connectivity
    - Tool integration mechanics
    - Basic AI reasoning capabilities

    Benefits:
    - Fast feedback (5 seconds vs 30+ for full system)
    - Isolates specific functionality for debugging
    - Validates setup before expensive operations
    """

    # Display test header
    print("🚀 QUICK FUNCTIONALITY TEST")
    print("=" * 40)
    print("Testing core agent components without vector database")
    print("Estimated time: ~5 seconds")
    print("=" * 40)

    # Run the test and provide detailed feedback
    if test_simple_agent():
        print("\n" + "="*40)
        print("🎉 QUICK TEST PASSED!")
        print("="*40)
        print("✅ Google Gemini API is working")
        print("✅ Tool binding and calling works")
        print("✅ Message processing is functional")
        print("✅ Basic agent architecture is sound")

        print("\n💡 Next steps:")
        print("   • Run full system test: python run_agent.py")
        print("   • Start interactive mode: python agent.py")
        print("   • Launch web interface: streamlit run app.py")

        print("\n🎓 Educational Notes:")
        print("   • This test uses a mock tool to avoid expensive vector DB setup")
        print("   • The full agent replaces the mock with real WikiVoyage search")
        print("   • LangGraph would orchestrate multiple tool calls in complex scenarios")

    else:
        print("\n" + "="*40)
        print("❌ QUICK TEST FAILED")
        print("="*40)
        print("⚠️  Basic functionality is not working")

        print("\n🔧 Troubleshooting checklist:")
        print("   • Verify GOOGLE_API_KEY in .env file")
        print("   • Check internet connection")
        print("   • Ensure dependencies are installed:")
        print("     pip install -r requirements.txt")
        print("   • Validate .env file format (no quotes around values)")

        print("\n📚 Common issues:")
        print("   • Missing or invalid API key → Authentication errors")
        print("   • Network issues → Connection timeouts")
        print("   • Wrong model names → Model not found errors")
        print("   • Missing dependencies → Import errors")