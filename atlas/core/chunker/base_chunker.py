from abc import ABC
from abc import abstractmethod
from typing import List, Dict

from atlas.utils.logger import LoggerConfig

LOGGER = LoggerConfig().logger


class BaseChunker(ABC):
    """
    Abstract base class for chunkers that split processed data into smaller "retrieval units.
    """

    @abstractmethod
    def read_processed_data(self) -> List[Dict] | None:
        """
        Read the processed data which is the output of the previous module
        ie,`KnowledgeBaseProcessor`.
        """
        pass

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

    @abstractmethod
    def save_chunked_data(self, chunked_data: List[Dict]) -> None:
        """
        Save the chunked data to a format suitable for later use.

        Args:
            chunked_data (list[dict]): The list of chunked data.
        """
        pass

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
