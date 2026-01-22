"""
Semantic Chunker Service for intelligent document splitting.
Uses header boundaries and paragraph-level fallback for optimal chunk sizes.
"""

import re
from dataclasses import dataclass
from typing import Optional
import tiktoken


@dataclass
class SemanticChunk:
    """A semantically meaningful chunk of document content."""

    content: str
    heading: str
    position: int
    parent_heading: Optional[str] = None
    token_count: int = 0


class SemanticChunker:
    """
    Splits markdown documents into semantic chunks based on structure.

    Uses document headers (H2/H3) as natural boundaries, with
    paragraph-level fallback for sections that exceed the token limit.
    """

    def __init__(
        self,
        max_tokens: int = 500,
        min_tokens: int = 50,
        model: str = "gpt-4o-mini",
    ):
        """
        Initialize the semantic chunker.

        Args:
            max_tokens: Maximum tokens per chunk (target 200-500)
            min_tokens: Minimum tokens per chunk (avoid tiny chunks)
            model: Model name for tiktoken encoding
        """
        self.max_tokens = max_tokens
        self.min_tokens = min_tokens
        try:
            self.encoder = tiktoken.encoding_for_model(model)
        except KeyError:
            self.encoder = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        """Count tokens in a text string."""
        return len(self.encoder.encode(text))

    def split_by_headers(self, markdown: str) -> list[dict]:
        """
        Split markdown by H2 and H3 headers.

        Args:
            markdown: Raw markdown content

        Returns:
            List of dicts with 'heading', 'content', 'level', 'parent_heading'
        """
        # Pattern to match H2 and H3 headers
        header_pattern = r"^(#{2,3})\s+(.+)$"

        sections = []
        current_h2 = None
        current_section = None
        lines = markdown.split("\n")

        for line in lines:
            header_match = re.match(header_pattern, line)

            if header_match:
                # Save previous section
                if current_section and current_section["content"].strip():
                    sections.append(current_section)

                level = len(header_match.group(1))
                heading = header_match.group(2).strip()

                if level == 2:
                    current_h2 = heading
                    parent = None
                else:  # level == 3
                    parent = current_h2

                current_section = {
                    "heading": heading,
                    "content": "",
                    "level": level,
                    "parent_heading": parent,
                }
            elif current_section is not None:
                current_section["content"] += line + "\n"

        # Don't forget the last section
        if current_section and current_section["content"].strip():
            sections.append(current_section)

        return sections

    def split_at_paragraphs(
        self,
        content: str,
        heading: str,
        parent_heading: Optional[str] = None,
    ) -> list[SemanticChunk]:
        """
        Split long content at paragraph boundaries.

        Args:
            content: Text content to split
            heading: Section heading
            parent_heading: Parent section heading (for H3 under H2)

        Returns:
            List of SemanticChunk objects
        """
        paragraphs = re.split(r"\n\s*\n", content.strip())
        chunks = []
        current_chunk_parts = []
        current_tokens = 0
        position = 0

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            para_tokens = self.count_tokens(para)

            # If single paragraph exceeds max, split it by sentences
            if para_tokens > self.max_tokens:
                # First, save accumulated content
                if current_chunk_parts:
                    chunks.append(
                        SemanticChunk(
                            content="\n\n".join(current_chunk_parts),
                            heading=heading,
                            position=position,
                            parent_heading=parent_heading,
                            token_count=current_tokens,
                        )
                    )
                    position += 1
                    current_chunk_parts = []
                    current_tokens = 0

                # Split large paragraph by sentences
                sentence_chunks = self._split_by_sentences(para)
                for sent_chunk in sentence_chunks:
                    sent_tokens = self.count_tokens(sent_chunk)
                    chunks.append(
                        SemanticChunk(
                            content=sent_chunk,
                            heading=heading,
                            position=position,
                            parent_heading=parent_heading,
                            token_count=sent_tokens,
                        )
                    )
                    position += 1
                continue

            # Check if adding this paragraph exceeds budget
            if current_tokens + para_tokens > self.max_tokens and current_chunk_parts:
                # Save current chunk and start new one
                chunks.append(
                    SemanticChunk(
                        content="\n\n".join(current_chunk_parts),
                        heading=heading,
                        position=position,
                        parent_heading=parent_heading,
                        token_count=current_tokens,
                    )
                )
                position += 1
                current_chunk_parts = []
                current_tokens = 0

            current_chunk_parts.append(para)
            current_tokens += para_tokens

        # Save remaining content
        if current_chunk_parts:
            chunks.append(
                SemanticChunk(
                    content="\n\n".join(current_chunk_parts),
                    heading=heading,
                    position=position,
                    parent_heading=parent_heading,
                    token_count=current_tokens,
                )
            )

        return chunks

    def _split_by_sentences(self, text: str) -> list[str]:
        """Split text by sentences, grouping to meet minimum token threshold."""
        # Simple sentence splitting
        sentences = re.split(r"(?<=[.!?])\s+", text)
        chunks = []
        current_parts = []
        current_tokens = 0

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            sent_tokens = self.count_tokens(sentence)

            if current_tokens + sent_tokens > self.max_tokens and current_parts:
                chunks.append(" ".join(current_parts))
                current_parts = []
                current_tokens = 0

            current_parts.append(sentence)
            current_tokens += sent_tokens

        if current_parts:
            chunks.append(" ".join(current_parts))

        return chunks

    def semantic_chunk(self, markdown: str) -> list[SemanticChunk]:
        """
        Orchestrate semantic chunking of a markdown document.

        Args:
            markdown: Raw markdown content

        Returns:
            List of SemanticChunk objects with position ordering
        """
        # First, split by headers
        sections = self.split_by_headers(markdown)

        all_chunks = []
        global_position = 0

        for section in sections:
            content = section["content"].strip()
            if not content:
                continue

            content_tokens = self.count_tokens(content)

            if content_tokens <= self.max_tokens:
                # Section fits in one chunk
                all_chunks.append(
                    SemanticChunk(
                        content=content,
                        heading=section["heading"],
                        position=global_position,
                        parent_heading=section.get("parent_heading"),
                        token_count=content_tokens,
                    )
                )
                global_position += 1
            else:
                # Section too large, split at paragraphs
                sub_chunks = self.split_at_paragraphs(
                    content,
                    section["heading"],
                    section.get("parent_heading"),
                )
                for chunk in sub_chunks:
                    chunk.position = global_position
                    global_position += 1
                    all_chunks.append(chunk)

        # Filter out chunks that are too small
        filtered_chunks = [c for c in all_chunks if c.token_count >= self.min_tokens]

        print(
            f"[SemanticChunker] Created {len(filtered_chunks)} chunks "
            f"(filtered {len(all_chunks) - len(filtered_chunks)} small chunks)"
        )

        return filtered_chunks
