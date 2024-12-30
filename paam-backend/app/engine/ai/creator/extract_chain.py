from pydantic import BaseModel
from typing import List

from langchain.docstore.document import Document
from langchain_openai import ChatOpenAI
from langchain.utils.openai_functions import convert_pydantic_to_openai_function
from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser
from langchain.schema.runnable import RunnableLambda

from .schemas import Info
from .prompts import extraction_prompt

class ExtractionChain(BaseModel):
    def __init__(self, api_key: str, model: str="gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        
    def extract(self, pages: List[Document]):
        model = ChatOpenAI(model=self.model, temperature=0, openai_api_key=self.api_key)
        
        prep = RunnableLambda(
            lambda x: [{"input": page.page_content} for page in pages]
        )
                
        extraction_model = model.bind(
            functions=[convert_pydantic_to_openai_function(Info)],
            function_call={'name': 'Info'}
        )
        
        extraction_chain = extraction_prompt | extraction_model | JsonKeyOutputFunctionsParser(key_name="questions")
        
        final_chain = prep | extraction_chain.map()
        
        return final_chain.invoke(pages)
        
        
        