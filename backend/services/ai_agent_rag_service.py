import asyncio
import logging
from typing import List, Optional
from pathlib import Path
import os
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from langchain.tools import tool
from langchain_core.tools import BaseTool
from langchain_openai import OpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
import google.generativeai as genai

try:
    # When running as a module
    from ..models.rag_models import SearchResult
    from ..config import settings
except ImportError:
    # When running directly for testing
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from models.rag_models import SearchResult
    from config import settings

logger = logging.getLogger(__name__)

class AIAgentRAGService:
    def __init__(self):
        self.content_dir = Path("../book/docs")
        self.documents = []
        self.vector_store = None
        self.llm = None
        self.retrieval_chain = None
        self.agent_executor = None
        self._initialized = False

        # Initialize API keys with priority: OpenRouter → OpenAI → Google
        if settings.OPENROUTER_API_KEY:
            # Use OpenRouter if available - set as primary API key for OpenAI-compatible client
            os.environ["OPENAI_API_KEY"] = settings.OPENROUTER_API_KEY
            # Set OpenRouter base URL for OpenAI-compatible client
            os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"
        elif settings.OPENAI_API_KEY:
            os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
            # Clear any OpenRouter base URL if using regular OpenAI
            if "OPENAI_BASE_URL" in os.environ:
                del os.environ["OPENAI_BASE_URL"]
        if settings.GOOGLE_API_KEY:
            os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY
            genai.configure(api_key=settings.GOOGLE_API_KEY)

    async def initialize(self):
        """Initialize the AI Agent RAG service by loading content and setting up the vector store"""
        if self._initialized:
            return

        logger.info("Initializing AI Agent RAG service...")

        # Load documents
        self.documents = await self._load_documents()
        logger.info(f"Loaded {len(self.documents)} documents")

        # Create vector store with priority: OpenRouter → Google → OpenAI
        embeddings = None
        if settings.OPENROUTER_API_KEY:
            # Use OpenAI-compatible embeddings with OpenRouter (highest priority)
            embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        elif settings.GOOGLE_API_KEY:
            # Try Google embeddings, but fall back if there are quota issues
            try:
                embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
                # Test the embeddings with a simple text to check for quota issues
                embeddings.embed_documents(["test"])
            except Exception as e:
                logger.warning(f"Google embeddings failed: {e}. Falling back to OpenAI embeddings.")
                embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        else:
            # Use OpenAI embeddings as default
            embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        self.vector_store = FAISS.from_documents(self.documents, embeddings)
        logger.info("Vector store created")

        # Initialize LLM (prefer OpenRouter if available, then Google Gemini, then OpenAI)
        if settings.OPENROUTER_API_KEY:
            self.llm = ChatOpenAI(
                model=settings.OPENROUTER_MODEL,
                temperature=0.1,
                base_url="https://openrouter.ai/api/v1"
            )
        elif settings.GOOGLE_API_KEY:
            self.llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.1)
        else:
            self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)

        # Create the retrieval chain using modern LangChain approach
        template = """You are an expert assistant for the Physical AI & Humanoid Robotics book.
        Use the following pieces of retrieved context to answer the question.
        Provide a clear, concise answer based on the book content.
        Do not include phrases like 'Based on the provided context' or 'According to the document'.
        If you don't know the answer, say that you don't know.
        Keep your answer focused and helpful.

        Context: {context}

        Question: {question}

        Answer:"""

        prompt = ChatPromptTemplate.from_template(template)
        output_parser = StrOutputParser()

        # Create the complete RAG chain
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        self.retrieval_chain = (
            RunnableParallel(
                {"context": self.vector_store.as_retriever() | format_docs, "question": RunnablePassthrough()}
            )
            | prompt
            | self.llm
            | output_parser
        )

        # Create tools for the agent
        self.search_tool = self._create_search_tool()

        # Create the retrieval chain using modern LangChain approach instead of agent
        template = """You are an expert assistant for the Physical AI & Humanoid Robotics book.
        Use the following pieces of retrieved context to answer the question.
        Provide a clear, concise answer based on the book content.
        Do not include phrases like 'Based on the provided context' or 'According to the document'.
        If you don't know the answer, say that you don't know.
        Keep your answer focused and helpful.

        Context: {context}

        Question: {question}

        Answer:"""

        prompt = ChatPromptTemplate.from_template(template)
        output_parser = StrOutputParser()

        # Create the complete RAG chain
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        self.retrieval_chain = (
            RunnableParallel(
                {"context": self.vector_store.as_retriever() | format_docs, "question": RunnablePassthrough()}
            )
            | prompt
            | self.llm
            | output_parser
        )

        # Set agent_executor to None since we're not using an agent approach
        self.agent_executor = None

        logger.info("AI Agent RAG service initialized")
        self._initialized = True

    def _create_search_tool(self):
        """Create a search tool for the agent"""
        from langchain.tools import tool

        @tool("search_book_content")
        def search_tool_func(query: str, max_results: int = 5) -> str:
            """Search the Physical AI & Humanoid Robotics book content for relevant information. Input should be a search query string."""
            if not self.vector_store:
                return "Vector store not initialized"

            # Perform similarity search
            docs = self.vector_store.similarity_search(query, k=max_results)

            # Format results
            results = []
            for doc in docs:
                results.append({
                    'content': doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content,
                    'source': doc.metadata.get('source', 'unknown')
                })

            return str(results)

        return search_tool_func

    async def _load_documents(self) -> List[Document]:
        """Load content from book/docs and create documents"""
        documents = []

        # Look for all markdown files in the book/docs directory
        if self.content_dir.exists():
            for md_file in self.content_dir.rglob("*.md"):
                try:
                    content = md_file.read_text(encoding='utf-8')
                    # Remove frontmatter if present
                    if content.startswith("---"):
                        parts = content.split("---", 2)
                        if len(parts) >= 3:
                            content = parts[2].strip()

                    # Create a document
                    doc = Document(
                        page_content=content,
                        metadata={"source": str(md_file.relative_to(self.content_dir.parent))}
                    )
                    documents.append(doc)
                except Exception as e:
                    logger.warning(f"Could not read file {md_file}: {e}")

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )

        split_docs = text_splitter.split_documents(documents)
        return split_docs

    async def search(self, query: str, max_results: int = 5, module_filter: Optional[str] = None) -> List[SearchResult]:
        """Search for relevant content using the AI agent"""
        await self.initialize()

        # Use the vector store directly for search
        if self.vector_store:
            try:
                # Perform similarity search
                docs = self.vector_store.similarity_search(query, k=max_results)

                # Filter by module if specified
                if module_filter:
                    docs = [doc for doc in docs if module_filter.lower() in doc.metadata.get('source', '').lower()]

                # Convert to SearchResult objects
                results = []
                for doc in docs[:max_results]:
                    results.append(SearchResult(
                        content=doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content,
                        source=doc.metadata.get('source', 'unknown'),
                        score=1.0,  # Placeholder score
                        chunk_size=len(doc.page_content)
                    ))
                return results
            except Exception as e:
                logger.error(f"Error in AI agent search: {e}")
                # More specific error handling for search errors
                error_msg = str(e).lower()
                if "openrouter" in error_msg or "api" in error_msg or "authentication" in error_msg or "401" in error_msg or "403" in error_msg:
                    logger.error(f"OpenRouter API error during search: {e}")
                return []

        return []

    async def generate_answer(self, query: str) -> str:
        """Generate an answer using the RAG chain"""
        await self.initialize()

        try:
            # Use the retrieval chain to generate a response
            if self.retrieval_chain:
                response = self.retrieval_chain.invoke(query)
                return str(response)
            else:
                logger.error("Retrieval chain not initialized")
                return "I'm having trouble generating a response. Please try again."
        except Exception as e:
            logger.error(f"Error in RAG answer generation: {e}")
            # More specific error handling for different types of errors
            error_msg = str(e).lower()
            if "openrouter" in error_msg or "api" in error_msg or "authentication" in error_msg or "401" in error_msg or "403" in error_msg:
                logger.error(f"OpenRouter API error: {e}")
                return "I'm currently experiencing issues with the AI service. Please try again later."
            elif "rate limit" in error_msg or "quota" in error_msg:
                logger.error(f"OpenRouter rate limit error: {e}")
                return "The AI service is temporarily unavailable due to high demand. Please try again later."
            else:
                logger.error(f"General error in RAG answer generation: {e}")
                return "I encountered an issue processing your request. Please try again."

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