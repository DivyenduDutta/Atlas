import pytest
import yaml
from pathlib import Path

from atlas.core.embedder.config import load_encoder_config, EncoderConfig


@pytest.mark.unittest
@pytest.mark.runonci
def test_load_encoder_config_positive(tmp_path: Path):
    """
    Test loading the encoder configuration file when file is available and not empty.

    Args:
        tmp_path (Path): Temporary directory provided by pytest.
    """

    # Create a temporary YAML config file
    config_data = {
        "model_name": "all-MiniLM-L6-v2",
        "batch_size": 32,
        "normalize_embeddings": True,
        "device": "cuda",
    }
    config_path = tmp_path / "encoder_config.yaml"
    with config_path.open("w", encoding="utf-8") as f:
        yaml.dump(config_data, f)

    # Load the configuration
    loaded_config = load_encoder_config(config_path)

    # Assert that the loaded configuration matches the original data
    assert isinstance(loaded_config, EncoderConfig)
    assert loaded_config.model_name == config_data["model_name"]
    assert loaded_config.batch_size == config_data["batch_size"]
    assert loaded_config.normalize_embeddings == config_data["normalize_embeddings"]
    assert loaded_config.device == config_data["device"]


@pytest.mark.unittest
@pytest.mark.runonci
def test_load_encoder_config_negative_empty_file(tmp_path):
    """
    Test loading the encoder configuration file when file is empty.

    Args:
        tmp_path (Path): Temporary directory provided by pytest.
    """
    # Create an empty temporary YAML config file
    config_path = tmp_path / "empty_encoder_config.yaml"
    with config_path.open("w", encoding="utf-8") as f:
        f.write("")

    # Attempt to load the configuration and expect a ValueError
    with pytest.raises(ValueError) as exc_info:
        load_encoder_config(config_path)

    assert "Encoder configuration file is empty" in str(exc_info.value)


@pytest.mark.unittest
@pytest.mark.runonci
def test_load_encoder_config_negative_file_not_found(tmp_path):
    """
    Test loading the encoder configuration file when file is not found.

    Args:
        tmp_path (Path): Temporary directory provided by pytest.
    """
    config_path = tmp_path / "incorrect_config_file.yaml"

    # Attempt to load the configuration and expect a FileNotFoundError
    with pytest.raises(FileNotFoundError) as exc_info:
        load_encoder_config(config_path)

    assert "Encoder configuration file not found" in str(exc_info.value)
