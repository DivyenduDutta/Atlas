from atlas.utils.logger import LoggerConfig
from atlas.core.ingest.base_file_processor import KnowledgeBaseProcessor

from pathlib import Path

LOGGER = LoggerConfig().logger


class ObsidianVaultProcessor(KnowledgeBaseProcessor):

    _OBSIDIAN_CONFIG_FILES = {
        "app.json",
        "appearance.json",
        "workspace.json",
    }

    def __init__(self, vault_path: str):
        LOGGER.info("ObsidianVaultProcessor initialized.")
        LOGGER.info(f"Obsidian Vault to be processed: {vault_path}")
        self.vault_path = vault_path

    def _find_vault_root(self) -> Path | None:
        """
        Find the root directory of the Obsidian vault by looking for the `.obsidian` folder.

        Args:
            vault_path (str): The starting path to search for the vault root.

        Returns:
            Path | None: The Path to the vault root or None if not found.
        """
        LOGGER.info(f"Finding root of the Obsidian vault")
        path = Path(self.vault_path).resolve()
        if path.is_file():  # defensive guard if the path is a file
            path = path.parent

        for parent in [path, *path.parents]:
            if (parent / ".obsidian").is_dir():
                return parent
        return None

    def _has_obsidian_config(self) -> bool:
        """
        Check if the Obsidian vault contains at least one of the required configuration files.

        Returns:
            bool: True if at least one config file is found, False otherwise.
        """

        _vault_path = Path(self.vault_path).resolve()

        obsidian_dir = _vault_path / ".obsidian"

        return any(
            (obsidian_dir / filename).exists()
            for filename in self._OBSIDIAN_CONFIG_FILES
        )

    def precheck(self) -> bool:
        """
        Check if the provided path is a valid Obsidian vault.

        Returns:
            bool: True if valid Obsidian vault, False otherwise.
        """

        LOGGER.info(f"Checking if {self.vault_path} is a valid Obsidian vault.")
        is_valid_obsidian_vault = True
        vault_root = self._find_vault_root()
        if vault_root is None:
            LOGGER.error(
                f"The path {self.vault_path} is not a valid Obsidian vault. '.obsidian' folder not found."
            )
            is_valid_obsidian_vault = False
        else:
            LOGGER.info(f"Valid Obsidian vault found at: {vault_root}")
            self.vault_path = str(vault_root)

        if is_valid_obsidian_vault:
            is_valid_obsidian_vault = self._has_obsidian_config()

        return is_valid_obsidian_vault

    def process(self) -> None:
        LOGGER.info(f"Processing Obsidian markdown file: {self.vault_path}")
        # Placeholder for actual processing logic
        processed_data = {"file_path": self.vault_path, "content": "Processed content"}
        # return processed_data


if __name__ == "__main__":
    pass
