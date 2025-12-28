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

Overall chunk schema,

```json
[
  { chunk 1 },
  { chunk 2 },
  { chunk 3 }
]
```

Individual chunk schema ie, `chunk 1` is as below,

```json
{
  "chunk_id": "folder/sample note.md::Heading 1::0",
  "note_id": "folder/sample note.md",
  "title": "sample note",
  "relative_path": "folder/sample note.md",
  "heading": "Heading 1",
  "chunk_index": 0,
  "text": "Actual chunk text here...",
  "tags": ["tag1", "tag2"],
  "frontmatter": {"tags": ["personal", "health"], "date": "2023-10-01"},
  "word_count": 214
}
```

When deciding to split a note into chunks, word based splitting is used. So word = token here.

#### Chunking Strategy

```bash
IF word_count <= MAX_WORDS:
    → single chunk (whole note)

ELIF headings exist:
    → split by headings
    → IF any section > MAX_WORDS:
        → split that section further by size

ELSE (no headings):
    → split note by size
```

Note that splitting by size isnt the best option because it will almost surely cut off sentences randomly, thereby loosing context. Solving this might require more complicated heuristics or utilize yet another LLM to do semantic chunking.
