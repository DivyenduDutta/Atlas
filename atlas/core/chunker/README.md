## Chunker Module

Chunking is used to convert the notes from an Obsidian Vault to "retrieval units".

Why is chunking necessary?

Chunking exists because notes can be larger than an LLM’s context window. Embeddings + retrieval work best on smaller, focused text units. So we split notes into chunks, but not randomly, not purely by token count, along coherent boundaries (headings, sections, structure).

Smaller, focused chunks = higher signal-to-noise.

RAG criteria for good chunks:

- Self-contained
    - Reads fine without extra context
    - Clear theme

- Properly sized
    - Not too small (wasteful)
    - Not too large (retrieval-safe)

- Traceable
    - Know exactly where it came from
    - Can cite it cleanly

- Future-proof
    - Embedding-friendly
    - Retrieval-friendly
    - LLM-friendly

#### Structural Chunking

Chunk along:
- headings
- sections
- paragraphs
- author-defined boundaries
