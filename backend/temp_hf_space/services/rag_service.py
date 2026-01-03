import asyncio
import logging
from typing import List, Optional
from pathlib import Path
import json

try:
    # When running as a module
    from ..models.rag_models import SearchResult
except ImportError:
    # When running directly for testing
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from models.rag_models import SearchResult
import os

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        # Look for content in the parent directory where the book is located
        self.content_dir = Path("../book/docs")
        self.chunks = []
        self._initialized = False

    async def initialize(self):
        """Initialize the RAG service by loading content from book/docs"""
        if self._initialized:
            return

        logger.info("Initializing RAG service...")
        self.chunks = await self._load_content_chunks()
        logger.info(f"Loaded {len(self.chunks)} content chunks for RAG")
        self._initialized = True

    async def _load_content_chunks(self) -> List[dict]:
        """Load content from book/docs and create chunks"""
        chunks = []

        # Look for all markdown files in the book/docs directory
        if self.content_dir.exists():
            for md_file in self.content_dir.rglob("*.md"):
                try:
                    content = md_file.read_text(encoding='utf-8')
                    # Simple chunking based on content size
                    file_chunks = self._chunk_content(content, md_file.relative_to(self.content_dir.parent))

                    for chunk in file_chunks:
                        chunks.append({
                            'content': chunk,
                            'source': str(md_file.relative_to(self.content_dir)),
                            'score': 0.0  # Will be calculated during search
                        })
                except Exception as e:
                    logger.warning(f"Could not read file {md_file}: {e}")

        return chunks

    def _chunk_content(self, content: str, file_path: Path) -> List[str]:
        """Chunk content into 500-1200 character pieces"""
        chunks = []
        paragraphs = content.split('\n\n')

        current_chunk = ""
        for paragraph in paragraphs:
            # If adding this paragraph would exceed max size, start a new chunk
            if len(current_chunk) + len(paragraph) > 1200 and current_chunk:
                if len(current_chunk) >= 500:  # Only add if it meets minimum size
                    chunks.append(current_chunk.strip())
                    current_chunk = paragraph
                else:
                    # If current chunk is too small, just add the paragraph and continue
                    current_chunk += "\n\n" + paragraph
            else:
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph

        # Add the last chunk if it meets minimum size
        if current_chunk and len(current_chunk) >= 100:  # Minimum meaningful chunk
            chunks.append(current_chunk.strip())

        return chunks

    async def search(self, query: str, max_results: int = 5, module_filter: Optional[str] = None) -> List[SearchResult]:
        """Search for relevant content chunks based on the query"""
        await self.initialize()

        # Simple keyword-based search (in a real implementation, this would use embeddings)
        query_lower = query.lower()
        scored_chunks = []

        for chunk_data in self.chunks:
            if module_filter and module_filter.lower() not in chunk_data['source'].lower():
                continue

            # Calculate a simple relevance score based on keyword matches
            content_lower = chunk_data['content'].lower()
            score = 0

            # Count occurrences of query terms
            for term in query_lower.split():
                score += content_lower.count(term) * 10  # Boost score for each match

            # Additional scoring based on title/section matches (if present in content)
            if query_lower in chunk_data['source'].lower():
                score += 50  # Boost if source matches query

            if score > 0:
                scored_chunks.append({
                    'content': chunk_data['content'],
                    'source': chunk_data['source'],
                    'score': score,
                    'chunk_size': len(chunk_data['content'])
                })

        # Sort by score and return top results
        scored_chunks.sort(key=lambda x: x['score'], reverse=True)
        top_chunks = scored_chunks[:max_results]

        # Convert to SearchResult objects
        results = [
            SearchResult(
                content=chunk['content'],
                source=chunk['source'],
                score=chunk['score'],
                chunk_size=chunk['chunk_size']
            )
            for chunk in top_chunks
        ]

        return results

    async def validate_content(self, content: str, min_chunk_size: int = 500, max_chunk_size: int = 1200) -> tuple[bool, List[str], int]:
        """Validate content for RAG optimization"""
        chunk_size = len(content)
        suggestions = []

        if chunk_size < min_chunk_size:
            suggestions.append(f"Content is too short ({chunk_size} chars). Consider combining with related content to meet minimum {min_chunk_size} characters.")
        elif chunk_size > max_chunk_size:
            suggestions.append(f"Content is too long ({chunk_size} chars). Consider splitting into smaller chunks of {max_chunk_size} characters or less.")

        is_valid = min_chunk_size <= chunk_size <= max_chunk_size

        if not suggestions:
            suggestions.append("Content size is appropriate for RAG chunking.")

        return is_valid, suggestions, chunk_size