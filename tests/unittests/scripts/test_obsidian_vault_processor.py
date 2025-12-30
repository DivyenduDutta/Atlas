# mypy: disable-error-code=arg-type
import pytest
import json
from pathlib import Path

from atlas.core.ingester.obsidian_vault_processor import ObsidianVaultProcessor


@pytest.fixture
def dummy_obsidian_vault_path(tmp_path: Path) -> Path:
    """
    Create a dummy obsidian vault structure for testing.

    Args:
        tmp_path (Path): Temporary path provided by pytest.

    Returns:
        Path: The path to the created dummy obsidian vault.
    """
    obsidian_vault_dir = tmp_path / "Test_Obsidian_Vault"
    obsidian_vault_dir.mkdir(parents=True)

    # Create the .obsidian directory
    obsidian_dir = obsidian_vault_dir / ".obsidian"
    obsidian_dir.mkdir()

    # Create one of the required config files
    config_file = obsidian_dir / "app.json"
    config_file.write_text('{"setting": "value"}')
    config_file = obsidian_dir / "appearance.json"
    config_file.write_text('{"theme": "dark"}')
    config_file = obsidian_dir / "workspace.json"
    config_file.write_text('{"layout": "default"}')

    obsidian_subdir = obsidian_vault_dir / "_learning about me"
    obsidian_subdir.mkdir()
    note_file = obsidian_subdir / "what I learnt about myself when dealing with ADHD.md"
    note_file.write_text(
        "---\n"
        "tags: [personal, health]\n"
        "date: 2023-10-01\n"
        "---\n"
        "# What I learnt about #myself when dealing [[wikilink|custom name]] with ADHD\n\nSome #content here.\n"
    )

    return obsidian_vault_dir


@pytest.fixture
def dummy_non_obsidian_vault_path(tmp_path: Path) -> Path:
    """
    Create a dummy non-obsidian vault structure for testing.
    Does not contain the .obsidian directory.

    Args:
        tmp_path (Path): Temporary path provided by pytest.

    Returns:
        Path: The path to the created dummy obsidian vault.
    """
    non_obsidian_vault_dir = tmp_path / "Test_Obsidian_Vault"
    non_obsidian_vault_dir.mkdir(parents=True)

    obsidian_subdir = non_obsidian_vault_dir / "_learning about me"
    obsidian_subdir.mkdir()
    note_file = obsidian_subdir / "what I learnt about myself when dealing with ADHD.md"
    note_file.write_text(
        "# What I learnt about myself when dealing with ADHD\n\nSome content here."
    )

    return non_obsidian_vault_dir


@pytest.fixture
def dummy_another_non_obsidian_vault_path(tmp_path: Path) -> Path:
    """
    Create a dummy non-obsidian vault structure for testing.
    Contains the .obsidian directory but missing required config files.

    Args:
        tmp_path (Path): Temporary path provided by pytest.

    Returns:
        Path: The path to the created dummy obsidian vault.
    """
    non_obsidian_vault_dir = tmp_path / "Test_Obsidian_Vault"
    non_obsidian_vault_dir.mkdir(parents=True)

    # Create the .obsidian directory
    obsidian_dir = non_obsidian_vault_dir / ".obsidian"
    obsidian_dir.mkdir()

    obsidian_subdir = non_obsidian_vault_dir / "_learning about me"
    obsidian_subdir.mkdir()
    note_file = obsidian_subdir / "what I learnt about myself when dealing with ADHD.md"
    note_file.write_text(
        "# What I learnt about myself when dealing with ADHD\n\nSome content here."
    )

    return non_obsidian_vault_dir


@pytest.fixture
def dummy_obsidian_vault_path_with_basic_note(tmp_path: Path) -> Path:
    """
    Create a dummy non-obsidian vault structure for testing.
    Contains a basic note without frontmatter, tags, headings or wikilinks.
    Contains the .obsidian directory but missing required config files.

    Args:
        tmp_path (Path): Temporary path provided by pytest.

    Returns:
        Path: The path to the created dummy obsidian vault.
    """
    non_obsidian_vault_dir = tmp_path / "Test_Obsidian_Vault"
    non_obsidian_vault_dir.mkdir(parents=True)

    # Create the .obsidian directory
    obsidian_dir = non_obsidian_vault_dir / ".obsidian"
    obsidian_dir.mkdir()

    obsidian_subdir = non_obsidian_vault_dir / "_learning about me"
    obsidian_subdir.mkdir()
    note_file = obsidian_subdir / "what I learnt about myself when dealing with ADHD.md"
    note_file.write_text(
        "What I learnt about myself when dealing with ADHD\n\nSome content here."
    )

    return non_obsidian_vault_dir


