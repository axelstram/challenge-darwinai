from abc import ABC, abstractmethod

class Bot(ABC):

    #sends the message to the bot for classification
    #returns dict with 'Category', 'Amount' and 'Description' as keys
    @abstractmethod
    def process_message(self, message) -> dict:
        pass
