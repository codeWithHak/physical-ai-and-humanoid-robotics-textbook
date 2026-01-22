"""
Hybrid Search Service for combining vector search with BM25 sparse retrieval.
Uses Reciprocal Rank Fusion (RRF) to merge ranked results.
"""

from dataclasses import dataclass
from typing import Optional
from rank_bm25 import BM25Okapi


@dataclass
class HybridResult:
    """A search result with hybrid ranking scores."""

    chunk_id: str
    content: str
    heading: str
    filepath: str
    vector_score: float
    bm25_score: float
    hybrid_score: float
    vector_rank: Optional[int] = None
    bm25_rank: Optional[int] = None


class HybridSearch:
    """
    Combines dense vector search with BM25 sparse retrieval.

    Uses Reciprocal Rank Fusion (RRF) to merge results from both
    retrieval methods, leveraging the strengths of each:
    - Vector search: semantic similarity, conceptual matching
    - BM25: exact keyword matching, technical terminology
    """

    def __init__(self, documents: list[dict], rrf_k: int = 60):
        """
        Initialize the hybrid search with a document corpus.

        Args:
            documents: List of dicts with 'id', 'content', 'heading', 'filepath' keys
            rrf_k: RRF constant (default 60, standard value from literature)
        """
        self.documents = documents
        self.rrf_k = rrf_k
        self._doc_index = {doc["id"]: doc for doc in documents}

        # Build BM25 index from document contents
        tokenized_corpus = [self._tokenize(doc["content"]) for doc in documents]
        self.bm25 = BM25Okapi(tokenized_corpus)

        print(f"[HybridSearch] Initialized with {len(documents)} documents")

    def _tokenize(self, text: str) -> list[str]:
        """Simple whitespace tokenization with lowercasing."""
        return text.lower().split()

    def bm25_search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]:
        """
        Perform BM25 sparse retrieval.

        Args:
            query: Search query string
            top_k: Number of results to return

        Returns:
            List of (doc_id, score) tuples sorted by score descending
        """
        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)

        # Pair doc IDs with scores and sort
        doc_scores = [(self.documents[i]["id"], scores[i]) for i in range(len(scores))]
        doc_scores.sort(key=lambda x: x[1], reverse=True)

        return doc_scores[:top_k]

    def _reciprocal_rank_fusion(
        self,
        vector_results: list[tuple[str, float]],
        bm25_results: list[tuple[str, float]],
    ) -> list[tuple[str, float, int, int]]:
        """
        Merge two ranked lists using Reciprocal Rank Fusion.

        RRF score = sum(1 / (k + rank_i)) for each ranking

        Args:
            vector_results: List of (doc_id, score) from vector search
            bm25_results: List of (doc_id, score) from BM25 search

        Returns:
            List of (doc_id, rrf_score, vector_rank, bm25_rank) sorted by rrf_score
        """
        rrf_scores: dict[str, float] = {}
        vector_ranks: dict[str, int] = {}
        bm25_ranks: dict[str, int] = {}

        # Calculate RRF contributions from vector search
        for rank, (doc_id, _) in enumerate(vector_results, start=1):
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + 1 / (self.rrf_k + rank)
            vector_ranks[doc_id] = rank

        # Calculate RRF contributions from BM25 search
        for rank, (doc_id, _) in enumerate(bm25_results, start=1):
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + 1 / (self.rrf_k + rank)
            bm25_ranks[doc_id] = rank

        # Sort by combined RRF score
        sorted_results = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

        return [
            (
                doc_id,
                score,
                vector_ranks.get(doc_id),
                bm25_ranks.get(doc_id),
            )
            for doc_id, score in sorted_results
        ]

    def hybrid_search(
        self,
        query: str,
        vector_results: list[tuple[str, float]],
        top_k: int = 10,
    ) -> list[HybridResult]:
        """
        Perform hybrid search combining vector results with BM25.

        Args:
            query: Search query string
            vector_results: Pre-computed vector search results as (doc_id, score) tuples
            top_k: Number of results to return

        Returns:
            List of HybridResult objects with combined scores
        """
        # Get BM25 results
        bm25_results = self.bm25_search(query, top_k=top_k * 2)

        # Merge using RRF
        fused_results = self._reciprocal_rank_fusion(vector_results, bm25_results)

        # Build HybridResult objects
        results = []
        vector_score_map = {doc_id: score for doc_id, score in vector_results}
        bm25_score_map = {doc_id: score for doc_id, score in bm25_results}

        for doc_id, rrf_score, v_rank, b_rank in fused_results[:top_k]:
            doc = self._doc_index.get(doc_id)
            if doc is None:
                continue

            results.append(
                HybridResult(
                    chunk_id=doc_id,
                    content=doc["content"],
                    heading=doc["heading"],
                    filepath=doc.get("filepath", ""),
                    vector_score=vector_score_map.get(doc_id, 0.0),
                    bm25_score=bm25_score_map.get(doc_id, 0.0),
                    hybrid_score=rrf_score,
                    vector_rank=v_rank,
                    bm25_rank=b_rank,
                )
            )

        return results
