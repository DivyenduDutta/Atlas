import pytest
import json
from pathlib import Path
from typing import List, Dict

from atlas.core.embedder.sentence_transformer.impl_embedder import (
    SentenceTransformerEmbedder,
)
from atlas.core.embedder.sentence_transformer.impl_encoder import (
    SentenceTransformerEncoder,
)


@pytest.fixture
def dummy_chunks() -> List[Dict]:
    """
    Create a dummy chunks for testing.

    Returns:
        List[Dict]: The dummy chunk data.
    """
    dummy_chunk_data = [
        {
            "chunk_id": "test Note.md::test_heading::chunk_0",
            "note_id": "test Note.md",
            "title": "Test Note",
            "relative_path": "test_note.md",
            "heading": "Test Heading",
            "chunk_index": 0,
            "text": "This is a test chunk.",
            "word_count": 5,
            "tags": [],
            "frontmatter": {},
        },
        {
            "chunk_id": "test Note 2.md::test_heading::chunk_0",
            "note_id": "test Note 2.md",
            "title": "Test Note 2",
            "relative_path": "test_note 2.md",
            "heading": "Test Heading 2",
            "chunk_index": 0,
            "text": "This is a test chunk 2.",
            "word_count": 6,
            "tags": [],
            "frontmatter": {},
        },
    ]
    return dummy_chunk_data


@pytest.mark.unittest
@pytest.mark.runonci
def test_load_encoder(dummy_encoder_config_path: Path):
    """
    Test SentenceTransformerEmbedder's encoder loading functionality.

    Args:
        dummy_encoder_config_path (Path): The path to the dummy encoder configuration file.
    """
    # Encoder is loaded when `SentenceTransformerEmbedder` is initialized. No need to call separately
    embedder = SentenceTransformerEmbedder(
        "dummy_chunked_data.json", "dummy.json", str(dummy_encoder_config_path)
    )
    assert embedder.encoder is not None
    assert isinstance(embedder.encoder, SentenceTransformerEncoder)


@pytest.mark.unittest
@pytest.mark.runonci
def test_embed_chunks_positive(
    dummy_encoder_config_path: Path, dummy_chunks: List[Dict]
):
    """
    Test SentenceTransformerEmbedder's functionality to generate embeddings for provided chunks.

    Args:
        dummy_encoder_config_path (Path): The path to the dummy encoder configuration file.
        dummy_chunks (List[Dict]): The provided dummy chunks.
    """
    embedder = SentenceTransformerEmbedder(
        "dummy_chunked_data.json", "dummy.json", str(dummy_encoder_config_path)
    )
    embedded_chunks = embedder.embed_chunks(dummy_chunks)
    assert len(embedded_chunks) == len(dummy_chunks)
    assert "embedding" in embedded_chunks[0].keys()
    assert len(embedded_chunks[0]["embedding"]) == 384


@pytest.mark.unittest
@pytest.mark.runonci
def test_embed_chunks_negative(dummy_encoder_config_path: Path):
    """
    Test SentenceTransformerEmbedder's functionality to fail in generating embeddings for
    provided chunks when no chunk data is passed to `SentenceTransformerEmbedder.embed_chunks()`.

    Args:
        dummy_encoder_config_path (Path): The path to the dummy encoder configuration file.
    """
    embedder = SentenceTransformerEmbedder(
        "dummy_chunked_data.json", "dummy.json", str(dummy_encoder_config_path)
    )
    embedded_chunks = embedder.embed_chunks([])
    assert len(embedded_chunks) == 0


@pytest.mark.unittest
@pytest.mark.runonci
def test_read_chunk_data_positive(
    dummy_encoder_config_path: Path, dummy_chunk_data_path: Path
):
    """
    Test SentenceTransformerEmbedder's functionality to read chunk data from the provided chunk data
    path.

    Args:
        dummy_encoder_config_path (Path): The path to the dummy encoder configuration file.
        dummy_chunk_data_path (Path): The path to the provided chunk data path.
    """
    embedder = SentenceTransformerEmbedder(
        str(dummy_chunk_data_path), "dummy.json", str(dummy_encoder_config_path)
    )
    chunks = embedder.read_chunk_data()
    assert chunks is not None
    assert len(chunks) == 1
    assert isinstance(chunks[0], dict)
    assert chunks[0]["chunk_id"] == "test Note.md::test_heading::chunk_0"


@pytest.mark.unittest
@pytest.mark.runonci
def test_read_chunk_data_negative(
    dummy_encoder_config_path: Path, dummy_chunk_data_path: Path
):
    """
    Test SentenceTransformerEmbedder's failure to read chunk data from the provided chunk data
    path when the provided chunk data path doesnt exist.

    Args:
        dummy_encoder_config_path (Path): The path to the dummy encoder configuration file.
        dummy_chunk_data_path (Path): The path to the provided chunk data path.
    """
    dummy_chunk_data_path = (
        dummy_chunk_data_path.parent / "dummy_chunked_data.json"
    )  # doesnt exist
    embedder = SentenceTransformerEmbedder(
        str(dummy_chunk_data_path), "dummy.json", str(dummy_encoder_config_path)
    )
    chunks = embedder.read_chunk_data()
    assert chunks is None


@pytest.mark.unittest
@pytest.mark.runonci
def test_save_embedded_chunks(tmp_path: Path, dummy_encoder_config_path: Path):
    """
    Test SentenceTransformerEmbedder's functionality to save the generated embedded chunk data.

    Args:
        tmp_path (Path): Temporary directory provided by pytest.
        dummy_encoder_config_path (Path): The path to the dummy encoder configuration file.
    """
    output_file_path = tmp_path / "embedded_chunks.json"
    dummy_embedded_chunks = [
        {
            "chunk_id": "test Note.md::test_heading::chunk_0",
            "note_id": "test Note.md",
            "title": "Test Note",
            "relative_path": "test_note.md",
            "heading": "Test Heading",
            "chunk_index": 0,
            "text": "This is a test chunk.",
            "word_count": 5,
            "tags": [],
            "frontmatter": {},
            "embedding": [float(i) for i in range(384)],
        }
    ]
    embedder = SentenceTransformerEmbedder(
        "dummy_chunked_data.json", str(output_file_path), str(dummy_encoder_config_path)
    )
    embedder.save_embedded_chunks(dummy_embedded_chunks)
    assert output_file_path.exists()
    with output_file_path.open("r", encoding="utf-8") as f:
        saved_data = json.load(f)
    assert saved_data == dummy_embedded_chunks


@pytest.mark.unittest
@pytest.mark.runonci
def test_embed(
    tmp_path: Path, dummy_chunk_data_path: Path, dummy_encoder_config_path: Path
):
    """
    Test SentenceTransformerEmbedder's overall functionality to generate the embedded chunk data
    from the chunks in the provided chunk data path.

    Args:
        tmp_path (Path): Temporary directory provided by pytest.
        dummy_chunk_data_path (Path): The path to the provided chunk data path.
        dummy_encoder_config_path (Path): The path to the dummy encoder configuration file.
    """
    output_file_path = tmp_path / "embedded_chunks.json"
    embedder = SentenceTransformerEmbedder(
        str(dummy_chunk_data_path),
        str(output_file_path),
        str(dummy_encoder_config_path),
    )
    embedder.embed()
    assert output_file_path.exists()
    with output_file_path.open("r", encoding="utf-8") as f:
        saved_data = json.load(f)

    assert len(saved_data[0]["embedding"]) == 384
