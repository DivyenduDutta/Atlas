import pytest
import json
from pathlib import Path

from atlas.core.chunker.structural_chunker import StructuralChunker


@pytest.mark.unittest
@pytest.mark.runonci
def test_read_processed_data_positive(dummy_processed_data_path: Path):
    """
    Test reading processed data from a valid JSON file.

    Args:
        dummy_processed_data_path (Path): Path to the dummy processed data file.
    """
    chunker = StructuralChunker(
        processed_data_path=str(dummy_processed_data_path),
        output_path=str(dummy_processed_data_path.parent / "chunked_data.json"),
        max_words=250,
    )
    processed_data = chunker.read_processed_data()
    assert processed_data is not None
    assert len(processed_data) == 2
    assert (
        processed_data[0]["note_id"]
        == "_learning about me/what I learnt about myself when dealing with ADHD.md"
    )
    assert processed_data[1]["note_id"] == "_Meditations/Games and Life.md"


@pytest.mark.unittest
@pytest.mark.runonci
def test_read_processed_data_negative_file_not_found(tmp_path: Path):
    """
    Test reading processed data from a non-existent file.

    Args:
        tmp_path (Path): Temporary directory provided by pytest.
    """
    non_existent_path = tmp_path / "non_existent_file.json"
    chunker = StructuralChunker(
        processed_data_path=str(non_existent_path),
        output_path=str(tmp_path / "chunked_data.json"),
        max_words=250,
    )
    processed_data = chunker.read_processed_data()
    assert processed_data is None


@pytest.mark.unittest
@pytest.mark.runonci
def test_split_by_word_limit():
    """Test splitting text by word limit."""
    chunker = StructuralChunker(
        processed_data_path="dummy_path", output_path="dummy_output", max_words=5
    )
    text = "This is a test sentence to check the splitting functionality."
    sub_chunks = chunker._split_by_word_limit(text, chunker.max_words)
    assert len(sub_chunks) == 2
    assert sub_chunks[0] == "This is a test sentence"
    assert sub_chunks[1] == "to check the splitting functionality."


@pytest.mark.unittest
@pytest.mark.runonci
def test_split_by_headings():
    """Test splitting text by headings."""
    chunker = StructuralChunker(
        processed_data_path="dummy_path", output_path="dummy_output", max_words=250
    )
    text = "## Heading 1\nThis is some text under heading 1.\n## Heading 2\nThis is some text under heading 2."
    sections = chunker._split_by_headings(text)
    assert len(sections) == 2
    assert sections[0]["heading"] == "Heading 1"
    assert sections[0]["text"] == "This is some text under heading 1."
    assert sections[1]["heading"] == "Heading 2"
    assert sections[1]["text"] == "This is some text under heading 2."


@pytest.mark.unittest
@pytest.mark.runonci
def test_make_chunk():
    """Test making a chunk from a note."""
    chunker = StructuralChunker(
        processed_data_path="dummy_path", output_path="dummy_output", max_words=250
    )
    note = {
        "note_id": "test Note.md",
        "title": "Test Note",
        "relative_path": "test_note.md",
    }
    text = "This is a test chunk."
    chunk = chunker._make_chunk(note, text, heading="Test Heading", chunk_index=0)
    assert chunk["chunk_id"] == "test Note.md::test_heading::chunk_0"
    assert chunk["note_id"] == "test Note.md"
    assert chunk["title"] == "Test Note"
    assert chunk["relative_path"] == "test_note.md"
    assert chunk["heading"] == "Test Heading"
    assert chunk["chunk_index"] == 0
    assert chunk["text"] == "This is a test chunk."
    assert chunk["word_count"] == 5
    assert chunk["tags"] == []
    assert chunk["frontmatter"] == {}


@pytest.mark.unittest
@pytest.mark.runonci
def test_create_chunks(dummy_processed_data_path: Path):
    """
    Test creating chunks from processed data.

    Args:
        dummy_processed_data_path (Path): Path to the dummy processed data file.
    """
    chunker = StructuralChunker(
        processed_data_path=str(dummy_processed_data_path),
        output_path=str(dummy_processed_data_path.parent / "chunked_data.json"),
        max_words=100,
    )
    processed_data = chunker.read_processed_data()
    assert processed_data is not None
    chunked_data = chunker.create_chunks(processed_data)
    assert len(chunked_data) > 0
    # Check that chunks are created correctly based on max_words
    for chunk in chunked_data:
        assert chunk["word_count"] <= chunker.max_words
        if (
            chunk["chunk_id"]
            == "_learning about me/what I learnt about myself when dealing with ADHD.md::root::chunk_0"
        ):
            assert chunk["chunk_index"] == 0
            assert (
                chunk["text"]
                == "- aim to do less, end up doing more - breakdown tasks into initial granular nested problems - work in iterations. Get 80% value from 20% of things, Pareto's principle - do long things, delay instant gratification. Avoid seeking novelty. Finish reading one book, watch one big video, play one game. - morning and night routines - just open things up, set things up, write in notepad ++ then take a break. Dont have to start immediately - do a little everyday in a robust consistent manner. Dont have to do it all in one day, in this one session."
            )
            assert chunk["heading"] is None
            assert chunk["title"] == "what I learnt about myself when dealing with ADHD"
            assert (
                chunk["relative_path"]
                == "_learning about me/what I learnt about myself when dealing with ADHD.md"
            )
            assert chunk["tags"] == []
            assert chunk["frontmatter"] == {}
            assert chunk["word_count"] == 100
        elif (
            chunk["chunk_id"]
            == "_Meditations/Games and Life.md::roguelikes_and_life::chunk_0"
        ):
            assert chunk["chunk_index"] == 0
            assert chunk["title"] == "Games and Life"
            assert chunk["relative_path"] == "_Meditations/Games and Life.md"
            assert chunk["tags"] == []
            assert chunk["frontmatter"] == {}
            assert chunk["heading"] == "Roguelikes and Life"


@pytest.mark.unittest
@pytest.mark.runonci
def test_save_chunked_data(tmp_path: Path):
    """
    Test saving chunked data to a JSON file.

    Args:
        tmp_path (Path): Temporary directory provided by pytest.
    """
    chunker = StructuralChunker(
        processed_data_path="dummy_path",
        output_path=str(tmp_path / "chunked_data.json"),
        max_words=250,
    )
    chunked_data = [
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
        }
    ]
    chunker.save_chunked_data(chunked_data)
    output_file = tmp_path / "chunked_data.json"
    assert output_file.exists()
    with output_file.open("r", encoding="utf-8") as f:
        saved_data = json.load(f)
    assert saved_data == chunked_data


@pytest.mark.unittest
@pytest.mark.runonci
def test_chunk(tmp_path: Path, dummy_processed_data_path: Path):
    """
    Test the main chunking process of the chunker module.

    Args:
        tmp_path (Path): Temporary directory provided by pytest.
        dummy_processed_data_path (Path): Path to the dummy processed data file.
    """
    chunker = StructuralChunker(
        processed_data_path=str(dummy_processed_data_path),
        output_path=str(tmp_path / "chunked_data.json"),
        max_words=250,
    )
    chunker.chunk()
    output_file = tmp_path / "chunked_data.json"
    assert output_file.exists()
    with output_file.open("r", encoding="utf-8") as f:
        saved_data = json.load(f)
    assert (
        saved_data[0]["note_id"]
        == "_learning about me/what I learnt about myself when dealing with ADHD.md"
    )
