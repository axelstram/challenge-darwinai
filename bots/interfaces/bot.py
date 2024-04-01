from abc import ABC, abstractmethod

class Bot(ABC):

    #sends the message to the bot for classification
    #returns dict with 'Category', 'Amount' and 'Description' as keys if message was related to expenses
    #if not, it return a dict with 'Category' = None
    @abstractmethod
    def process_message(self, message) -> dict:
        pass