@pytest.fixture
def dummy_output_path(tmp_path: Path) -> Path:
    """
    Create a dummy output path for testing.

    Args:
        tmp_path (Path): Temporary path provided by pytest.

    Returns:
        Path: The path to the created dummy output directory.
    """
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True)
    return output_dir


@pytest.mark.unittest
@pytest.mark.runonci
def test_find_vault_root_positive(
    dummy_obsidian_vault_path: Path, dummy_output_path: Path
) -> None:
    """
    Test if the vault root is correctly identified when it exists.

    Args:
        dummy_obsidian_vault_path (Path): The path to the dummy obsidian vault.
        dummy_output_path (Path): The path to the dummy output directory.
    """
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=dummy_obsidian_vault_path, output_path=dummy_output_path
    )
    vault_root = obsidian_vault_processor._find_vault_root()
    assert (
        vault_root == dummy_obsidian_vault_path
    ), "Vault root should be correctly identified."


@pytest.mark.unittest
@pytest.mark.runonci
def test_find_vault_root_positive_file(
    dummy_obsidian_vault_path: Path, dummy_output_path: Path
) -> None:
    """
    Test if the vault root is correctly identified when starting from a file path within the vault.

    Args:
        dummy_obsidian_vault_path (Path): The path to the dummy obsidian vault.
        dummy_output_path (Path): The path to the dummy output directory.
    """
    file_path = (
        dummy_obsidian_vault_path
        / "_learning about me"
        / "what I learnt about myself when dealing with ADHD.md"
    )
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=file_path, output_path=dummy_output_path
    )
    vault_root = obsidian_vault_processor._find_vault_root()
    assert (
        vault_root == dummy_obsidian_vault_path
    ), "Vault root should be correctly identified."


@pytest.mark.unittest
@pytest.mark.runonci
def test_find_vault_root_negative_missing_obsidian_folder(
    dummy_non_obsidian_vault_path: Path, dummy_output_path: Path
) -> None:
    """
    Test if the vault root is correctly identified when it does not exist.
    .obsidian folder is missing.

    Args:
        dummy_non_obsidian_vault_path (Path): The path to the dummy non-obsidian vault.
        dummy_output_path (Path): The path to the dummy output directory.
    """
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=dummy_non_obsidian_vault_path, output_path=dummy_output_path
    )
    vault_root = obsidian_vault_processor._find_vault_root()
    assert vault_root == None, "Should return None when no vault root is found."


@pytest.mark.unittest
@pytest.mark.runonci
def test_has_obsidian_config_positive(
    dummy_obsidian_vault_path: Path, dummy_output_path: Path
) -> None:
    """
    Test if the config files are detected when they are present.

    Args:
        dummy_obsidian_vault_path (Path): The path to the dummy obsidian vault.
        dummy_output_path (Path): The path to the dummy output directory.
    """
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=dummy_obsidian_vault_path, output_path=dummy_output_path
    )
    has_config = obsidian_vault_processor._has_obsidian_config()
    assert has_config == True, "Should return True when config files are found."


@pytest.mark.unittest
@pytest.mark.runonci
def test_has_obsidian_config_negative_missing_config_files(
    dummy_another_non_obsidian_vault_path: Path,
    dummy_output_path: Path,
) -> None:
    """
    Test if the config files are detected when they are missing.
    .obsidian folder exists but missing required config files.

    Args:
        dummy_another_non_obsidian_vault_path (Path): The path to the dummy non-obsidian vault.
        dummy_output_path (Path): The path to the dummy output directory.
    """
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=dummy_another_non_obsidian_vault_path, output_path=dummy_output_path
    )
    has_config = obsidian_vault_processor._has_obsidian_config()
    assert has_config == False, "Should return False when no config files are found."


@pytest.mark.unittest
@pytest.mark.runonci
def test_precheck_positive(
    dummy_obsidian_vault_path: Path, dummy_output_path: Path
) -> None:
    """
    Test if precheck passes for a valid Obsidian vault.

    Args:
        dummy_obsidian_vault_path (Path): The path to the dummy obsidian vault.
        dummy_output_path (Path): The path to the dummy output directory.
    """
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=dummy_obsidian_vault_path, output_path=dummy_output_path
    )
    is_valid = obsidian_vault_processor.precheck()
    assert is_valid == True, "Precheck should return True for a valid Obsidian vault."


