#!/usr/bin/env python3
"""
Test script for the AI Agent RAG Service
"""

import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.services.ai_agent_rag_service import AIAgentRAGService
from backend.models.rag_models import SearchResult

async def test_ai_agent():
    """Test the AI Agent RAG Service"""
    print("Testing AI Agent RAG Service...")

    # Create an instance of the service
    agent_service = AIAgentRAGService()

    try:
        # Initialize the service
        print("Initializing AI Agent RAG Service...")
        await agent_service.initialize()
        print("AI Agent RAG Service initialized successfully!")

        # Test search functionality
        print("\nTesting search functionality...")
        search_results = await agent_service.search("What is ROS2?", max_results=3)
        print(f"Found {len(search_results)} search results")
        for i, result in enumerate(search_results):
            print(f"Result {i+1}:")
            print(f"  Source: {result.source}")
            print(f"  Content preview: {result.content[:100]}...")
            print()

        # Test answer generation
        print("Testing answer generation...")
        answer = await agent_service.generate_answer("What is this book about?")
        print(f"Generated answer: {answer}")

        # Test another question
        print("\nTesting another question...")
        answer2 = await agent_service.generate_answer("Explain ROS2 fundamentals")
        print(f"Generated answer: {answer2}")

    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_ai_agent())