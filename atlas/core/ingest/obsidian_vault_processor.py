from datetime import date
from atlas.utils.logger import LoggerConfig
from atlas.core.ingest.base_file_processor import KnowledgeBaseProcessor

from pathlib import Path
from datetime import date, datetime
import re
import yaml
import json
from typing import Dict, Any, List

LOGGER = LoggerConfig().logger


class ObsidianVaultProcessor(KnowledgeBaseProcessor):

    _OBSIDIAN_CONFIG_FILES = {
        "app.json",
        "appearance.json",
        "workspace.json",
    }

    def __init__(self, vault_path: str, output_path: str) -> None:
        LOGGER.info("ObsidianVaultProcessor initialized.")
        LOGGER.info(f"Obsidian Vault to be processed: {vault_path}")
        self.vault_path = Path(vault_path)
        self.output_path = Path(output_path)

    def _find_vault_root(self) -> Path | None:
        """
        Find the root directory of the Obsidian vault by looking for the `.obsidian` folder.

        Args:
            vault_path (str): The starting path to search for the vault root.

        Returns:
            Path | None: The Path to the vault root or None if not found.
        """
        LOGGER.info(f"Finding root of the Obsidian vault")
        path = self.vault_path.resolve()
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

        _vault_path = self.vault_path.resolve()

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

        LOGGER.info(f"Checking if {str(self.vault_path)} is a valid Obsidian vault.")
        is_valid_obsidian_vault = True
        vault_root = self._find_vault_root()
        if vault_root is None:
            LOGGER.error(
                f"The path {str(self.vault_path)} is not a valid Obsidian vault. '.obsidian' folder not found."
            )
            is_valid_obsidian_vault = False
        else:
            LOGGER.info(f"Valid Obsidian vault found at: {vault_root}")
            self.vault_path = vault_root

        if is_valid_obsidian_vault:
            LOGGER.info("Checking for presence of valid Obsidian configuration files.")
            is_valid_obsidian_vault = self._has_obsidian_config()
            if not is_valid_obsidian_vault:
                LOGGER.error(
                    f"The Obsidian vault at {str(self.vault_path)} does not contain any valid configuration files."
                )

        return is_valid_obsidian_vault

    def _normalize_yaml(self, obj):
        if isinstance(obj, dict):
            return {k: self._normalize_yaml(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._normalize_yaml(v) for v in obj]
        elif isinstance(obj, (date, datetime)):
            return obj.isoformat()
        else:
            return obj

    def _extract_frontmatter(self, text: str) -> tuple[dict, str]:
        """
        Detect and extract YAML frontmatter from the top of a Markdown file

        Below we can see an example of a markdown file with frontmatter:
        ---
        title: Atlas
        tags: [llm, rag]
        ---

        # Introduction
        Hello world

        Args:
            text (str): The content of the Markdown file.

        Returns:
            tuple[dict, str]: A tuple containing the frontmatter as a dictionary and the body text.
        """

        if text.startswith("---"):
            match = re.match(r"^---\n(.*?)\n---\n(.*)", text, re.S)
            if match:
                frontmatter = self._normalize_yaml(yaml.safe_load(match.group(1))) or {}
                body = match.group(2)
                return frontmatter, body
        return {}, text

    def _extract_headings(self, text: str) -> list[dict]:
        """
        Extract Markdown headings from the text.

        Args:
            text (str): One line of the Markdown file content.

        Returns:
            list[dict]: A list of dictionaries containing heading levels and titles.
        """

        headings = []
        for line in text.splitlines():
            match = re.match(r"^(#{1,6})\s+(.*)", line)
            if match:
                headings.append(
                    {"level": len(match.group(1)), "title": match.group(2).strip()}
                )
        return headings

    def _extract_tags(self, text: str) -> list[str]:
        """
        Extract tags from the text.

        Below we can see an example of tags in a markdown file:
        This is a #note about #LLM and #deep_learning

        Args:
            text (str): The Markdown file content.

        Returns:
            list[str]: A list of unique tags found in the text.
        """
        return sorted(set(re.findall(r"#(\w+)", text)))

    def _extract_wikilinks(self, text: str) -> list[str]:
        """
        Extract wikilinks from the text.

        Below we can see an example of wikilinks in a markdown file:
        This is a link to [[Note1]] and another link to [[Note2|Custom Title]].

        Args:
            text (str): The Markdown file content.

        Returns:
            list[str]: A list of unique wikilinks found in the text.
        """
        return sorted(set(re.findall(r"\[\[(.*?)\]\]", text)))

    def _parse_markdown_note(self, note_path: Path, vault_path: Path) -> Dict[str, Any]:
        """
        Parse a Markdown note to extract metadata and content.

        Args:
            note_path (Path): The path to the Markdown note.
            vault_path (Path): The root path of the Obsidian vault.

        Returns:
            dict: A dictionary containing the note's metadata and content.
        """

        text = note_path.read_text(encoding="utf-8")

        frontmatter, body = self._extract_frontmatter(text)

        return {
            "note_id": note_path.relative_to(vault_path).as_posix(),
            "title": note_path.stem,
            "relative_path": note_path.relative_to(vault_path).as_posix(),
            "raw_text": body,
            "frontmatter": frontmatter,
            "headings": self._extract_headings(body),
            "tags": self._extract_tags(body),
            "wikilinks": self._extract_wikilinks(body),
            "word_count": len(body.split()),
        }

    def save_processed_data(self, processed_data: List[Dict]) -> None:
        """
        Save the extracted notes metadata to a JSON file.
        Replaces any existing file at the output path.

        Args:
            notes (list[dict]): The list of parsed notes metadata.
        """

        with self.output_path.open("w", encoding="utf-8") as f:
            json.dump(processed_data, f, indent=2, ensure_ascii=False)

    def process(self) -> list[dict]:
        """
        Process the Obsidian vault to extract notes metadata.

        Returns:
            list[dict]: A list of dictionaries containing notes metadata ie, processed data.
        """

        LOGGER.info(f"Processing Obsidian markdown files from {str(self.vault_path)}")

        vault_path = self.vault_path.resolve()
        notes = []

        for md_file in vault_path.rglob("*.md"):
            if ".obsidian" in md_file.parts:
                continue
            note_data = self._parse_markdown_note(md_file, vault_path)
            notes.append(note_data)
        return notes


if __name__ == "__main__":
    obsidian_vault_path = r"D:\\Deep learning\\Test Obsidian Vault"
    obsidian_index_path = r"D:\\Deep learning\\Atlas\\Resources\\obsidian_index.json"
    obsidian_vault_processor = ObsidianVaultProcessor(
        vault_path=obsidian_vault_path, output_path=obsidian_index_path
    )
    obsidian_vault_processor.ingest()
