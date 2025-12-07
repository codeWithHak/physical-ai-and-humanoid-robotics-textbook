# Research Summary: RAG Ingestion Engine (Backend Initialization)

This feature's primary technical decisions were made during the specification clarification phase. This document summarizes those decisions, providing a clear rationale and outlining alternatives considered for completeness.

## Decision: Document Chunk Unique Identification

-   **What was chosen**: A combination of the source file path and a hash of the chunk content will serve as the unique identifier for each document chunk in Qdrant.
-   **Rationale**: This strategy ensures unique identification across different files and allows for efficient detection of changes within existing content. When a file is re-ingested, chunks whose content (and thus hash) have not changed can be skipped or updated selectively, preventing duplicate entries and optimizing re-ingestion performance.
-   **Alternatives considered**:
    -   Auto-incrementing integer ID: Rejected due to difficulties in managing updates and re-ingestion of specific chunks.
    -   File path + H2/H3 header text: Rejected due to brittleness if headers change and potential non-uniqueness.
    -   Qdrant-generated UUID: Rejected because it would complicate the process of updating specific existing chunks during re-ingestion.

## Decision: Data Volume and Scale Assumptions

-   **What was chosen**: The ingestion script is designed to handle approximately 15 Markdown/MDX files from the `frontend/docs/` directory.
-   **Rationale**: This reflects the current scope of the textbook content. This small scale simplifies initial implementation, reduces immediate concerns about Qdrant scaling and Gemini API rate limits, and allows for a focus on core functionality.
-   **Alternatives considered**: None explicitly, as this was a clarification of existing constraints.

## Decision: Error Handling and Logging Detail

-   **What was chosen**: The ingestion script will log critical errors and provide a summary of progress (e.g., number of files processed, chunks indexed) to stdout.
-   **Rationale**: This provides sufficient operational feedback for a local utility script without generating excessive log noise. It ensures that significant issues are immediately visible to the developer running the script, while routine progress is also reported.
-   **Alternatives considered**:
    -   Very verbose logging: Rejected as unnecessary for a local script and would create clutter.
    -   Minimal success/failure only: Rejected as insufficient for debugging.
    -   Structured logging (JSON): Rejected as overkill for a local, standalone script given the current needs.

## Decision: Gemini API Rate Limit Handling

-   **What was chosen**: The ingestion script will stop execution and report an error immediately upon encountering a rate limit or any other API error from the Google Gemini Embeddings API.
-   **Rationale**: For a local, infrequent ingestion of a small number of files, immediate error reporting is acceptable. It simplifies the script's logic by avoiding complex retry mechanisms which might be overkill for this usage pattern. The developer can manually re-run the script if a transient rate limit occurs.
-   **Alternatives considered**:
    -   Retry mechanism with exponential backoff: Rejected for its added complexity, deemed unnecessary for the current scale and local execution context.

## Decision: Chunking Strategy Refinement

-   **What was chosen**: The chunking strategy will rely solely on splitting content by H2/H3 headers, with no additional rules for maximum chunk size, overlap, or further splitting.
-   **Rationale**: H2/H3 headers in a well-structured textbook typically delineate semantically coherent sections, which is suitable for RAG. This approach keeps the chunking logic simple and aligned with the Docusaurus content structure.
-   **Alternatives considered**:
    -   Max token/word limit: Rejected to avoid breaking semantic coherence within sections.
    -   Chunk overlap: Rejected for added complexity not deemed necessary for the initial small-scale implementation.
    -   Combination of strategies: Rejected for significantly increased complexity.