@pytest.mark.unittest
@pytest.mark.runonci
def test_precheck_negative_missing_obsidian_folder(
    dummy_non_obsidian_vault_path: Path, dummy_output_path: Path
) -> None:
    """
    Test if precheck fails when .obsidian folder is missing.

    Args:
        dummy_non_obsidian_vault_path (Path): The path to the dummy non-obsidian vault.
        dummy_output_path (Path): The path to the dummy output directory.
    """
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=dummy_non_obsidian_vault_path, output_path=dummy_output_path
    )
    is_valid = obsidian_vault_processor.precheck()
    assert (
        is_valid == False
    ), "Precheck should return False when .obsidian folder is missing."


@pytest.mark.unittest
@pytest.mark.runonci
def test_precheck_negative_missing_config_files(
    dummy_another_non_obsidian_vault_path: Path, dummy_output_path: Path
) -> None:
    """
    Test if precheck fails when required config files are missing.

    Args:
        dummy_another_non_obsidian_vault_path (Path): The path to the dummy non-obsidian vault.
        dummy_output_path (Path): The path to the dummy output directory.
    """
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=dummy_another_non_obsidian_vault_path, output_path=dummy_output_path
    )
    is_valid = obsidian_vault_processor.precheck()
    assert (
        is_valid == False
    ), "Precheck should return False when required config files are missing."


@pytest.mark.unittest
@pytest.mark.runonci
def test_extract_frontmatter_positive(
    dummy_obsidian_vault_path: Path, dummy_output_path: Path
) -> None:
    """
    Test if frontmatter is correctly extracted from a markdown file with frontmatter.

    Args:
        dummy_obsidian_vault_path (Path): The path to the dummy obsidian vault.
        dummy_output_path (Path): The path to the dummy output directory.
    """
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=dummy_obsidian_vault_path, output_path=dummy_output_path
    )
    note_file = (
        dummy_obsidian_vault_path
        / "_learning about me"
        / "what I learnt about myself when dealing with ADHD.md"
    )
    text = note_file.read_text()
    frontmatter, body = obsidian_vault_processor._extract_frontmatter(text)
    assert frontmatter == {
        "tags": ["personal", "health"],
        "date": "2023-10-01",
    }, "Frontmatter should be correctly extracted."
    assert body.startswith(
        "# What I learnt about"
    ), "Body should be correctly extracted."


@pytest.mark.unittest
@pytest.mark.runonci
def test_extract_frontmatter_negative_no_frontmatter(
    dummy_obsidian_vault_path_with_basic_note: Path, dummy_output_path: Path
) -> None:
    """
    Test if frontmatter extraction handles markdown file without frontmatter.

    Args:
        dummy_obsidian_vault_path_with_basic_note (Path): The path to the dummy obsidian vault with basic note.
        dummy_output_path (Path): The path to the dummy output directory.
    """
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=dummy_obsidian_vault_path_with_basic_note,
        output_path=dummy_output_path,
    )
    note_file = (
        dummy_obsidian_vault_path_with_basic_note
        / "_learning about me"
        / "what I learnt about myself when dealing with ADHD.md"
    )
    text = note_file.read_text()
    frontmatter, body = obsidian_vault_processor._extract_frontmatter(text)
    assert (
        frontmatter == {}
    ), "Frontmatter should be empty for file without frontmatter."
    assert body.startswith("What I learnt about"), "Body should be correctly extracted."


@pytest.mark.unittest
@pytest.mark.runonci
def test_extract_headings_positive(
    dummy_obsidian_vault_path: Path, dummy_output_path: Path
) -> None:
    """
    Test if headings are correctly extracted from a markdown file.

    Args:
        dummy_obsidian_vault_path (Path): The path to the dummy obsidian vault.
        dummy_output_path (Path): The path to the dummy output directory.
    """
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=dummy_obsidian_vault_path, output_path=dummy_output_path
    )
    note_file = (
        dummy_obsidian_vault_path
        / "_learning about me"
        / "what I learnt about myself when dealing with ADHD.md"
    )
    text = note_file.read_text()
    _, body = obsidian_vault_processor._extract_frontmatter(text)
    headings = obsidian_vault_processor._extract_headings(body)
    assert headings == [
        {
            "level": 1,
            "title": "What I learnt about #myself when dealing [[wikilink|custom name]] with ADHD",
        }
    ], "Headings should be correctly extracted."


