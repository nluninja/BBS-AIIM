#!/usr/bin/env python3
"""
Simple Streamlit web UI for the Cornwall Travel Agent
"""
import streamlit as st
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# Load environment
load_dotenv()

# Page config
st.set_page_config(
    page_title="Cornwall Travel Assistant",
    page_icon="🏖️",
    layout="wide"
)

@st.cache_resource
def load_agent():
    """Load the travel agent (cached for performance)"""
    try:
        from agent import travel_info_agent
        return travel_info_agent
    except Exception as e:
        st.error(f"Failed to load agent: {e}")
        return None

def main():
    """Main Streamlit app"""

    # Header
    st.title("🏖️ Cornwall Travel Assistant")
    st.markdown("*Your AI-powered guide to Cornwall, England*")

    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This travel assistant uses:
        - **Vector Search** through WikiVoyage content
        - **LangGraph** multi-agent system
        - **OpenAI** for natural language processing

        Ask about beaches, attractions, activities, and more in Cornwall!
        """)

        st.header("🔧 Status")

        # Check API key
        api_key = os.environ.get('OPENAI_API_KEY')
        if api_key:
            st.success("✅ API Key loaded")
        else:
            st.error("❌ No API Key found")
            st.info("Add OPENAI_API_KEY to .env file")
            return

        # Load agent
        with st.spinner("Loading travel agent..."):
            agent = load_agent()

        if agent:
            st.success("✅ Agent ready")
        else:
            st.error("❌ Agent failed to load")
            return

    # Main chat interface
    st.header("💬 Chat with Your Travel Agent")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Hello! I'm your Cornwall travel assistant. I can help you discover the best beaches, attractions, restaurants, and activities in Cornwall, England. What would you like to know?"
        })

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me about Cornwall..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Create state and get response
                    state = {"messages": [HumanMessage(content=prompt)]}
                    result = agent.invoke(state)
                    response = result["messages"][-1].content

                    st.markdown(response)

                    # Add to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})

                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

    # Example questions
    st.header("💡 Example Questions")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **🏖️ Beaches & Coast**
        - What are the best beaches in Cornwall?
        - Tell me about surfing spots in Newquay
        - Which beaches are good for families?
        """)

        st.markdown("""
        **🏛️ Attractions & Activities**
        - What should I visit in St Ives?
        - Tell me about Eden Project
        - What are the must-see attractions?
        """)

    with col2:
        st.markdown("""
        **🍽️ Food & Dining**
        - Where can I find good seafood?
        - What's the local cuisine like?
        - Best restaurants in Falmouth?
        """)

        st.markdown("""
        **🚗 Travel & Logistics**
        - How do I get around Cornwall?
        - Best time to visit Cornwall?
        - What towns should I visit?
        """)

    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main()