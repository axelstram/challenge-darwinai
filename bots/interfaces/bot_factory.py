from abc import ABC, abstractmethod

class BotFactory(ABC):
    @abstractmethod
    def create_bot(self):
        pass