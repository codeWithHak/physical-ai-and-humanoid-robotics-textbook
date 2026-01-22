"""
Context Manager Service for managing token budgets in RAG responses.
Uses tiktoken for accurate token counting with OpenAI models.
"""

import tiktoken


class ContextManager:
    """
    Manages context window budget for retrieved content.

    Ensures retrieved chunks fit within the token budget while
    preserving the highest-relevance content. Uses score-based
    truncation to prioritize the most relevant results.
    """

    def __init__(self, budget: int = 4000, model: str = "gpt-4o-mini"):
        """
        Initialize the context manager.

        Args:
            budget: Maximum token budget for retrieved content
            model: Model name for tiktoken encoding
        """
        self.budget = budget
        self.model = model
        try:
            self.encoder = tiktoken.encoding_for_model(model)
        except KeyError:
            # Fallback to cl100k_base for newer models
            self.encoder = tiktoken.get_encoding("cl100k_base")

        print(f"[ContextManager] Initialized with {budget} token budget for {model}")

    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in a text string.

        Args:
            text: The text to count tokens for

        Returns:
            Number of tokens
        """
        return len(self.encoder.encode(text))

    def fit_to_budget(
        self,
        chunks: list[tuple[str, float]],
        separator: str = "\n\n",
    ) -> tuple[list[str], int]:
        """
        Select chunks that fit within the token budget.

        Chunks are assumed to be pre-sorted by relevance (highest first).
        Greedily adds chunks until budget is exhausted.

        Args:
            chunks: List of (content, relevance_score) tuples, sorted by score descending
            separator: String used to join chunks (counted in budget)

        Returns:
            Tuple of (selected_contents, total_tokens_used)
        """
        selected = []
        used_tokens = 0
        separator_tokens = self.count_tokens(separator)

        for content, _score in chunks:
            chunk_tokens = self.count_tokens(content)

            # Account for separator between chunks
            needed_tokens = chunk_tokens
            if selected:
                needed_tokens += separator_tokens

            if used_tokens + needed_tokens <= self.budget:
                selected.append(content)
                used_tokens += needed_tokens
            else:
                # Budget exhausted
                break

        return selected, used_tokens

    def truncate_content(self, content: str, max_tokens: int) -> str:
        """
        Truncate content to fit within a token limit.

        Useful for emergency truncation when content exceeds budget.
        Attempts to truncate at sentence boundaries when possible.

        Args:
            content: Text content to truncate
            max_tokens: Maximum tokens allowed

        Returns:
            Truncated content string
        """
        tokens = self.encoder.encode(content)

        if len(tokens) <= max_tokens:
            return content

        # Truncate tokens
        truncated_tokens = tokens[:max_tokens]
        truncated_text = self.encoder.decode(truncated_tokens)

        # Try to end at a sentence boundary
        for end_char in [".", "!", "?", "\n"]:
            last_boundary = truncated_text.rfind(end_char)
            if last_boundary > len(truncated_text) * 0.7:  # Keep at least 70%
                return truncated_text[: last_boundary + 1]

        return truncated_text + "..."

    def format_context_with_sources(
        self,
        chunks: list[tuple[str, str, float]],
    ) -> tuple[str, int]:
        """
        Format chunks with source citations for agent context.

        Args:
            chunks: List of (content, heading, score) tuples, sorted by score descending

        Returns:
            Tuple of (formatted_context, tokens_used)
        """
        # Convert to the format expected by fit_to_budget
        formatted_chunks = []
        for content, heading, score in chunks:
            formatted = f"[Source: {heading}]\n{content}"
            formatted_chunks.append((formatted, score))

        selected, tokens_used = self.fit_to_budget(formatted_chunks)
        return "\n\n".join(selected), tokens_used
