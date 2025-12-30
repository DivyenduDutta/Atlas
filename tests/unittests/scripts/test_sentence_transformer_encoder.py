import pytest

from atlas.core.embedder.config import EncoderConfig
from atlas.core.embedder.sentence_transformer.impl_encoder import (
    SentenceTransformerEncoder,
)
from sentence_transformers import SentenceTransformer


@pytest.mark.unittest
@pytest.mark.runonci
def test_load(dummy_encoder_config: EncoderConfig):
    """
    Test the model loading functionality of the SentenceTransformerEncoder wrapper.

    Args:
        dummy_encoder_config (EncoderConfig): Loaded encoder configuration data.
    """
    encoder = SentenceTransformerEncoder(dummy_encoder_config)
    assert encoder.model is not None
    assert isinstance(encoder.model, SentenceTransformer)


@pytest.mark.unittest
@pytest.mark.runonci
def test_encode(dummy_encoder_config: EncoderConfig):
    """
    Test the loaded encoder model's encoding functionality of the SentenceTransformerEncoder wrapper.

    Args:
        dummy_encoder_config (EncoderConfig): Loaded encoder configuration data.
    """
    encoder = SentenceTransformerEncoder(dummy_encoder_config)
    encoder.load()
    texts = ["lorem ipsum", "do re mi fa so la ti", "hello world"]
    embeddings = encoder.encode(texts)
    assert embeddings.shape == (3, 384)
