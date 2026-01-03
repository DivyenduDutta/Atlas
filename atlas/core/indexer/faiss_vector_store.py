import faiss
import numpy as np
from typing import List, Dict
from pathlib import Path
import json

from atlas.core.indexer.base_vector_store import BaseVectorStore
from atlas.utils.logger import LoggerConfig

LOGGER = LoggerConfig().logger


class FaissVectorStore(BaseVectorStore):
    """
    Vector store using FAISS (Facebook AI Semantic Search) library.
    Currently uses Flat Indexing but can be changed as needed.

    Args:
        dim (int): Number of dimensions of the embeddings/vectors.
    """

    def __init__(self, dim: int):
        LOGGER.info("-" * 20)
        LOGGER.info("Initializing Indexer.")
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)
        self.metadata: List[Dict] = []

    def add(self, vectors: np.ndarray, metadata: List[Dict]) -> None:
        """
        Add the vector embeddings to the FAISS vector index and the corresponding
        chunks to the metatdata.

        Args:
            vectors (np.ndarray): Vector embeddings to add to the FAISS vector store.
            metadata (List[Dict]): Corresponding list of chunk dictionaries.
        """

        if vectors.ndim != 2 or vectors.shape[1] != self.dim:
            LOGGER.error(
                f"Invalid vector shape. Expected num of dim = 2 and size of vector = {self.dim}"
            )
            raise ValueError(
                f"Invalid vector shape. Expected num of dim = 2 and size of vector = {self.dim}"
            )

        if len(vectors) != len(metadata):
            LOGGER.error("Vectors and metadata length mismatch")
            raise ValueError("Vectors and metadata length mismatch")

        # we append metadata in the same order we add vectors
        # this is to enforce the invariant `FAISS vector ID <-> metadata list index`
        # this also means that when passing `vectors` and `metadata` to `add()`,
        # they need to by synced
        self.index.add(vectors)
        self.metadata.extend(metadata)

    def search(self, query_vector: np.ndarray, k: int) -> List[Dict]:
        """
        Search a query (via its embedding/vector) in the FAISS vector store.

        Args:
            query_vector (np.ndarray): Embedding of the query to search in the FAISS vector store.
            k (int): Number of most similar embeddings (aka neighbors) to the query vector.

        Returns:
            List[Dict]: List of dictionaries of the most similar embeddings to the query vector.
                        Each dictionary contains the score (probability) for each similar embedding
                        match along with the full chunk metadata.
        """

        if k > self.index.ntotal:
            LOGGER.error(f"k is more than maximum possible value : {self.index.ntotal}")
            raise Exception(
                f"k is more than maximum possible value : {self.index.ntotal}"
            )

        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(
                1, -1
            )  # add first dimension as batch == 1

        scores, indices = self.index.search(query_vector, k)

        # search() returns two arrays:
        # scores:   shape (n_queries, k)
        # indices:  shape (n_queries, k)

        results = []
        for score, idx in zip(
            scores[0], indices[0]
        ):  # use 0th element because we have 1 query vector
            if idx == -1:  # guard for neighbor not found for given query vector
                continue

            result = {"score": float(score), **self.metadata[idx]}
            results.append(result)

        LOGGER.info(f"Number of similar embeddings found : {len(results)}")
        LOGGER.info(
            f"Chunk with highest match : {results[0]['score']} is {results[0]['chunk_id']}"
        )
        return results

    def save(self, results_save_path: str) -> None:
        """
        Save the following two files:
        1. index file -> index.faiss
        2. chunk metadata -> metadata.json

        Ensure that the elements in the two files are in sync
        ie, `FAISS vector ID <-> metadata list index`

        Args:
            results_save_path (str): Directory to save the above mentioned two result files.
        """

        _results_save_path = Path(results_save_path)
        _results_save_path.mkdir(parents=True, exist_ok=True)

        faiss.write_index(self.index, str(_results_save_path / "index.faiss"))

        metadata_save_path = _results_save_path / "metadata.json"
        tmp_path = metadata_save_path.with_suffix(".tmp")
        with (tmp_path).open("w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)

        tmp_path.replace(metadata_save_path)
        LOGGER.info(
            f"Index file and chunk metadata saved successfully to directory : {results_save_path}"
        )

    def load(self, results_load_path: str) -> None:
        """
        Load the following two files:
        1. index file -> index.faiss
        2. chunk metadata -> metadata.json

        Use this in case we dont want to build the index and metadata from scratch and already
        have both of them saved.

        Args:
            results_load_path (str): Directory to load the above mentioned two result files from.
        """

        _results_load_path = Path(results_load_path)
        try:
            self.index = faiss.read_index(str(_results_load_path / "index.faiss"))

            with (_results_load_path / "metadata.json").open(
                "r", encoding="utf-8"
            ) as f:
                self.metadata = json.load(f)

            LOGGER.info(
                f"Index file and chunk metadata loaded successfully from directory : {results_load_path}"
            )
        except Exception as e:
            LOGGER.error(f"Error reading either index file or metadata file : {e}")
            raise Exception(f"Error reading either index file or metadata file : {e}")
