import json
import pytest
import numpy as np
from pathlib import Path
import faiss

from atlas.core.indexer.faiss_vector_store import FaissVectorStore
from atlas.core.retriever.context import retrieve_context
from atlas.utils.embedder_utils import load_embedded_chunks


@pytest.mark.unittest
@pytest.mark.runonci
def test_retrieve_context(tmp_path: Path, dummy_embedded_chunk_data_path: Path) -> None:
    """
    Test context retrieval functionality given a user query.

    Args:
        tmp_path (Path): Temporary path provided by pytest.
        dummy_embedded_chunk_data_path (Path): The path to the dummy embedded chunks json file.
    """
    vectors = np.array([[i for i in range(384)]])
    embedded_chunks = load_embedded_chunks(str(dummy_embedded_chunk_data_path))
    store = FaissVectorStore(dim=384)
    store.add(vectors, embedded_chunks)
    results_save_path = tmp_path / "Results"
    store.save(str(results_save_path))

    user_query = "test note is used for testing"
    k = 1
    context = retrieve_context(
        results_load_path=str(results_save_path), user_query=user_query, k=k
    )

    assert context != None and len(context) != 0
