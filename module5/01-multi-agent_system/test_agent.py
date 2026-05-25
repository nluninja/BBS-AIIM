#!/usr/bin/env python3
"""
COMPREHENSIVE TEST SUITE: Validate all agent components

This script provides thorough testing of the travel agent system by:
1. Testing all required imports and dependencies
2. Validating Google Gemini API connections
3. Testing embedding model functionality
4. Verifying chat model responses

Purpose: Comprehensive validation before deploying or demonstrating the system
Usage: python test_agent.py
Scope: Tests individual components without building full knowledge base
"""

# System imports
import os                               # Operating system interface
import asyncio                          # Asynchronous programming support

# Configuration
from dotenv import load_dotenv          # Environment variable management

# Google Gemini integration components
from langchain_google_genai import (
    ChatGoogleGenerativeAI,             # Google's conversational AI model
    GoogleGenerativeAIEmbeddings        # Google's text embedding model
)

# Load environment configuration
load_dotenv()

async def test_basic_components():
    """
    Test core Google Gemini components independently.

    This async function validates that both embedding and chat models
    are working correctly with our API configuration. It tests:
    - Embedding model for vector search capability
    - Chat model for conversational AI capability

    Returns:
        bool: True if all components work, False otherwise

    Educational Value:
        Shows how to test AI components independently before integration.
        Demonstrates async programming with AI models.
    """
    print("🔍 Testing Google Gemini API integration...")

    try:
        # Test 1: Google Gemini Embeddings
        print("   📊 Testing embedding model...")
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"  # Latest Google embedding model
        )

        # Test embedding generation with a simple query
        test_text = "Hello world, this is a test of semantic embeddings"
        test_embedding = await embeddings.aembed_query(test_text)

        print(f"   ✅ Embeddings working - Vector size: {len(test_embedding)}")
        print(f"   📈 Vector dimensions indicate model: {len(test_embedding)}D space")

        # Test 2: Google Gemini Chat Model
        print("   🤖 Testing chat model...")
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",  # Fast, efficient conversational model
            temperature=0               # Deterministic for testing
        )

        # Test with a simple conversation
        test_prompt = "Say 'Hello from the travel agent test!' and confirm you can help with travel questions."
        response = await llm.ainvoke(test_prompt)

        print(f"   ✅ Chat model working")
        print(f"   💬 Response: {response.content}")

        # Validate response quality
        if "travel" in response.content.lower():
            print("   ✅ Model understands travel context")
        else:
            print("   ⚠️  Model response doesn't mention travel (but still working)")

        return True

    except Exception as e:
        print(f"   ❌ Component test failed: {e}")

        # Provide specific debugging guidance
        error_str = str(e).lower()
        if "api_key" in error_str or "authentication" in error_str:
            print("   💡 Check GOOGLE_API_KEY in .env file")
        elif "model" in error_str:
            print("   💡 Verify model names are correct")
        elif "quota" in error_str or "limit" in error_str:
            print("   💡 Check API quota and billing")
        else:
            print("   💡 Check internet connection and firewall settings")

        return False

def test_imports():
    """
    Test all required imports for the agent system.

    This validates that all dependencies are properly installed
    and can be imported. It's especially important after migration
    from deprecated packages to standalone alternatives.

    Returns:
        bool: True if all imports succeed, False otherwise

    Educational Value:
        Shows the complete dependency stack for a modern AI agent system.
        Demonstrates the migration from deprecated langchain_community.
    """
    print("📦 Testing imports and dependencies...")

    try:
        # Modern vector database integration (standalone package)
        print("   🔗 Testing vector database imports...")
        from langchain_chroma import Chroma

        # Web scraping components (replacement for deprecated AsyncHtmlLoader)
        print("   🌐 Testing web scraping imports...")
        import aiohttp                    # Async HTTP client
        from bs4 import BeautifulSoup    # HTML parsing

        # LangChain core components
        print("   🧠 Testing LangChain core imports...")
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_core.messages import HumanMessage, ToolMessage
        from langchain_core.documents import Document
        from langchain_core.tools import tool

        # LangGraph for agent orchestration
        print("   📊 Testing LangGraph imports...")
        from langgraph.graph import StateGraph, END
        from langgraph.prebuilt import tools_condition

        print("✅ All imports successful!")
        print("   📦 Using modern standalone packages (no deprecated dependencies)")

        # Additional version information for educational purposes
        try:
            import langchain_chroma
            print(f"   📊 langchain-chroma version: {langchain_chroma.__version__}")
        except:
            pass

        try:
            import aiohttp
            print(f"   🌐 aiohttp version: {aiohttp.__version__}")
        except:
            pass

        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Install missing dependencies with:")
        print("   pip install -r requirements.txt")
        return False

    except Exception as e:
        print(f"❌ Unexpected error during imports: {e}")
        return False

async def main():
    """
    Main test suite coordinator.

    Runs all tests in logical order and provides comprehensive feedback.
    This async function coordinates the test sequence and provides
    detailed results for educational and debugging purposes.
    """
    # Test suite header
    print("🤖 CORNWALL TRAVEL AGENT - COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    print("Validating all system components before deployment")
    print("Testing imports, API connections, and core functionality")
    print("=" * 60)

    test_results = {"passed": 0, "total": 2}

    # Test 1: Dependency validation
    print("\n🔍 TEST 1: Dependency and Import Validation")
    print("-" * 45)
    if test_imports():
        test_results["passed"] += 1
        print("   ✅ Import test PASSED")
    else:
        print("   ❌ Import test FAILED - Cannot proceed without dependencies")
        print("\n📋 Test Summary: 0/2 tests passed")
        print("🚫 System is not ready for use")
        return

    # Test 2: API and model validation
    print("\n🔍 TEST 2: Google Gemini API Integration")
    print("-" * 45)
    if await test_basic_components():
        test_results["passed"] += 1
        print("   ✅ API integration test PASSED")
    else:
        print("   ❌ API integration test FAILED - Check configuration")

    # Final results and recommendations
    print("\n" + "=" * 60)
    print("📋 FINAL TEST RESULTS")
    print("=" * 60)
    print(f"Tests passed: {test_results['passed']}/{test_results['total']}")

    if test_results["passed"] == test_results["total"]:
        print("🎉 ALL TESTS PASSED! System is ready for use.")
        print("\n🚀 Next steps:")
        print("   • Full system demo: python run_agent.py")
        print("   • Interactive chat: python agent.py")
        print("   • Web interface: streamlit run app.py")

        print("\n🎓 Educational notes:")
        print("   • This validates individual components before integration")
        print("   • The full agent adds vector database and web scraping")
        print("   • LangGraph orchestrates these components into an agent")

    else:
        print("⚠️  SOME TESTS FAILED - System may not work correctly")
        print("\n🔧 Troubleshooting:")
        print("   • Review error messages above")
        print("   • Check .env file configuration")
        print("   • Verify internet connectivity")
        print("   • Ensure all dependencies are installed")

    print("=" * 60)


# -----------------------------------------------------------------------------
# MAIN EXECUTION: Comprehensive testing entry point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    """
    Entry point for comprehensive system testing.

    Usage:
        python test_agent.py

    This provides thorough validation of:
    - All required dependencies and imports
    - Google Gemini API connectivity and functionality
    - Core model capabilities (embeddings and chat)

    Ideal for:
    - Pre-deployment validation
    - Troubleshooting setup issues
    - Educational demonstration of testing practices
    """
    asyncio.run(main())