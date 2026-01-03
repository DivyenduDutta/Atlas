import os
import numpy as np

from atlas.utils.embedder_utils import load_embedded_chunks, generate_embedding
from atlas.core.indexer.faiss_vector_store import FaissVectorStore

from atlas.utils.logger import LoggerConfig

LOGGER = LoggerConfig().logger

if __name__ == "__main__":
    LOGGER.info("Running indexer to save the chunk embeddings to a vector index")
    # this is the root folder which saves the following 2 files:
    # 1. index file
    # 2. metadata json
    results_save_path = r"D:\\Deep learning\\Atlas\\Resources"
    store = FaissVectorStore(
        dim=384
    )  # the encoder model we used generated embeddings of size 384
    embedded_chunks_json_file = (
        r"D:\\Deep learning\\Atlas\\Resources\\embedded_chunks.json"
    )
    embedded_chunks = load_embedded_chunks(embedded_chunks_json_file)

    store.add(
        vectors=np.array([chunk["embedding"] for chunk in embedded_chunks]),
        metadata=embedded_chunks,
    )

    store.save(results_save_path)

    # Sanity checks
    # query_text = "Role of luck in life"  # exact phrase query
    # query_text = "Folks who inspire me" # paraphrasing
    query_text = (
        "Journey is more important that the final result in life"  # paraphrasing
    )
    encoder_config_path = os.path.join(
        os.getcwd(), "atlas", "core", "configs", "sentence_transformer_config.yaml"
    )
    query_vector = generate_embedding(query_text, encoder_config_path)
    results = store.search(query_vector, k=5)
    LOGGER.info(len(results))
    for res in results:
        LOGGER.info(f"score: {res['score']}")
        LOGGER.info(f"Note title: {res['chunk_id']}")
        LOGGER.info("===\n")
