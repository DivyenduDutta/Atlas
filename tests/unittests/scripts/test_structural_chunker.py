import pytest
import json
from pathlib import Path

from atlas.core.chunker.structural_chunker import StructuralChunker


@pytest.fixture
def dummy_processed_data_path(tmp_path: Path) -> Path:
    """
    Create a dummy processed data file for testing.

    Args:
        tmp_path (Path): Temporary directory provided by pytest.

    Returns:
        Path: The path to the created dummy processed data file.
    """
    dummy_data = [
        {
            "note_id": "_learning about me/what I learnt about myself when dealing with ADHD.md",
            "title": "what I learnt about myself when dealing with ADHD",
            "relative_path": "_learning about me/what I learnt about myself when dealing with ADHD.md",
            "raw_text": "\n- aim to do less, end up doing more\n- breakdown tasks into initial granular nested problems\n- work in iterations. Get 80% value from 20% of things, Pareto's principle\n- do long things, delay instant gratification. Avoid seeking novelty. Finish reading one book, watch one big video, play one game.\n- morning and night routines\n- just open things up, set things up, write in notepad ++ then take a break. Dont have to start immediately\n- do a little everyday in a robust consistent manner. Dont have to do it all in one day, in this one session. Takes time. Be patient but consistent\n- systems thinker - seeing the whole picture and its parts as early as possible - related to working in iterations",
            "frontmatter": {},
            "headings": [],
            "tags": [],
            "wikilinks": [],
            "word_count": 127,
        },
        {
            "note_id": "_Meditations/Games and Life.md",
            "title": "Games and Life",
            "relative_path": "_Meditations/Games and Life.md",
            "raw_text": "\n### Roguelikes and Life\n- **Learning** more about the thing that's causing us _problems/scaring us/making us uncomfortable_ will help us deal with the problem better\n- For example, in Darkest Dungeon, stress is a huge problem for me but as I learn more about it, the fear changes into enthusiasm because I understand things better\n\t- So we try to apply the same in life as well\n---\n- Frame _questions_ regarding the problems Im currently facing\n\t- and _answer_ them\n\t\t- if you dont know the answer, search online or ask someone\n---\n- Learn from mistakes in life\n\t- For ex, we didnt know about traps in DD (Darkest Dungeon) and took deadly stress damage\n\t\t- but thats fine as long as we used that opportunity to learn about traps and how to avoid in future\n- Use experiences/problems/obstacles to acquire information\n\t- For ex, every run is an experience and helps us learn more\n- Write these things down\n---\n### Plateup and life\n- If something makes you uncomfortable (because you don't understand it or are not good at it)\n\t- and if that thing is good for you, its result benefits you\n\t\t- then embrace it and do more of that thing\n- This is the only way to get used to that uncomfortable feeling and learn more about it\n\t- and eventually it becomes less uncomfortable\n- For ex, in Plateup, we see a recipe we didn't understand before and we chose it so that we could embrace it and understand it\n\t- the game ended because I didn't know it but I was able to learn from it and next time I did better\n---\n- the real reason why the tasks of life evoke fear and anxiety is because I give utmost importance to just the outcome/result of the task\n\t- I need to focus on the doing part, the journey. To take control of my fate, to be in control\n\t- focusing on what I CAN DO, leads to excitement\n\t\t- it becomes opportunities to solve problems/ challenges/ obstacles\n\t\t\t- solving them leads to contentment and fulfillment and happiness\n---\n\n### Skyrim/Valorant and Life obstacles\n- When I was challenged to a fist fight by Uthgerd The Unbroken, it was not an easy fight considering her armour is much better than mine, the combat in the game is bad and its a fist fight (no weapon, magic or healing)\n- I lost multiple times and yet I didnt give up, I kept going back to it and wanted to beat her/ overcome the obstacle\n- similarly in life, similar problems will keep arising and the point is to not give up after the first failure but to learn from it and keep trying to overcome the obstacle\n- for ex, when applying for jobs, we fail an interview, instead of giving up we learn from it and keep trying to pass the interviews\n- the same thing happens in valorant too, where I keep trying to get better at aiming and getting headshots even though I have bad ping and am at a disadvantage\n\t- I drop off sometimes but always come back in order to try to best the obstacle and eventually I keep improving\n\n---\n\n### Spelunky\n- the game is a corollary for life. Sometimes things dont go our way like the shopkeeper is enraged due to something we didn't do, the key and chest and in locations unreachable without prior knowledge, its a dark level and rushing water and black market entrance level so we miss the black market. But thats fine. I dont give up the run immediately but rather take it as a challenge to see how far can I go with this hand I've been dealt.\n- The main reason I give up is because I think \"since I dont have the conditions I think I needed to succeed, there's no point pursuing things further. Whats the point of trying if I know I cant succeed\". Many problems with this way of thinking. \n\t- First, I make up the conditions to succeed. I dont know for sure if those are actually the conditions to succeed\n\t- Second, I dont know for sure that if those conditions to succeed arent available then I wont be able succeed for sure. It might be harder to succeed maybe but not impossible. Its impossible if I give up.\n\t\t- subpoint - even if I have all the conditions to succeed available, I might not be able to succeed. Eg, I have a jetpack and a shotgun and good amount of health, I die and the run ends\n\t- Third, if I try to succeed ie, work with what I have, there's always a chance to succeed. The chance may be low but its not 0. And even 1% is more than 0%. (this is related to the previous point)\n\t\t- eg, I lost 1 hp due to some pointless mistake. I immediately thought of abandoning the run. I remember all this that I've written here and kept progressing and found a jetpack and compass in the market in the next level. \n\t- Fourth, the point isnt always about succeeding but even failing is fine because I can learn from it and try again and try again and again and again. As long as I'm learning its good. And failure isnt the end of it all. Life goes on and opportunities come again. Learning from failure and improving makes me capable of being able to capitalize on those opportunities better.\n- I do think this mental distortion might have something to do with my ADHD. If things dont go properly/successfully (properly/successfully as defined by me or society) right from the very beginning ie, each small step needs to be perfect and successful, then I give up. I think its my ADHD kicking in which wants rewards in the short term ie, each small step going properly rather than considering things in the long term.\n- `important` - I beat spelunky finally. And prior to beating it today, I had a run where I did everything perfectly but some random explosion killed me. Another one - The shopkeeper got angered due to a snail spawning in the shop in the black market and I made no mistake in that run. Another one - There was a bug and I got stuck exiting and got killed by a tiki trap. But I didnt give up. I immediately did a <span style=\"color:lightgreen\">quick restart</span>. So why can I keep restarting and not give up in games but not do so in real life? All the times I got screwed in Spelunky where it wasnt my mistake has happened and will happen in life as well. I could do everything perfectly, be very good, follow all the rules and life will fuck me over. Life is procedurally generated just like Spelunky. But I do a quick restart and immediately try again because if I do so then eventually I will win the game just like how I eventually beat spelunky. ^f7912e\n- Life is hard just like Spelunky. Then does that mean I cant beat it? Nope, I learn and keep trying and keep getting better and eventually everything will align properly for me. Luck will be on my side and I will win at life.\n---\n\n",
            "frontmatter": {},
            "headings": [
                {"level": 3, "title": "Roguelikes and Life"},
                {"level": 3, "title": "Plateup and life"},
                {"level": 3, "title": "Skyrim/Valorant and Life obstacles"},
                {"level": 3, "title": "Spelunky"},
            ],
            "tags": [],
            "wikilinks": [],
            "word_count": 1233,
        },
    ]
    processed_data_path = tmp_path / "obsidian_index.json"
    with processed_data_path.open("w", encoding="utf-8") as f:
        json.dump(dummy_data, f, indent=2, ensure_ascii=False)
    return processed_data_path


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
