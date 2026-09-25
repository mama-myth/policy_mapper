from typing import List, Dict, Any
from backend.rag.vector_store import policy_vector_store


def retrieve_policy_context(observed_pattern: str, sensitive_identifier: str) -> List[Dict[str, Any]]:
    """Retrieves relevant policy records from the vector store based on observed pattern evidence."""
    query = f"sensitive identifier {sensitive_identifier} passed to logging function {observed_pattern}"
    results = policy_vector_store.search(query, top_k=2)
    return results
