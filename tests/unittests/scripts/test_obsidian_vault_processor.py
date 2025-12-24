import pytest

from atlas.core.ingest.obsidian_vault_processor import ObsidianVaultProcessor


@pytest.fixture
def dummy_obsidian_vault_path(tmp_path):
    """
    Create a dummy obsidian vault structure for testing.
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
        "# What I learnt about myself when dealing with ADHD\n\nSome content here."
    )

    # TODO: Add more files and directories as needed for testing

    return obsidian_vault_dir


@pytest.fixture
def dummy_non_obsidian_vault_path(tmp_path):
    """
    Create a dummy non-obsidian vault structure for testing.
    Does not contain the .obsidian directory.
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
def dummy_another_non_obsidian_vault_path(tmp_path):
    """
    Create a dummy non-obsidian vault structure for testing.
    Contains the .obsidian directory but missing required config files.
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


@pytest.mark.unittest
@pytest.mark.runonci
def test_find_vault_root_positive(dummy_obsidian_vault_path) -> None:
    """
    Test if the vault root is correctly identified when it exists.
    """
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=dummy_obsidian_vault_path
    )
    vault_root = obsidian_vault_processor._find_vault_root()
    assert (
        vault_root == dummy_obsidian_vault_path
    ), "Vault root should be correctly identified."


@pytest.mark.unittest
@pytest.mark.runonci
def test_find_vault_root_positive_file(dummy_obsidian_vault_path) -> None:
    """
    Test if the vault root is correctly identified when starting from a file path within the vault.
    """
    file_path = (
        dummy_obsidian_vault_path
        / "_learning about me"
        / "what I learnt about myself when dealing with ADHD.md"
    )
    obsidian_vault_processor = ObsidianVaultProcessor(vault_path=file_path)
    vault_root = obsidian_vault_processor._find_vault_root()
    assert (
        vault_root == dummy_obsidian_vault_path
    ), "Vault root should be correctly identified."


@pytest.mark.unittest
@pytest.mark.runonci
def test_find_vault_root_negative_missing_obsidian_folder(
    dummy_non_obsidian_vault_path,
) -> None:
    """
    Test if the vault root is correctly identified when it does not exist.
    .obsidian folder is missing.
    """
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=dummy_non_obsidian_vault_path
    )
    vault_root = obsidian_vault_processor._find_vault_root()
    assert vault_root == None, "Should return None when no vault root is found."


@pytest.mark.unittest
@pytest.mark.runonci
def test_has_obsidian_config_positive(dummy_obsidian_vault_path) -> None:
    """
    Test if the config files are detected when they are present.
    """
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=dummy_obsidian_vault_path
    )
    has_config = obsidian_vault_processor._has_obsidian_config()
    assert has_config == True, "Should return True when config files are found."


@pytest.mark.unittest
@pytest.mark.runonci
def test_has_obsidian_config_negative_missing_config_files(
    dummy_another_non_obsidian_vault_path,
) -> None:
    """
    Test if the config files are detected when they are missing.
    .obsidian folder exists but missing required config files.
    """
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=dummy_another_non_obsidian_vault_path
    )
    has_config = obsidian_vault_processor._has_obsidian_config()
    assert has_config == False, "Should return False when no config files are found."


@pytest.mark.unittest
@pytest.mark.runonci
def test_precheck_positive(dummy_obsidian_vault_path) -> None:
    """
    Test if precheck passes for a valid Obsidian vault.
    """
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=dummy_obsidian_vault_path
    )
    is_valid = obsidian_vault_processor.precheck()
    assert is_valid == True, "Precheck should return True for a valid Obsidian vault."


@pytest.mark.unittest
@pytest.mark.runonci
def test_precheck_negative_missing_obsidian_folder(
    dummy_non_obsidian_vault_path,
) -> None:
    """
    Test if precheck fails when .obsidian folder is missing.
    """
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=dummy_non_obsidian_vault_path
    )
    is_valid = obsidian_vault_processor.precheck()
    assert (
        is_valid == False
    ), "Precheck should return False when .obsidian folder is missing."


@pytest.mark.unittest
@pytest.mark.runonci
def test_precheck_negative_missing_config_files(
    dummy_another_non_obsidian_vault_path,
) -> None:
    """
    Test if precheck fails when required config files are missing.
    """
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=dummy_another_non_obsidian_vault_path
    )
    is_valid = obsidian_vault_processor.precheck()
    assert (
        is_valid == False
    ), "Precheck should return False when required config files are missing."
