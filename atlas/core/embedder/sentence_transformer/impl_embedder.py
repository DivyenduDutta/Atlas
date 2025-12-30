import os
from typing import List, Dict

from atlas.core.embedder.base.base_embedder import BaseEmbedder
from atlas.core.embedder.config import load_encoder_config
from atlas.core.embedder.sentence_transformer.impl_encoder import (
    SentenceTransformerEncoder,
)
from atlas.utils.logger import LoggerConfig

LOGGER = LoggerConfig().logger


class SentenceTransformerEmbedder(BaseEmbedder):
    """Embedder implementation using Sentence Transformers."""

    def __init__(
        self, chunk_data_path: str, output_path: str, encoder_config_path: str
    ):
        super().__init__(chunk_data_path, output_path, encoder_config_path)

    def load_encoder(self) -> None:
        """Load the Sentence Transformer encoder model."""

        embedding_config = load_encoder_config(self.encoder_config_path)
        encoder = SentenceTransformerEncoder(embedding_config)
        self.encoder = encoder

    def embed_chunks(self, chunks: List[Dict]) -> List[Dict]:
        """
        Embed the provided chunks using the loaded encoder.

        Args:
            chunks (List[Dict]): List of chunk dictionaries to be embedded.

        Returns:
            List[Dict]: List of chunk dictionaries with added embeddings.
        """
        if not chunks:
            LOGGER.warning("No chunks provided for embedding.")
            return []

        texts = [chunk["text"] for chunk in chunks]

        embeddings = self.encoder.encode(texts)

        if len(embeddings) != len(chunks):
            LOGGER.error("Embedding count does not match chunk count.")
            raise ValueError("Embedding count does not match chunk count")

        embedded_chunks = []

        for chunk, embedding in zip(chunks, embeddings):
            embedded_chunk = {
                **chunk,
                "embedding": embedding.tolist(),  # Convert numpy array to list for JSON serialization
            }
            embedded_chunks.append(embedded_chunk)

        return embedded_chunks


if __name__ == "__main__":
    chunk_data_path = r"D:\\Deep learning\\Atlas\\Resources\\chunked_data.json"
    output_path = r"D:\\Deep learning\\Atlas\\Resources\\embedded_chunks.json"
    encoder_config_path = os.path.join(
        os.getcwd(), "atlas", "core", "configs", "sentence_transformer_config.yaml"
    )
    embedder = SentenceTransformerEmbedder(
        chunk_data_path, output_path, encoder_config_path
    )
    embedder.embed()
