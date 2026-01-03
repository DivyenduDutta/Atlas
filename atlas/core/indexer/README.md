## Indexer Module

Indexing as a general concept is used to enhance speed of search and retrieval (ie, lookup) at the expense of storage space. And an index is a data structure that allows us to do this.A

> We could scan all our data every time.
> An index exists so we don’t have to.

Its used in various places like,
- databases
- search engines
- vector stores
- compilers

### Why do indexing if I can just use the encoder to give me top K chunks?

We can skip indexing when our data is small. We do indexing because computing similarity against everything doesn’t scale. Indexing exists to make nearest-neighbor search fast.

When we use the encoder to get the top K chunks for a query, internally it ends up comparing against all the vector embeddings we have.

```bash
for each chunk:
    similarity(query_embedding, chunk_embedding)
```

Time Complexity : `O(N × d)` where `N` = number of chunks and `d` = embedding dimension

### Vector indexing library

[FAISS](https://faiss.ai/index.html), a vector indexing library was chosen instead of a vector DB to have more control when building the vector index.