@pytest.mark.unittest
@pytest.mark.runonci
def test_extract_headings_negative_no_headings(
    dummy_obsidian_vault_path_with_basic_note: Path, dummy_output_path: Path
) -> None:
    """
    Test if heading extraction handles markdown file without headings.

    Args:
        dummy_obsidian_vault_path_with_basic_note (Path): The path to the dummy obsidian vault with basic note.
        dummy_output_path (Path): The path to the dummy output directory.
    """
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=dummy_obsidian_vault_path_with_basic_note,
        output_path=dummy_output_path,
    )
    note_file = (
        dummy_obsidian_vault_path_with_basic_note
        / "_learning about me"
        / "what I learnt about myself when dealing with ADHD.md"
    )
    text = note_file.read_text()
    _, body = obsidian_vault_processor._extract_frontmatter(text)
    headings = obsidian_vault_processor._extract_headings(body)
    assert headings == [], "Headings should be empty for file without headings."


@pytest.mark.unittest
@pytest.mark.runonci
def test_extract_tags_positive(
    dummy_obsidian_vault_path: Path, dummy_output_path: Path
) -> None:
    """
    Test if tags are correctly extracted from a markdown file.

    Args:
        dummy_obsidian_vault_path (Path): The path to the dummy obsidian vault.
        dummy_output_path (Path): The path to the dummy output directory.
    """
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=dummy_obsidian_vault_path, output_path=dummy_output_path
    )
    note_file = (
        dummy_obsidian_vault_path
        / "_learning about me"
        / "what I learnt about myself when dealing with ADHD.md"
    )
    text = note_file.read_text()
    _, body = obsidian_vault_processor._extract_frontmatter(text)
    tags = obsidian_vault_processor._extract_tags(body)
    assert tags == ["content", "myself"], "Tags should be correctly extracted."


@pytest.mark.unittest
@pytest.mark.runonci
def test_extract_tags_negative_no_tags(
    dummy_obsidian_vault_path_with_basic_note: Path, dummy_output_path: Path
) -> None:
    """
    Test if tag extraction handles markdown file without tags.

    Args:
        dummy_obsidian_vault_path_with_basic_note (Path): The path to the dummy obsidian vault with basic note.
        dummy_output_path (Path): The path to the dummy output directory.
    """
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=dummy_obsidian_vault_path_with_basic_note,
        output_path=dummy_output_path,
    )
    note_file = (
        dummy_obsidian_vault_path_with_basic_note
        / "_learning about me"
        / "what I learnt about myself when dealing with ADHD.md"
    )
    text = note_file.read_text()
    _, body = obsidian_vault_processor._extract_frontmatter(text)
    tags = obsidian_vault_processor._extract_tags(body)
    assert tags == [], "Tags should be empty for file without tags."


@pytest.mark.unittest
@pytest.mark.runonci
def test_extract_wikilinks_positive(
    dummy_obsidian_vault_path: Path, dummy_output_path: Path
) -> None:
    """
    Test if wikilinks are correctly extracted from a markdown file.

    Args:
        dummy_obsidian_vault_path (Path): The path to the dummy obsidian vault.
        dummy_output_path (Path): The path to the dummy output directory.
    """
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=dummy_obsidian_vault_path, output_path=dummy_output_path
    )
    note_file = (
        dummy_obsidian_vault_path
        / "_learning about me"
        / "what I learnt about myself when dealing with ADHD.md"
    )
    text = note_file.read_text()
    _, body = obsidian_vault_processor._extract_frontmatter(text)
    wikilinks = obsidian_vault_processor._extract_wikilinks(body)
    assert wikilinks == [
        "wikilink|custom name"
    ], "Wikilinks should be correctly extracted."


@pytest.mark.unittest
@pytest.mark.runonci
def test_extract_wikilinks_negative_no_wikilinks(
    dummy_obsidian_vault_path_with_basic_note: Path, dummy_output_path: Path
) -> None:
    """
    Test if wikilink extraction handles markdown file without wikilinks.

    Args:
        dummy_obsidian_vault_path_with_basic_note (Path): The path to the dummy obsidian vault with basic note.
        dummy_output_path (Path): The path to the dummy output directory.
    """
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=dummy_obsidian_vault_path_with_basic_note,
        output_path=dummy_output_path,
    )
    note_file = (
        dummy_obsidian_vault_path_with_basic_note
        / "_learning about me"
        / "what I learnt about myself when dealing with ADHD.md"
    )
    text = note_file.read_text()
    _, body = obsidian_vault_processor._extract_frontmatter(text)
    wikilinks = obsidian_vault_processor._extract_wikilinks(body)
    assert wikilinks == [], "Wikilinks should be empty for file without wikilinks."


