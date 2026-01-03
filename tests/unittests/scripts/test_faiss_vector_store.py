import json
import pytest
import numpy as np
from pathlib import Path
import faiss

from atlas.core.indexer.faiss_vector_store import FaissVectorStore
from atlas.utils.embedder_utils import load_embedded_chunks


@pytest.mark.unittest
@pytest.mark.runonci
def test_add_positive(dummy_embedded_chunk_data_path: Path) -> None:
    """
    Test if embeddings/vectors can be added to the FAISS vector store.

    Args:
        dummy_embedded_chunk_data_path (Path): The path to the dummy embedded chunks json file.
    """
    vectors = np.array([[1, 2, 3]])
    embedded_chunks = load_embedded_chunks(str(dummy_embedded_chunk_data_path))
    store = FaissVectorStore(dim=3)
    store.add(vectors, embedded_chunks)
    assert store.index.ntotal == len(vectors)
    assert len(store.metadata) == len(embedded_chunks)


@pytest.mark.unittest
@pytest.mark.runonci
def test_add_negative_invalid_embedding_shape(
    dummy_embedded_chunk_data_path: Path,
) -> None:
    """
    Test if exception is raised if the embedding(s) to be added to the FAISS vector
    store has incorrect shape.

    Args:
        dummy_embedded_chunk_data_path (Path): The path to the dummy embedded chunks json file.
    """
    vectors = np.array([1, 2])
    embedded_chunks = load_embedded_chunks(str(dummy_embedded_chunk_data_path))
    store = FaissVectorStore(dim=3)
    with pytest.raises(ValueError) as exc_info:
        store.add(vectors, embedded_chunks)
    assert "Invalid vector shape. Expected num of dim = 2 and size of vector" in str(
        exc_info.value
    )


@pytest.mark.unittest
@pytest.mark.runonci
def test_add_negative_length_mismatch(dummy_embedded_chunk_data_path: Path) -> None:
    """
    Test if exception is raised if the length of the embeddings/vectors and
    associated metadata does not match when adding embedding(s) to the FAISS
    vector store.

    Args:
        dummy_embedded_chunk_data_path (Path): The path to the dummy embedded chunks json file.
    """
    vectors = np.array([[1, 2, 3], [2, 3, 4]])
    embedded_chunks = load_embedded_chunks(str(dummy_embedded_chunk_data_path))
    store = FaissVectorStore(dim=3)
    with pytest.raises(ValueError) as exc_info:
        store.add(vectors, embedded_chunks)
    assert "Vectors and metadata length mismatch" in str(exc_info.value)


@pytest.mark.unittest
@pytest.mark.runonci
def test_search_positive(dummy_embedded_chunk_data_path: Path) -> None:
    """
    Test if the FAISS store can successfully search for neighbor embeddings for a
    provided input embedding.

    Args:
        dummy_embedded_chunk_data_path (Path): The path to the dummy embedded chunks json file.
    """
    vectors = np.array([[1, 2, 3]])
    embedded_chunks = load_embedded_chunks(str(dummy_embedded_chunk_data_path))
    store = FaissVectorStore(dim=3)
    store.add(vectors, embedded_chunks)
    query_vector = np.array([1, 2, 2])
    k = 1
    results = store.search(query_vector, k)
    assert len(results) == k
    assert "score" in results[0].keys()


@pytest.mark.unittest
@pytest.mark.runonci
def test_search_negative_large_k(dummy_embedded_chunk_data_path: Path) -> None:
    """
    Test if exeception is raised if the number of neighbors ie, `k` to be searched
    in the vector store for an input embedding is more than the maximum embeddings
    saved in the vector store.

    Args:
        dummy_embedded_chunk_data_path (Path): The path to the dummy embedded chunks json file.
    """
    vectors = np.array([[1, 2, 3]])
    embedded_chunks = load_embedded_chunks(str(dummy_embedded_chunk_data_path))
    store = FaissVectorStore(dim=3)
    store.add(vectors, embedded_chunks)
    query_vector = np.array([[1, 2, 2]])
    k = 3
    with pytest.raises(Exception) as exc_info:
        _ = store.search(query_vector, k)
    assert "k is more than maximum possible value" in str(exc_info.value)


@pytest.mark.unittest
@pytest.mark.runonci
def test_save(tmp_path: Path, dummy_embedded_chunk_data_path: Path) -> None:
    """
    Test if generated index and metadata files can be saved.

    Args:
        tmp_path (Path): Temporary path provided by pytest.
        dummy_embedded_chunk_data_path (Path): The path to the dummy embedded chunks json file.
    """
    vectors = np.array([[1, 2, 3]])
    embedded_chunks = load_embedded_chunks(str(dummy_embedded_chunk_data_path))
    store = FaissVectorStore(dim=3)
    store.add(vectors, embedded_chunks)
    results_save_path = tmp_path / "Results"
    store.save(str(results_save_path))
    index_file_path = results_save_path / "index.faiss"
    metadata_file_path = results_save_path / "metadata.json"

    assert index_file_path.exists()
    index_data = faiss.read_index(str(index_file_path))
    assert index_data.ntotal == len(vectors)

    assert metadata_file_path.exists()
    with metadata_file_path.open("r", encoding="utf-8") as f:
        metadata_data = json.load(f)
    assert len(metadata_data) == len(embedded_chunks)


@pytest.mark.unittest
@pytest.mark.runonci
def test_load_positive(tmp_path: Path, dummy_embedded_chunk_data_path: Path) -> None:
    """
    Test if saved index and metadata files can be loaded.

    Args:
        tmp_path (Path): Temporary path provided by pytest.
        dummy_embedded_chunk_data_path (Path): The path to the dummy embedded chunks json file.
    """
    vectors = np.array([[1, 2, 3]])
    embedded_chunks = load_embedded_chunks(str(dummy_embedded_chunk_data_path))
    store = FaissVectorStore(dim=3)
    store.add(vectors, embedded_chunks)
    results_save_path = tmp_path / "Results"
    store.save(str(results_save_path))
    index_file_path = results_save_path / "index.faiss"
    metadata_file_path = results_save_path / "metadata.json"
    store.load(results_load_path=str(results_save_path))

    assert index_file_path.exists()
    index_data = faiss.read_index(str(index_file_path))
    assert index_data.ntotal == len(vectors)

    assert metadata_file_path.exists()
    with metadata_file_path.open("r", encoding="utf-8") as f:
        metadata_data = json.load(f)
    assert len(metadata_data) == len(embedded_chunks)


@pytest.mark.unittest
@pytest.mark.runonci
def test_load_negative_file_not_found(
    tmp_path: Path, dummy_embedded_chunk_data_path: Path
) -> None:
    """
    Test if exception is raised if the index or metadata file is not found when trying to load them.

    Args:
        tmp_path (Path): Temporary path provided by pytest.
        dummy_embedded_chunk_data_path (Path): The path to the dummy embedded chunks json file.
    """
    vectors = np.array([[1, 2, 3]])
    embedded_chunks = load_embedded_chunks(str(dummy_embedded_chunk_data_path))
    store = FaissVectorStore(dim=3)
    store.add(vectors, embedded_chunks)
    results_save_path = tmp_path / "Results"
    store.save(str(results_save_path))
    results_load_path = tmp_path / "Res"  # folder doesnt exist

    with pytest.raises(Exception) as exc_info:
        store.load(results_load_path=str(results_load_path))
    assert "Error reading either index file or metadata file" in str(exc_info.value)
