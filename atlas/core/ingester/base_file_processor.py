from abc import ABC
from abc import abstractmethod
from typing import List, Dict
from pathlib import Path
import json

from atlas.utils.logger import LoggerConfig

LOGGER = LoggerConfig().logger


class KnowledgeBaseProcessor(ABC):
    """
    Abstract base class for processors that handle knowledge base files.

    Args:
        vault_path (str): Path to the knowledge base.
        output_path (str): Path to save the processed data.
    """

    def __init__(self, vault_path: str, output_path: str) -> None:
        self.vault_path = Path(vault_path)
        self.output_path = Path(output_path)

    @abstractmethod
    def precheck(self) -> bool:
        """
        Perform pre-processing checks.
        Should be run before `self.process()`.
        """
        pass

    @abstractmethod
    def process(self) -> List[Dict]:
        """
        Performs processing of the files and folders in the knowledge base
        and extracts relevant information.

        Returns:
            List[Dict]: A list of dictionaries containing processed data.
        """
        pass

    def save_processed_data(self, processed_data: List[Dict]) -> None:
        """
        Save the processed data to a JSON file atomically.
        This ensures that the file is either fully written or not written at all.

        Args:
            processed_data (list[dict]): The list of parsed notes metadata.
        """
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self.output_path.with_suffix(".tmp")

        with tmp_path.open("w", encoding="utf-8") as f:
            json.dump(processed_data, f, indent=2, ensure_ascii=False)

        tmp_path.replace(self.output_path)
        LOGGER.info(f"Processed data successfully to {str(self.output_path)}")

    def ingest(self) -> None:
        """
        Ingest and parse the files in the knowledge base.
        """
        if not self.precheck():
            LOGGER.error("Precheck failed. Aborting processing.")
            return
        processed_data = self.process()
        if processed_data and len(processed_data) > 0:
            LOGGER.info(f"Saving processed data for {len(processed_data)} items.")
            self.save_processed_data(processed_data)
        else:
            LOGGER.warning("No data processed. Nothing to save.")
