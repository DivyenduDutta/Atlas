import pytest
from pathlib import Path

from atlas.utils.embedder_utils import load_embedded_chunks, generate_embedding


@pytest.mark.unittest
@pytest.mark.runonci
def test_load_embedded_chunks_positive(dummy_embedded_chunk_data_path: Path) -> None:
    """
    Test if embedded chunks data can be successfully loaded from json file.

    Args:
        dummy_embedded_chunk_data_path (Path): The path to the dummy embedded chunks json file.
    """

    metadata = load_embedded_chunks(str(dummy_embedded_chunk_data_path))
    assert len(metadata) == 1
    assert metadata[0]["chunk_id"] == "test Note.md::test_heading::chunk_0"


@pytest.mark.unittest
@pytest.mark.runonci
def test_load_embedded_chunks_negative(tmp_path: Path) -> None:
    """
    Test if exception is raised if the embedded chunks json file isnt available.

    Args:
        tmp_path (Path): Temporary path provided by pytest.
    """

    dummy_embedded_chunk_data_path = (
        tmp_path / "embedded_chunks.json"
    )  # file on this path doesnt exist
    with pytest.raises(Exception) as exc_info:
        _ = load_embedded_chunks(str(dummy_embedded_chunk_data_path))
    assert "Error loading embedded chunks json file" in str(exc_info.value)


@pytest.mark.unittest
@pytest.mark.runonci
def test_generate_embedding(dummy_encoder_config_path: Path) -> None:
    """
    Test encoder model generates proper embedding for a given text.

    Args:
        dummy_encoder_config_path (Path): The path to the dummy encoder configuration file.
    """

    text = "Hi, my name is Bob Ross!"
    embedding = generate_embedding(text, str(dummy_encoder_config_path))
    assert embedding.shape == (384,)
