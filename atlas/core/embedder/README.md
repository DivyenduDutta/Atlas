## Embedder Module

LLM's dont really understand text. Hence, the text needs to be converted to a numeric representation, more specifically a vector called embedding. This is just a numeric representation in a low dimensional space. Two vectors close to each other in this space represent two texts which are close to each other semantically.

### Encoder Model Choice

`sentence-transformers/all-MiniLM-L6-v2` from [Sentence Transformers](https://www.sbert.net/) was chosen because its,
- fast and lightweight (super important for latency)
- provides really good [semantic search](https://www.sbert.net/examples/sentence_transformer/applications/semantic-search/README.html#background) performance


The encoder model is ultimately used for semantic search.

#### What is Semantic Search?

1. Take chunks → embed into vector space
2. Take query → embed into same space
3. Find nearest neighbors (cosine / dot / L2)
4. Return top-k chunks

#### Why not use TinyLLama's encoder

- There are three types of Transformer models
    - Encoder only models
        - eg, BERT, ROBERTa, MiniLM
    - Decoder only models
        - LLama/TinyLlama/GPT-2
        - they dont have an explicit encoder model in their architecture but they do encoding on text internally
    - Encoder - Decoder models
        - BART, T5, FLAN

- TinyLlama being a decoder only model is specifically trained for next token prediction (the encoding is still done but its not the main focus and it does not have an encoder in the architectural sense).
- Whereas encoder only models are specifically trained generate embeddings and further use cases of embeddings (like retrieval, semantic search)

#### Structure of embedding chunks json

```json
[
  {
    "chunk_id": "folder/sample note.md::Heading 1::0",
    "note_id": "folder/sample note.md",
    "title": "sample note",
    "relative_path": "folder/sample note.md",
    "heading": "Heading 1",
    "chunk_index": 0,
    "text": "lorem ipsum",
    "word_count": 2,
    "tags": [],
    "frontmatter": {},
    "embedding": [
      0.017203988507390022,
      0.06233978644013405,
      -0.011157829314470291,
      -0.012113398872315884,
      ...
    ]
  },
  ...
]
```
- This is same as the json output of the chunker module with the added `embedding` key. This represents the vector representation of the `text` as provided by the chosen encoder model.
