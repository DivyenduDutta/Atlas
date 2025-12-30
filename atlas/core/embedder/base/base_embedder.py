from abc import ABC
from abc import abstractmethod
from typing import List, Dict
from pathlib import Path
import json

from atlas.utils.logger import LoggerConfig

LOGGER = LoggerConfig().logger


class BaseEmbedder(ABC):
    """
    Abstract base class for all embedder implementations.

    Args:
        chunk_data_path (str): Path to the chunk data file.
        output_path (str): Path to save the embedded chunks.
        encoder_config_path (str): Path to the encoder configuration file.
    """

    def __init__(
        self, chunk_data_path: str, output_path: str, encoder_config_path: str
    ):
        LOGGER.info("-" * 20)
        LOGGER.info("Initializing Embedder.")
        self.chunk_data_path = Path(chunk_data_path)
        self.output_path = Path(output_path)
        self.encoder_config_path = Path(encoder_config_path)
        self.load_encoder()

    def read_chunk_data(self) -> List[Dict] | None:
        """Load chunk data to be embedded."""
        LOGGER.info(f"Loading chunk data from {self.chunk_data_path}")
        try:
            with self.chunk_data_path.open("r", encoding="utf-8") as f:
                chunk_data = json.load(f)
                LOGGER.info(f"Loaded {len(chunk_data)} chunks for embedding.")
                return chunk_data
        except Exception as e:
            LOGGER.error(f"Error reading chunk data file: {e}")
            return None

    @abstractmethod
    def load_encoder(self) -> None:
        """
        Load the encoder model.
        """
        pass

    def embed(self) -> None:
        """
        Main method to perform the embedding process.
        """
        chunks = self.read_chunk_data()
        assert chunks is not None, "Chunk data read should be present."
        embedded_chunks = self.embed_chunks(chunks)
        self.save_embedded_chunks(embedded_chunks)
        LOGGER.info("Embedding process completed.")

    @abstractmethod
    def embed_chunks(self, chunks: List[Dict]) -> List[Dict]:
        """
        Embed the provided chunks using the loaded encoder.

        Args:
            chunks (List[Dict]): List of chunk dictionaries to be embedded.
        """
        pass

    def save_embedded_chunks(self, embedded_chunks: List[Dict]) -> None:
        """
        Save the embedded chunks to a suitable format for later use.
        """
        tmp_path = self.output_path.with_suffix(".tmp")

        with tmp_path.open("w", encoding="utf-8") as f:
            json.dump(embedded_chunks, f, indent=2, ensure_ascii=False)

        tmp_path.replace(self.output_path)
        LOGGER.info("Embedded chunks saved successfully.")