@pytest.mark.unittest
@pytest.mark.runonci
def test_parse_markdown_note(
    dummy_obsidian_vault_path: Path, dummy_output_path: Path
) -> None:
    """
    Test if a markdown note is correctly parsed into metadata.

    Args:
        dummy_obsidian_vault_path (Path): The path to the dummy obsidian vault.
        dummy_output_path (Path): The path to the dummy output directory.
    """
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=dummy_obsidian_vault_path, output_path=dummy_output_path
    )
    note_file = (
        dummy_obsidian_vault_path
        / "_learning about me"
        / "what I learnt about myself when dealing with ADHD.md"
    )
    note_data = obsidian_vault_processor._parse_markdown_note(
        note_file, dummy_obsidian_vault_path
    )
    expected_data = {
        "note_id": "_learning about me/what I learnt about myself when dealing with ADHD.md",
        "title": "what I learnt about myself when dealing with ADHD",
        "relative_path": "_learning about me/what I learnt about myself when dealing with ADHD.md",
        "raw_text": "# What I learnt about #myself when dealing [[wikilink|custom name]] with ADHD\n\nSome #content here.\n",
        "frontmatter": {"tags": ["personal", "health"], "date": "2023-10-01"},
        "headings": [
            {
                "level": 1,
                "title": "What I learnt about #myself when dealing [[wikilink|custom name]] with ADHD",
            }
        ],
        "tags": ["content", "myself"],
        "wikilinks": ["wikilink|custom name"],
        "word_count": 15,
    }
    assert (
        note_data == expected_data
    ), "Markdown note should be correctly parsed into metadata."


@pytest.mark.unittest
@pytest.mark.runonci
def test_save_processed_data(
    dummy_obsidian_vault_path: Path,
    dummy_output_path: Path,
) -> None:
    """
    Test if processed data is correctly saved to a JSON file.

    Args:
        dummy_obsidian_vault_path (Path): The path to the dummy obsidian vault.
        dummy_output_path (Path): The path to the dummy output directory.
    """
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=dummy_obsidian_vault_path,
        output_path=dummy_output_path / "obsidian_index.json",
    )
    processed_data = [
        {
            "note_id": "note1.md",
            "title": "Note 1",
            "relative_path": "note1.md",
            "raw_text": "Content of note 1.",
            "frontmatter": {},
            "headings": [],
            "tags": [],
            "wikilinks": [],
            "word_count": 4,
        },
        {
            "note_id": "note2.md",
            "title": "Note 2",
            "relative_path": "note2.md",
            "raw_text": "Content of note 2.",
            "frontmatter": {},
            "headings": [],
            "tags": [],
            "wikilinks": [],
            "word_count": 4,
        },
    ]
    obsidian_vault_processor.save_processed_data(processed_data)

    output_file = dummy_output_path / "obsidian_index.json"
    assert output_file.exists(), "Output JSON file should be created."

    with output_file.open("r", encoding="utf-8") as f:
        saved_data = json.load(f)
    assert saved_data == processed_data, "Saved data should match the processed data."


@pytest.mark.unittest
@pytest.mark.runonci
def test_process(dummy_obsidian_vault_path: Path, dummy_output_path: Path) -> None:
    """
    Test if the Obsidian vault is correctly processed to extract notes metadata.

    Args:
        dummy_obsidian_vault_path (Path): The path to the dummy obsidian vault.
        dummy_output_path (Path): The path to the dummy output directory.
    """
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=dummy_obsidian_vault_path,
        output_path=dummy_output_path / "obsidian_index.json",
    )
    processed_data = obsidian_vault_processor.process()
    assert len(processed_data) == 1, "There should be one note processed."

    note_data = processed_data[0]
    assert (
        note_data["note_id"]
        == "_learning about me/what I learnt about myself when dealing with ADHD.md"
    ), "Note ID should be correct."
    assert (
        note_data["title"] == "what I learnt about myself when dealing with ADHD"
    ), "Note title should be correct."
