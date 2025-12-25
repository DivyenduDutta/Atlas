from abc import ABC
from abc import abstractmethod
from typing import List, Dict
from pathlib import Path

from atlas.utils.logger import LoggerConfig

LOGGER = LoggerConfig().logger


class KnowledgeBaseProcessor(ABC):
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

    @abstractmethod
    def save_processed_data(self, processed_data: List[Dict]) -> None:
        """
        Save the processed data to a format suitable for later use.

        Args:
            notes (list[dict]): The list of parsed metadata ie, processed data.
        """
        pass

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
