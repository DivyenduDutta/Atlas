from abc import ABC
from abc import abstractmethod


class KnowledgeBaseProcessor(ABC):
    @abstractmethod
    def precheck(self) -> bool:
        """
        Perform pre-processing checks.
        Should be run before `self.process()`.
        """
        pass

    @abstractmethod
    def process(self) -> None:
        """
        Performs processing of the files and folders in the knowledge base.
        """
        pass
