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

        # Handle different response formats from Google Gemini
        if hasattr(response_msg, 'content'):
            content = response_msg.content
            # If content is a list (like from Google Gemini), extract text
            if isinstance(content, list) and len(content) > 0:
                # Look for text content in the first item
                if isinstance(content[0], dict) and 'text' in content[0]:
                    text_content = content[0]['text']
                else:
                    text_content = str(content[0])
            else:
                text_content = str(content)
        else:
            text_content = str(response_msg)

        print(f"\n🤖 Assistant: {text_content}")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 BBS Travel Assistant Test")
    print("=" * 50)

    if test_agent_query():
        print("\n🎉 Agent test successful!")
        print("💡 The full interactive version can be started with 'python agent.py'")
    else:
        print("\n❌ Agent test failed.")