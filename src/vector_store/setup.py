"""
Vector Store Manager for ChromaDB
Handles setup and configuration of ChromaDB collections for insurance claim data.
"""

import chromadb
from chromadb.config import Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorStoreManager:
    """
    Manages ChromaDB vector store with separate collections for:
    1. Summary Index - High-level document summaries and timeline data
    2. Hierarchical Index - Multi-level chunks with parent-child relationships
    """

    def __init__(self, persist_dir: str = "./chroma_db"):
        """
        Initialize ChromaDB with persistence

        Args:
            persist_dir: Directory path for persisting ChromaDB data
        """
        self.persist_dir = Path(persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Initializing ChromaDB at {self.persist_dir}")

        self.client = chromadb.PersistentClient(
            path=str(self.persist_dir),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True  # Allow reset for clean rebuilds
            )
        )

    def get_summary_collection(self):
        """
        Get or create collection for summary index

        Returns:
            ChromaDB collection for summaries
        """
        collection = self.client.get_or_create_collection(
            name="insurance_summaries",
            metadata={
                "description": "Document summaries, timeline data, and high-level overviews",
                "hnsw:space": "cosine",  # Distance metric for similarity
                "index_type": "summary"
            }
        )
        logger.info(f"Summary collection loaded: {collection.count()} documents")
        return collection

    def get_hierarchical_collection(self):
        """
        Get or create collection for hierarchical chunks

        Returns:
            ChromaDB collection for hierarchical chunks
        """
        collection = self.client.get_or_create_collection(
            name="insurance_hierarchical",
            metadata={
                "description": "Multi-level chunks with parent-child relationships for precise retrieval",
                "hnsw:space": "cosine",
                "index_type": "hierarchical"
            }
        )
        logger.info(f"Hierarchical collection loaded: {collection.count()} chunks")
        return collection

    def create_storage_context(self, collection):
        """
        Create LlamaIndex storage context with ChromaDB backend

        Args:
            collection: ChromaDB collection

        Returns:
            StorageContext for LlamaIndex
        """
        vector_store = ChromaVectorStore(chroma_collection=collection)
        return StorageContext.from_defaults(vector_store=vector_store)

    def reset_collections(self):
        """
        Reset all collections (use with caution!)
        Useful for development and testing
        """
        logger.warning("Resetting all collections...")
        try:
            self.client.delete_collection("insurance_summaries")
            logger.info("Deleted summary collection")
        except Exception as e:
            logger.debug(f"Summary collection doesn't exist: {e}")

        try:
            self.client.delete_collection("insurance_hierarchical")
            logger.info("Deleted hierarchical collection")
        except Exception as e:
            logger.debug(f"Hierarchical collection doesn't exist: {e}")

    def get_collection_stats(self):
        """
        Get statistics about collections

        Returns:
            Dictionary with collection statistics
        """
        stats = {}

        try:
            summary_col = self.get_summary_collection()
            stats['summary'] = {
                'count': summary_col.count(),
                'name': summary_col.name,
                'metadata': summary_col.metadata
            }
        except Exception as e:
            stats['summary'] = {'error': str(e)}

        try:
            hier_col = self.get_hierarchical_collection()
            stats['hierarchical'] = {
                'count': hier_col.count(),
                'name': hier_col.name,
                'metadata': hier_col.metadata
            }
        except Exception as e:
            stats['hierarchical'] = {'error': str(e)}

        return stats

    def inspect_collection(self, collection_name: str, limit: int = 5):
        """
        Inspect contents of a collection for debugging

        Args:
            collection_name: Name of collection to inspect
            limit: Number of items to retrieve

        Returns:
            Sample documents from collection
        """
        try:
            collection = self.client.get_collection(collection_name)
            results = collection.peek(limit=limit)
            return {
                'ids': results['ids'],
                'metadatas': results['metadatas'],
                'documents': results['documents'][:limit] if results['documents'] else []
            }
        except Exception as e:
            logger.error(f"Error inspecting collection {collection_name}: {e}")
            return {'error': str(e)}


if __name__ == "__main__":
    # Test the vector store manager
    vsm = VectorStoreManager()

    print("\n=== Vector Store Manager Test ===\n")

    # Get collections
    summary_col = vsm.get_summary_collection()
    hier_col = vsm.get_hierarchical_collection()

    print(f"Summary Collection: {summary_col.name}")
    print(f"  Count: {summary_col.count()}")
    print(f"  Metadata: {summary_col.metadata}")

    print(f"\nHierarchical Collection: {hier_col.name}")
    print(f"  Count: {hier_col.count()}")
    print(f"  Metadata: {hier_col.metadata}")

    # Get stats
    stats = vsm.get_collection_stats()
    print(f"\n=== Collection Stats ===")
    for name, info in stats.items():
        print(f"{name}: {info}")
