#!/usr/bin/env python3
"""
Quick test script for the travel agent
"""
import os
import asyncio
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

# Load environment
load_dotenv()

async def test_basic_components():
    """Test basic components without full agent setup"""
    print("🔍 Testing Google Gemini connection...")

    try:
        # Test Google Gemini embeddings
        embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        test_embedding = await embeddings.aembed_query("Hello world")
        print(f"✅ Google Embeddings working - vector size: {len(test_embedding)}")

        # Test Gemini Chat
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
        response = await llm.ainvoke("Say 'Hello from the travel agent test!'")
        print(f"✅ Gemini Chat working - Response: {response.content}")

        return True

    except Exception as e:
        print(f"❌ Error testing components: {e}")
        return False

def test_imports():
    """Test all required imports"""
    print("📦 Testing imports...")

    try:
        from langchain_chroma import Chroma
        import aiohttp
        from bs4 import BeautifulSoup
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_core.messages import HumanMessage, ToolMessage
        from langchain_core.documents import Document
        from langchain_core.tools import tool
        from langgraph.graph import StateGraph, END
        from langgraph.prebuilt import tools_condition

        print("✅ All imports successful (using standalone packages)")
        return True

    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

async def main():
    print("🤖 Travel Agent Test Suite")
    print("=" * 40)

    # Test 1: Imports
    if not test_imports():
        return

    # Test 2: Basic components
    if not await test_basic_components():
        return

    print("\n🎉 All tests passed! The agent should work correctly.")
    print("💡 You can now run 'python agent.py' to start the full agent.")

if __name__ == "__main__":
    asyncio.run(main())