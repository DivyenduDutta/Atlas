import json
from pathlib import Path
from typing import List, Dict
import numpy as np

from atlas.core.embedder.config import load_encoder_config
from atlas.core.embedder.sentence_transformer.impl_encoder import (
    SentenceTransformerEncoder,
)

from atlas.utils.logger import LoggerConfig

LOGGER = LoggerConfig().logger


def load_embedded_chunks(path: str) -> List[Dict]:
    """
    Load and return the list of chunk dictionaries with added embeddings.

    Args:
        path (str): Path to the list of chunk dictionaries json file.

    Returns:
        List[Dict]: The list of chunk dictionaries with added embeddings.
    """

    _path = Path(path)
    try:
        with (_path).open("r", encoding="utf-8") as f:
            metadata = json.load(f)
    except Exception as e:
        LOGGER.error(f"Error loading embedded chunks json file : {e}")
        raise Exception(f"Error loading embedded chunks json file : {e}")

    LOGGER.info(f"Embedded chunks json successfully loaded from {str(path)}")
    return metadata


def generate_embedding(text: str, encoder_config_path: str) -> np.ndarray:
    """
    Generate the embedding/vector for a given text using the configuration settings
    for a specific encoder.

    Args:
        text (str): `text` for which to generate embeddings.
        encoder_config_path (str): Path to the configuration settings file for the encoder.

    Returns:
        np.ndarray: Embedding/vector for the provided `text`.
    """
    texts = [text]
    _encoder_config_path = Path(encoder_config_path)
    embedding_config = load_encoder_config(_encoder_config_path)
    encoder = SentenceTransformerEncoder(embedding_config)
    embedding = encoder.encode(texts)
    return embedding
