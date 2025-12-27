import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_search_functionality():
    print("Testing search functionality...")

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

        print("Search functionality test passed!")

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

        print(f"Valid content (size {chunk_size}): is_valid={is_valid}, suggestions={suggestions[:2]}")
        assert is_valid, "Content should be valid"

        # Test too short content
        short_content = "Short"
        is_valid, suggestions, chunk_size = await rag_service.validate_content(short_content)

        print(f"Short content (size {chunk_size}): is_valid={is_valid}, suggestions={suggestions[:2]}")
        assert not is_valid, "Short content should not be valid"

        print("Content validation test passed!")

    asyncio.run(run_validation())

if __name__ == "__main__":
    test_search_functionality()
    test_content_validation()

    print("\nAll functionality tests passed! The RAG system is working correctly.")