from abc import ABC
from abc import abstractmethod
from typing import List
import numpy as np

from atlas.utils.logger import LoggerConfig

LOGGER = LoggerConfig().logger


class BaseEncoder(ABC):
    """Abstract base class for the encoder wrapper."""

    @abstractmethod
    def load(self) -> None:
        """
        Loads the encoder model.

        """
        pass

    @abstractmethod
    def encode(self, texts: List[str]) -> np.ndarray:
        """
        Encodes a list of texts into their corresponding embeddings.

        Args:
            texts (list[str]): A list of texts to be encoded.

        Returns:
            np.ndarray: An array of embeddings corresponding to the input texts.
        """
        pass
