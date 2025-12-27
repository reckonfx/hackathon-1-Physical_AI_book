import asyncio
import logging
from typing import List, Dict, Any
import openai

try:
    # When running as a module
    from .ai_agent_rag_service import AIAgentRAGService
    from ..models.rag_models import SearchResult
    from ..models.chat_models import ChatMessage, ChatRequest, ChatResponse
except ImportError:
    # When running directly for testing
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from services.ai_agent_rag_service import AIAgentRAGService
    from models.rag_models import SearchResult
    from models.chat_models import ChatMessage, ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

class ChatbotService:
    def __init__(self):
        self.ai_agent_rag_service = AIAgentRAGService()
        self.openai_client = None  # Will be configured later or use mock if unavailable

    async def initialize(self):
        """Initialize the chatbot service"""
        await self.ai_agent_rag_service.initialize()
        logger.info("Chatbot service with AI Agent initialized")

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Process a chat request using AI Agent RAG"""
        # Get the user's query from the last message
        user_query = ""
        for message in reversed(request.messages):
            if message.role == "user":
                user_query = message.content
                break

        if not user_query:
            raise ValueError("No user message found in request")

        # Generate response using the AI agent
        response_text = await self.ai_agent_rag_service.generate_answer(user_query)

        # Get relevant sources
        search_results = await self.ai_agent_rag_service.search(
            query=user_query,
            max_results=request.max_results,
            module_filter=request.module_filter
        )

        # Extract sources from search results
        sources = [result.source for result in search_results]

        return ChatResponse(
            response=response_text,
            sources=sources,
            tokens_used=len(response_text.split())  # Rough token count
        )

    def _format_context(self, search_results: List[SearchResult]) -> str:
        """Format search results as context for the LLM"""
        if not search_results:
            return "No relevant content found in the book. Please provide a general response based on your knowledge."

        context_parts = ["Relevant information from the Physical AI & Humanoid Robotics book:"]
        for i, result in enumerate(search_results, 1):
            # Extract just the content without the frontmatter
            content = result.content
            # Remove frontmatter if present (lines between --- markers at the beginning)
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    content = parts[2].strip()

            # Take a meaningful excerpt, avoiding just metadata
            clean_content = content[:500].strip()
            if len(result.content) > 500:
                clean_content += "..."

            context_parts.append(
                f"\n{i}. From {result.source}:\n{clean_content}"
            )

        return "\n".join(context_parts)

    def _prepare_prompt_with_context(self, messages: List[ChatMessage], context: str) -> List[Dict[str, str]]:
        """Prepare the full prompt with context"""
        # Create a system message with context - this context is for internal use only
        system_message = {
            "role": "system",
            "content": f"{context}\n\nInstructions: Answer the user's questions based on the provided book content. If the information is not in the provided context, say 'I don't have information about that in the Physical AI & Humanoid Robotics book.' Create a response that only contains the answer to the user's question without repeating the context. Do not include phrases like 'From [source]:' or the raw content snippets in your response. Be helpful and reference the specific sections when possible, but only in a natural way as part of your answer."
        }

        # Convert Pydantic messages to dict format
        formatted_messages = [system_message]
        for msg in messages:
            formatted_messages.append({
                "role": msg.role,
                "content": msg.content
            })

        return formatted_messages

    async def _generate_with_openai(self, messages: List[Dict[str, str]], temperature: float) -> str:
        """Generate response using OpenAI API"""
        # This is a placeholder - in a real implementation you would use the OpenAI API
        # For now, we'll create a real response based on the context
        import time
        time.sleep(0.1)  # Simulate API call delay

        # Extract the user query and context from the messages
        user_query = messages[-1]['content']
        context = messages[0]['content']  # System message contains context

        # Check if this is a high-level overview question (more specific to avoid catching technical "what is" questions)
        overview_keywords = ["overview", "about", "introduction", "summary", "describe", "explain", "what is this book", "what is the book"]
        is_overview_question = any(keyword in user_query.lower() for keyword in overview_keywords)

        # Generate a response based on the context
        if "No relevant content found" in context:
            return "I don't have information about that in the Physical AI & Humanoid Robotics book. Please try asking about ROS2, Isaac Sim, Gazebo, or VLA models."
        elif is_overview_question:
            # For overview questions, provide a synthesized summary of the book
            overview_response = "This comprehensive guide covers the complete technology stack for developing AI-powered humanoid robots across 4 main modules:\n\n"
            overview_response += "1. Module 1: ROS2 Fundamentals - Core concepts of Robot Operating System 2\n"
            overview_response += "2. Module 2: Gazebo & Unity Simulation - Physics simulation and realistic environments\n"
            overview_response += "3. Module 3: The AI-Robot Brain (NVIDIA Isaac™) - Advanced perception and navigation with Isaac Sim and ROS integration\n"
            overview_response += "4. Module 4: Vision-Language-Action (VLA) Models - Multimodal AI systems for perception, understanding, and action\n\n"
            overview_response += "The book is designed for intermediate AI/robotics students with hands-on exercises using technologies like ROS 2 Humble Hawksbill, Isaac Sim, and advanced robotics simulation tools."
            return overview_response
        else:
            # Extract relevant information from context, looking for content after "From [source]:"
            import re
            # Find all content sections that follow the "From [source]:\n[content]" pattern
            pattern = r"From (.*?):\n(.*?)(?=\n\d+\. From|$)"
            matches = re.findall(pattern, context, re.DOTALL)

            if matches:
                response = ""
                for i, (source, content) in enumerate(matches[:2]):  # Take first 2 matches
                    # Clean up the content by removing frontmatter and taking a meaningful excerpt
                    clean_content = content.strip()
                    if clean_content.startswith("---"):
                        parts = clean_content.split("---", 2)
                        if len(parts) >= 3:
                            clean_content = parts[2].strip()

                    # Take content that's most relevant to the user's query, focusing on explanations rather than learning objectives
                    import re
                    lines = clean_content.split('\n')
                    meaningful_lines = []
                    for line in lines:
                        line = line.strip()
                        # Remove HTML-like tags (e.g., <div className="...">, <p>, </p>, etc.)
                        clean_line = re.sub(r'<[^>]+>', '', line).strip()

                        if clean_line and not line.startswith('#') and not line.startswith('id:') and not line.startswith('title:') and not line.startswith('sidebar_position:'):
                            # Skip learning objectives, prerequisites, etc.
                            if not any(skip_phrase in clean_line.lower() for skip_phrase in
                                      ['by the end of this lesson', 'learning objectives', 'prerequisites',
                                       'objectives:', 'you will be able to:', 'we will cover:',
                                       'in this lesson', 'lesson covers', 'this lesson introduces']):
                                meaningful_lines.append(clean_line)
                                if len(meaningful_lines) >= 2:  # Take up to 2 most relevant lines
                                    break

                    if meaningful_lines:
                        if response:  # Add a separator if this is not the first item
                            response += "\n"
                        response += "\n".join(meaningful_lines)

                if response:
                    response += "\n\nFor more detailed information, please refer to the specific sections in the book."
                    return response
                else:
                    return f"I found information in the Physical AI & Humanoid Robotics book related to your query. For complete details, please refer to the relevant sections in the book."
            else:
                return f"I found information in the Physical AI & Humanoid Robotics book related to your query. For complete details, please refer to the relevant sections in the book."

    def _generate_fallback_response(self, user_query: str, context: str) -> str:
        """Generate a fallback response when LLM is not available"""
        if "No relevant content found" in context:
            return "I don't have information about that in the Physical AI & Humanoid Robotics book. Please try asking about ROS2, Isaac Sim, Gazebo, or VLA models."
        else:
            # Check if this is a high-level overview question (more specific to avoid catching technical "what is" questions)
            overview_keywords = ["overview", "about", "introduction", "summary", "describe", "explain", "what is this book", "what is the book"]
            is_overview_question = any(keyword in user_query.lower() for keyword in overview_keywords)

            if is_overview_question:
                # For overview questions, provide a synthesized summary of the book
                overview_response = "This comprehensive guide covers the complete technology stack for developing AI-powered humanoid robots across 4 main modules:\n\n"
                overview_response += "1. Module 1: ROS2 Fundamentals - Core concepts of Robot Operating System 2\n"
                overview_response += "2. Module 2: Gazebo & Unity Simulation - Physics simulation and realistic environments\n"
                overview_response += "3. Module 3: The AI-Robot Brain (NVIDIA Isaac™) - Advanced perception and navigation with Isaac Sim and ROS integration\n"
                overview_response += "4. Module 4: Vision-Language-Action (VLA) Models - Multimodal AI systems for perception, understanding, and action\n\n"
                overview_response += "The book is designed for intermediate AI/robotics students with hands-on exercises using technologies like ROS 2 Humble Hawksbill, Isaac Sim, and advanced robotics simulation tools."
                return overview_response
            else:
                # Extract relevant information from context, looking for content after "From [source]:"
                import re
                # Find all content sections that follow the "From [source]:\n[content]" pattern
                pattern = r"From (.*?):\n(.*?)(?=\n\d+\. From|$)"
                matches = re.findall(pattern, context, re.DOTALL)

                if matches:
                    response = ""
                    for i, (source, content) in enumerate(matches[:2]):  # Take first 2 matches
                        # Clean up the content by removing frontmatter and taking a meaningful excerpt
                        clean_content = content.strip()
                        if clean_content.startswith("---"):
                            parts = clean_content.split("---", 2)
                            if len(parts) >= 3:
                                clean_content = parts[2].strip()

                        # Take content that's most relevant to the user's query, focusing on explanations rather than learning objectives
                        import re
                        lines = clean_content.split('\n')
                        meaningful_lines = []
                        for line in lines:
                            line = line.strip()
                            # Remove HTML-like tags (e.g., <div className="...">, <p>, </p>, etc.)
                            clean_line = re.sub(r'<[^>]+>', '', line).strip()

                            if clean_line and not line.startswith('#') and not line.startswith('id:') and not line.startswith('title:') and not line.startswith('sidebar_position:'):
                                # Skip learning objectives, prerequisites, etc.
                                if not any(skip_phrase in clean_line.lower() for skip_phrase in
                                          ['by the end of this lesson', 'learning objectives', 'prerequisites',
                                           'objectives:', 'you will be able to:', 'we will cover:',
                                           'in this lesson', 'lesson covers', 'this lesson introduces']):
                                    meaningful_lines.append(clean_line)
                                    if len(meaningful_lines) >= 2:  # Take up to 2 most relevant lines
                                        break

                        if meaningful_lines:
                            if response:  # Add a separator if this is not the first item
                                response += "\n"
                            response += "\n".join(meaningful_lines)

                    if response:
                        response += "\n\nFor more detailed information, please refer to the specific sections in the book."
                        return response
                    else:
                        return f"I found information in the Physical AI & Humanoid Robotics book related to your query. For complete details, please refer to the relevant sections in the book."
                else:
                    return f"I found information in the Physical AI & Humanoid Robotics book related to your query. For complete details, please refer to the relevant sections in the book."