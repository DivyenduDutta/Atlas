from sentence_transformers import SentenceTransformer
import numpy as np
import torch

from atlas.core.embedder.base.base_encoder import BaseEncoder
from atlas.core.embedder.config import EncoderConfig
from atlas.utils.logger import LoggerConfig

from typing import List

LOGGER = LoggerConfig().logger


class SentenceTransformerEncoder(BaseEncoder):
    """
    Sentence Transformer Encoder Wrapper.

    Args:
        config (EncoderConfig): Configuration for the encoder.
    """

    def __init__(self, config: EncoderConfig):
        LOGGER.info("-" * 20)
        LOGGER.info("Initializing Sentence Transformer Encoder Wrapper")
        self.config = config
        self.model: SentenceTransformer | None = None
        self.load()

    def load(self) -> None:
        """Load the Sentence Transformer model."""
        if self.model is not None:
            return

        if self.config.device == "cuda":
            device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model = SentenceTransformer(self.config.model_name, device=device)
        LOGGER.info(f"Loaded Sentence Transformer model: {self.config.model_name}")

    def encode(self, texts: List[str]) -> np.ndarray:
        """
        Encode a List of texts into embeddings.

        Args:
            texts (List[str]): List of texts to encode.

        Returns:
            np.ndarray: Array of embeddings.
        """
        LOGGER.info(f"Encoding {len(texts)} texts using Sentence Transformer model.")

        assert self.model is not None, "Model must be loaded before encoding"

        embeddings = self.model.encode(
            texts,
            batch_size=self.config.batch_size,
            show_progress_bar=True,
            normalize_embeddings=self.config.normalize_embeddings,
        )

        return embeddings
