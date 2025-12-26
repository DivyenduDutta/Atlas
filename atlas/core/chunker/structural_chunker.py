from atlas.utils.logger import LoggerConfig
from atlas.core.chunker.base_chunker import BaseChunker

from pathlib import Path
from typing import List, Dict
import json

LOGGER = LoggerConfig().logger


class StructuralChunker(BaseChunker):

    def __init__(self, processed_data_path: str, output_path: str) -> None:
        LOGGER.info("StructuralChunker initialized.")
        LOGGER.info(f"Chunking based on processed data at {processed_data_path}")
        self.processed_data_path = Path(processed_data_path)
        self.output_path = Path(output_path)

    def read_processed_data(self) -> List[Dict] | None:
        """
        Read the obsidian indexed data which is the output of the previous module
        ie, `ObsidianVaultProcessor`.

        Returns:
            List[Dict] | None: The obsidian indexed data as a list of dictionaries or None if an error occurs.
        """

        try:
            with open(self.processed_data_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            LOGGER.info("Obsidian indexed data successfully read.")
            return data
        except Exception as e:
            LOGGER.error(f"Error reading processed data: {e}")
            return None

    def create_chunks(self, processed_data: List[Dict]) -> None:
        pass

    def save_chunked_data(self, chunked_data: List[Dict]) -> None:
        pass


if __name__ == "__main__":
    processed_data_path = r"D:\\Deep learning\\Atlas\\Resources\\obsidian_index.json"
    output_path = r"D:\\Deep learning\\Atlas\\Resources\\chunked_data.json"
    chunker = StructuralChunker(processed_data_path, output_path)
    obsidian_indexed_data = chunker.read_processed_data()
    if obsidian_indexed_data is not None:
        LOGGER.info(f"Read {len(obsidian_indexed_data)} records from processed data.")
