#!/usr/bin/env python3
"""
Quick test of agent without vector store setup
"""
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

# Load environment
load_dotenv()

# Simple mock tool for testing
@tool
def mock_search_tool(query: str) -> str:
    """Mock search tool that returns sample travel info"""
    return f"Here's some travel information about '{query}': Cornwall has beautiful beaches and coastal towns."

def test_simple_agent():
    """Test basic agent functionality"""
    print("🧪 Testing simple agent setup...")

    try:
        # Create LLM
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

        # Bind tool
        llm_with_tools = llm.bind_tools([mock_search_tool])

        # Test message
        messages = [HumanMessage(content="Tell me about beaches in Cornwall")]

        # Get response
        response = llm_with_tools.invoke(messages)

        print(f"✅ Agent responded: {response.content}")

        if hasattr(response, 'tool_calls') and response.tool_calls:
            print(f"🔧 Tool calls requested: {len(response.tool_calls)}")
            for tool_call in response.tool_calls:
                print(f"   Tool: {tool_call['name']}")
                print(f"   Args: {tool_call['args']}")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Quick Agent Test")
    print("=" * 30)

    if test_simple_agent():
        print("\n🎉 Basic agent functionality works!")
        print("💡 The full agent should work correctly.")
    else:
        print("\n❌ Basic test failed.")