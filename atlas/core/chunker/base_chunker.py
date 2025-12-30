from abc import ABC
from abc import abstractmethod
from typing import List, Dict
from pathlib import Path
import json

from atlas.utils.logger import LoggerConfig

LOGGER = LoggerConfig().logger


class BaseChunker(ABC):
    """
    Abstract base class for chunkers that split processed data into smaller "retrieval units.

    Args:
        processed_data_path (str): Path to the processed data file.
        output_path (str): Path to save the chunked data.
    """

    def __init__(self, processed_data_path: str, output_path: str) -> None:
        LOGGER.info("-" * 20)
        LOGGER.info("StructuralChunker initialized.")
        LOGGER.info(f"Chunking processed data at {processed_data_path}")
        self.processed_data_path = Path(processed_data_path)
        self.output_path = Path(output_path)

    def read_processed_data(self) -> List[Dict] | None:
        """
        Read the processed data which is the output of the previous module
        ie, `KnowledgeBaseProcessor`.

        Returns:
            List[Dict] | None: The processed data as a list of dictionaries or None if an error occurs.
        """
        try:
            with open(self.processed_data_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            LOGGER.info("Processed data successfully read.")
            return data
        except Exception as e:
            LOGGER.error(f"Error reading processed data: {e}")
            return None

    @abstractmethod
    def create_chunks(self, processed_data: List[Dict]) -> List[Dict]:
        """
        Chunk the processed data into smaller "retrieval units" based on a chunking strategy.

        Args:
            processed_data (list[dict]): The list of processed data to be chunked.

        Returns:
            list[dict]: The list of chunked data.
        """
        pass

    def save_chunked_data(self, chunked_data: List[Dict]) -> None:
        """
        Save the chunked data to the output path in JSON format.
        This method writes to a temporary file first and then renames it to ensure atomicity.
        This prevents data corruption in case of interruptions during the write process.

        Args:
            chunked_data (List[Dict]): The chunked data to be saved.
        """
        tmp_path = self.output_path.with_suffix(".tmp")

        with tmp_path.open("w", encoding="utf-8") as f:
            json.dump(chunked_data, f, indent=2, ensure_ascii=False)

        tmp_path.replace(self.output_path)

    def chunk(self) -> None:
        """
        Perform the chunking process.
        """
        processed_data = self.read_processed_data()
        if processed_data is None or len(processed_data) == 0:
            LOGGER.error("No processed data available for chunking. Aborting.")
            return
        LOGGER.info(f"Creating chunks for {len(processed_data)} items.")
        chunked_data = self.create_chunks(processed_data)
        if chunked_data and len(chunked_data) > 0:
            LOGGER.info(f"Saving chunked data for {len(chunked_data)} items.")
            self.save_chunked_data(chunked_data)
        else:
            LOGGER.warning("No chunked data created. Nothing to save.")
