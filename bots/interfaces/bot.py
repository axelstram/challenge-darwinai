from abc import ABC, abstractmethod

class Bot(ABC):

    #sends the message to the bot for classification
    #returns dict with 'category', 'price' and 'description' as keys
    @abstractmethod
    def process_message(self, message) -> dict:
        pass
   