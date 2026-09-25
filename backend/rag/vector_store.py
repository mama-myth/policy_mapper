from typing import List, Dict, Any
from backend.policies.policy_loader import policy_loader, PolicyRecordModel
from backend.rag.embeddings import tokenize, compute_tf, cosine_similarity


class PolicyVectorStore:

    def __init__(self):
        self.documents: List[Dict[str, Any]] = []
        self.build_index()

    def build_index(self):
        policies = policy_loader.list_policies()
        self.documents = []

        for p in policies:
            # Combine policy text fields for semantic indexing
            content = f"{p.id} {p.title} {p.category} {p.requirement} {p.risk_explanation} {p.developer_guidance}"
            tokens = tokenize(content)
            tf_vector = compute_tf(tokens)

            self.documents.append({
                "policy_id": p.id,
                "policy": p,
                "content": content,
                "vector": tf_vector
            })

    def search(self, query: str, top_k: int = 2) -> List[Dict[str, Any]]:
        query_tokens = tokenize(query)
        query_vector = compute_tf(query_tokens)

        results = []
        for doc in self.documents:
            sim = cosine_similarity(query_vector, doc["vector"])
            results.append({
                "policy_id": doc["policy_id"],
                "policy": doc["policy"],
                "score": sim
            })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]


policy_vector_store = PolicyVectorStore()
