"""
Manager (Router) Agent
Routes queries to appropriate specialist agents based on query type
"""

from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ManagerAgent:
    """
    Manager/Router Agent that analyzes queries and routes to appropriate tools/agents

    Responsibilities:
    - Classify query type (summary vs precise fact vs hybrid)
    - Select appropriate retrieval tool(s)
    - Coordinate MCP tool usage
    - Synthesize results if multiple tools used
    """

    def __init__(
        self,
        tools: List[Tool],
        llm_model: str = "gpt-4",
        temperature: float = 0
    ):
        """
        Initialize Manager Agent

        Args:
            tools: List of available tools
            llm_model: LLM model to use
            temperature: Temperature setting
        """
        self.tools = tools
        self.llm = ChatOpenAI(model=llm_model, temperature=temperature)

        logger.info(f"ManagerAgent initialized with {len(tools)} tools")
        logger.info(f"Available tools: {[t.name for t in tools]}")

        # Create agent
        self.agent_executor = self._create_agent()

    def _create_agent(self):
        """Create the LangGraph agent with routing logic"""

        system_prompt = """You are a helpful assistant that answers questions about insurance claims.

You have access to tools to retrieve information from the claim documents. Use the appropriate tool based on the question:

RETRIEVAL TOOLS:
- SummaryRetriever: For general questions, overviews, timelines, "what happened" questions
- NeedleRetriever: For specific facts like dates, amounts, names, exact details
- SectionRetriever: For questions about specific document sections (format: "SECTION|question")

MCP TOOLS (for computations and metadata):
- GetDocumentMetadata: Get claim metadata (filing date, status, adjuster, policyholder info). Input: claim_id e.g. "CLM-2024-001"
- CalculateDaysBetween: Calculate days between two dates. Input: "YYYY-MM-DD,YYYY-MM-DD" e.g. "2024-01-12,2024-01-15"
- EstimateCoveragePayout: Calculate insurance payout. Input: "damage_amount,deductible" e.g. "17111.83,750.00"
- ValidateClaimStatus: Check if claim status is normal. Input: "filed_date,status" e.g. "2024-01-15,Under Review"
- GetTimelineSummary: Get timeline milestones for a claim. Input: claim_id e.g. "CLM-2024-001"

Use MCP tools when questions involve:
- Calculations (how many days, payout amounts, etc.)
- Claim metadata (status, adjuster name, filing date)
- Timeline milestones

Always use a tool to get information before answering. After getting the tool result, provide a clear, direct answer to the user's question based on the retrieved information.

Do NOT output code or function call syntax. Simply use the tools and then respond with the answer."""

        return create_react_agent(
            model=self.llm,
            tools=self.tools,
            prompt=system_prompt
        )

    def query(self, query: str) -> Dict[str, Any]:
        """
        Process a query through the manager agent

        Args:
            query: User query

        Returns:
            Dictionary with output and metadata
        """
        logger.info(f"ManagerAgent processing query: '{query[:100]}...'")

        try:
            # LangGraph uses messages format
            result = self.agent_executor.invoke(
                {"messages": [{"role": "user", "content": query}]}
            )

            # Extract the final response from messages
            messages = result.get("messages", [])
            output = ""

            if messages:
                # Get the last AI message that has actual text content (not tool calls)
                from langchain_core.messages import AIMessage, ToolMessage

                for msg in reversed(messages):
                    # Skip tool messages
                    if isinstance(msg, ToolMessage):
                        continue

                    # For AI messages, check if it has content and no tool calls
                    if isinstance(msg, AIMessage):
                        # If this message has tool_calls, it's not the final answer
                        if hasattr(msg, 'tool_calls') and msg.tool_calls:
                            continue
                        # If it has text content, this is likely the final answer
                        if msg.content and isinstance(msg.content, str) and msg.content.strip():
                            output = msg.content
                            break

                    # Fallback for other message types
                    elif hasattr(msg, 'content') and msg.content:
                        if isinstance(msg.content, str) and msg.content.strip():
                            output = msg.content
                            break

            # If no good output found, try to get any content
            if not output and messages:
                for msg in reversed(messages):
                    if hasattr(msg, 'content') and msg.content:
                        output = str(msg.content)
                        break

            # Log message types for debugging
            logger.info(f"Messages received: {len(messages)}")
            for i, msg in enumerate(messages):
                msg_type = type(msg).__name__
                has_tool_calls = hasattr(msg, 'tool_calls') and msg.tool_calls
                content_preview = str(msg.content)[:100] if hasattr(msg, 'content') and msg.content else 'None'
                logger.info(f"  [{i}] {msg_type}: tool_calls={has_tool_calls}, content={content_preview}...")

            return {
                "query": query,
                "output": output,
                "messages": messages,
                "success": True
            }

        except Exception as e:
            logger.error(f"ManagerAgent error: {e}")
            return {
                "query": query,
                "output": f"Error processing query: {str(e)}",
                "error": str(e),
                "success": False
            }

    def batch_query(self, queries: List[str]) -> List[Dict[str, Any]]:
        """
        Process multiple queries

        Args:
            queries: List of queries

        Returns:
            List of results
        """
        results = []
        for query in queries:
            result = self.query(query)
            results.append(result)

        return results


if __name__ == "__main__":
    print("ManagerAgent module - use via main system")
