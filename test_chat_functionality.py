import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test the chat functionality specifically
from backend.services.chatbot_service import ChatbotService
from backend.models.chat_models import ChatMessage, ChatRequest

async def test_chat_functionality():
    print("Testing chat functionality...")

    # Initialize the chatbot service
    chatbot_service = ChatbotService()
    await chatbot_service.initialize()

    # Create a test chat request
    chat_request = ChatRequest(
        messages=[
            ChatMessage(role="user", content="What is ROS2 and how does it relate to robotics?")
        ],
        max_results=3
    )

    # Process the chat request
    response = await chatbot_service.chat(chat_request)

    print(f"Response: {response.response}")
    print(f"Sources: {response.sources}")
    print(f"Tokens used: {response.tokens_used}")

    # Verify the response has content
    assert len(response.response) > 0, "Response should not be empty"
    assert len(response.sources) > 0, "Should have at least one source"
    assert response.tokens_used > 0, "Should have used some tokens"

    print("✅ Chat functionality test passed!")

def test_search_functionality():
    print("\nTesting search functionality...")

    from backend.services.rag_service import RAGService
    import asyncio

    async def run_search():
        rag_service = RAGService()
        results = await rag_service.search("ROS2", max_results=5)

        print(f"Found {len(results)} results for 'ROS2' query")
        for i, result in enumerate(results[:2]):  # Show first 2 results
            print(f"  Result {i+1}: Source: {result.source[:50]}..., Score: {result.score}")

        assert len(results) > 0, "Should find results for ROS2 query"
        assert all(r.score > 0 for r in results), "All results should have positive scores"

        print("✅ Search functionality test passed!")

    asyncio.run(run_search())

def test_content_validation():
    print("\nTesting content validation...")

    from backend.services.rag_service import RAGService
    import asyncio

    async def run_validation():
        rag_service = RAGService()

        # Test valid content
        valid_content = "This is a properly sized content chunk for RAG system testing. " * 15  # ~750 chars
        is_valid, suggestions, chunk_size = await rag_service.validate_content(valid_content)

        print(f"Valid content (size {chunk_size}): is_valid={is_valid}, suggestions={suggestions}")
        assert is_valid, "Content should be valid"

        # Test too short content
        short_content = "Short"
        is_valid, suggestions, chunk_size = await rag_service.validate_content(short_content)

        print(f"Short content (size {chunk_size}): is_valid={is_valid}, suggestions={suggestions}")
        assert not is_valid, "Short content should not be valid"

        # Test too long content
        long_content = "This is very long content. " * 60  # ~1500 chars
        is_valid, suggestions, chunk_size = await rag_service.validate_content(long_content)

        print(f"Long content (size {chunk_size}): is_valid={is_valid}, suggestions={suggestions}")
        assert not is_valid, "Long content should not be valid"

        print("✅ Content validation test passed!")

    asyncio.run(run_validation())

if __name__ == "__main__":
    test_search_functionality()
    test_content_validation()

    # Run async test
    import asyncio
    asyncio.run(test_chat_functionality())

    print("\n🎉 All functionality tests passed! The RAG system and chatbot are working correctly.")