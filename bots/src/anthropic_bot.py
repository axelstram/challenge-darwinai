from bots.interfaces.bot import Bot
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

class AnthropicBot(Bot):
    def __init__(self, api_key=None):
        if os.environ.get('ENV') != 'PRODUCTION':
            load_dotenv()

        self.llm = ChatAnthropic(temperature=0, model_name="claude-3-opus-20240229", anthropic_api_key=api_key or os.environ.get('ANTHROPIC_API_KEY'))
        self.input = """You classify inputs into the following categories: Housing, Transportation, Food, Utilities, Insurance, Medical/Healthcare, Savings, 
                        Debt, Education, Entertainment, and Other. If the message isn't related to expenses at all, the category is None. If the category isn't None, 
                        your answer should always contain the category, the amount (just the number, without dollar sign) and a description with just the item name. If it doesn't fit any category, 
                        just respond with category: 'None'. Your response should always be in english. The text to analyze is the following: """

    
    def process_message(self, message):
        prompt = ChatPromptTemplate.from_messages([("system", self.input), ("human", "{text}")])
        chain = prompt | self.llm
        res = chain.invoke(message).content

        d = dict(e.split(': ') for e in res.split('\n'))
        d2 = {}
        for k,v in d.items():
            d2[k.capitalize()] = v

        return d2
