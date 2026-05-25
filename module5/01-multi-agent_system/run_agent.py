#!/usr/bin/env python3
"""
Run the travel agent with a simple test query
"""
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# Load environment
load_dotenv()

def test_agent_query():
    """Test the agent with a sample query"""
    print("🤖 Starting Travel Agent...")

    try:
        # Import agent components
        from agent import travel_info_agent

        print("✅ Agent loaded successfully!")

        # Test query
        test_query = "What are the best beaches in Cornwall?"
        print(f"\n🗣️ User: {test_query}")

        # Create initial state
        state = {"messages": [HumanMessage(content=test_query)]}

        # Get response
        print("🔍 Agent is thinking...")
        result = travel_info_agent.invoke(state)

        # Extract response
        response_msg = result["messages"][-1]
        print(f"\n🤖 Assistant: {response_msg.content}")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Cornwall Travel Assistant Test")
    print("=" * 50)

    if test_agent_query():
        print("\n🎉 Agent test successful!")
        print("💡 The full interactive version can be started with 'python agent.py'")
    else:
        print("\n❌ Agent test failed.")