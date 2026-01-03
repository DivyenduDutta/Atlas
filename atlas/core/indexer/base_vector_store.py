from abc import ABC
from abc import abstractmethod
from typing import List, Dict
import numpy as np


class BaseVectorStore(ABC):
    """
    Abstract base class for a vector store. Used for vector indexing.
    """

    @abstractmethod
    def add(self, vectors: np.ndarray, metadata: List[Dict]) -> None:
        """
        Add the vector embeddings to the vector index and the corresponding
        chunks to the metatdata.

        Args:
            vectors (np.ndarray): Vector embeddings to add to the vector store.
            metadata (List[Dict]): Corresponding list of chunk dictionaries.
        """
        pass

    @abstractmethod
    def search(self, query_vector: np.ndarray, k: int) -> List[Dict]:
        """
        Search a query (via its embedding) in the vector store.

        Args:
            query_vector (np.ndarray): Embedding of the query to search in the vector store.
            k (int): Number of most similar embeddings (aka neighbors) to the query vector.

        Returns:
            List[Dict]: List of dictionaries of the most similar embeddings to the query vector.
        """
        pass

    @abstractmethod
    def save(self, results_save_path: str):
        """
        Save the following two files:
        1. index file
        2. chunk metadata

        Ensure that the elements in the two files are in sync
        ie, `vector ID <-> metadata list index`

        Args:
            results_save_path (str): Directory to save the above mentioned two result files.
        """
        pass

    @abstractmethod
    def load(self, results_load_path: str):
        """
        Load the following two files:
        1. index file
        2. chunk metadata

        Use this in case we dont want to build the index and metadata from scratch and already
        have both of them saved.

        Args:
            results_load_path (str): Directory to load the above mentioned two result files from.
        """
        pass
