"""
Needle-in-a-Haystack Agent
Specialized in finding precise, specific facts using the Hierarchical Index
"""

from typing import Dict, Any, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NeedleAgent:
    """
    Specialized agent for precise fact-finding
    Uses hierarchical index with small chunks for maximum precision
    """

    def __init__(
        self,
        hierarchical_retriever,
        llm=None
    ):
        """
        Initialize Needle Agent

        Args:
            hierarchical_retriever: HierarchicalRetriever instance
            llm: Optional LLM for answer synthesis
        """
        self.retriever = hierarchical_retriever
        self.llm = llm

        logger.info("NeedleAgent initialized")

    def query(self, query: str, k: int = 3) -> Dict[str, Any]:
        """
        Find specific facts using needle search

        Args:
            query: Specific factual query
            k: Number of chunks to retrieve

        Returns:
            Dictionary with precise answer and sources
        """
        logger.info(f"NeedleAgent searching for: '{query[:100]}...'")

        try:
            # Use needle search for precision
            results = self.retriever.needle_search(query, k=k)

            if not results:
                return {
                    "query": query,
                    "output": "Could not find specific information matching your query. Please try rephrasing or ask a different question.",
                    "found": False,
                    "agent_type": "needle",
                    "success": True
                }

            # Extract information from results
            context = self.retriever.get_retrieval_context(results, include_metadata=True)

            # If LLM available, synthesize answer
            if self.llm:
                from langchain_core.prompts import ChatPromptTemplate

                synthesis_prompt = ChatPromptTemplate.from_messages([
                    ("system", """You are a precise fact-extraction agent.

Extract the specific information requested from the context provided.

Guidelines:
- Be precise and specific
- Quote exact numbers, dates, names when available
- Cite which part of the document the information came from
- If the exact information isn't found, say so clearly
- Don't infer or guess - only report what's explicitly stated"""),
                    ("human", """Query: {query}

Context:
{context}

Provide the precise answer to the query based only on the context above.""")
                ])

                chain = synthesis_prompt | self.llm
                response = chain.invoke({"query": query, "context": context})

                answer = response.content if hasattr(response, 'content') else str(response)
            else:
                # Return raw context if no LLM
                answer = f"Found relevant information:\n\n{context}"

            return {
                "query": query,
                "output": answer,
                "num_sources": len(results),
                "sources": [
                    {
                        "section": node.node.metadata.get('section_title', 'N/A'),
                        "chunk_level": node.node.metadata.get('chunk_level', 'N/A'),
                        "text_preview": node.node.text[:200] + "..."
                    }
                    for node in results
                ],
                "found": True,
                "agent_type": "needle",
                "success": True
            }

        except Exception as e:
            logger.error(f"NeedleAgent error: {e}")
            return {
                "query": query,
                "output": f"Error during needle search: {str(e)}",
                "error": str(e),
                "agent_type": "needle",
                "success": False
            }

    def find_exact_amount(self, amount_type: str) -> Dict[str, Any]:
        """
        Find specific dollar amount

        Args:
            amount_type: Type of amount (e.g., "deductible", "repair cost", "total claim")

        Returns:
            Precise amount information
        """
        query = f"What was the exact {amount_type} amount in dollars?"
        return self.query(query)

    def find_exact_date(self, event: str) -> Dict[str, Any]:
        """
        Find specific date for an event

        Args:
            event: Event description (e.g., "accident", "claim filed", "repairs completed")

        Returns:
            Precise date information
        """
        query = f"What was the exact date when {event}?"
        return self.query(query)

    def find_person(self, role: str) -> Dict[str, Any]:
        """
        Find specific person by role

        Args:
            role: Person's role (e.g., "claims adjuster", "policyholder", "at-fault driver")

        Returns:
            Person information
        """
        query = f"Who was the {role}? Provide the exact name."
        return self.query(query)

    def find_by_section(self, query: str, section: str) -> Dict[str, Any]:
        """
        Find specific information within a particular section

        Args:
            query: What to find
            section: Section to search in

        Returns:
            Section-specific information
        """
        logger.info(f"Searching section '{section}' for: '{query}'")

        try:
            results = self.retriever.retrieve_by_section(query, section, k=3)

            if not results:
                return {
                    "query": query,
                    "output": f"No information found in section '{section}'",
                    "found": False,
                    "section": section,
                    "success": True
                }

            context = self.retriever.get_retrieval_context(results, include_metadata=True)

            return {
                "query": query,
                "output": context,
                "section": section,
                "num_sources": len(results),
                "found": True,
                "success": True
            }

        except Exception as e:
            logger.error(f"Section search error: {e}")
            return {
                "query": query,
                "output": f"Error searching section: {str(e)}",
                "error": str(e),
                "success": False
            }


if __name__ == "__main__":
    print("NeedleAgent module - use via main system")
