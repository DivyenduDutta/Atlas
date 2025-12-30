from dataclasses import dataclass
import yaml
from pathlib import Path

from atlas.utils.logger import LoggerConfig

LOGGER = LoggerConfig().logger


@dataclass
class EncoderConfig:
    """Configuration parameters for the encoder."""

    model_name: str
    batch_size: int
    normalize_embeddings: bool
    device: str


def load_encoder_config(path: Path) -> EncoderConfig:
    """
    Load encoder configuration from a YAML file.

    Args:
        path (Path): Path to the encoder YAML configuration file.
    """
    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError as e:
        LOGGER.error(f"Encoder configuration file not found: {path}")
        raise FileNotFoundError(f"Encoder configuration file not found: {path}")

    if not data:
        LOGGER.error(f"Encoder configuration file is empty: {path}")
        raise ValueError(f"Encoder configuration file is empty: {path}")

    LOGGER.info(f"Encoder configuration loaded successfully from {path}")
    return EncoderConfig(**data)
