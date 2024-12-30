from pydantic import BaseModel
from typing import List

from langchain.docstore.document import Document
from langchain_openai import ChatOpenAI
from langchain.utils.openai_functions import convert_pydantic_to_openai_function
from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema.runnable import RunnableLambda

from .schemas import Info
from .prompts import extraction_prompt


from .extract_chain import ExtractionChain

class QuestionnaireCreator(BaseModel):
    def __init__(self, design_file_path: str, api_key: str, model: str="gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self.design_file_path = design_file_path
        self.pages = self._get_pages()
        
    def _get_pages(self) -> List[Document]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4096,
            chunk_overlap=1000, 
        )
        loader = PyPDFLoader(self.design_file_path)
        pages = loader.load_and_split(text_splitter)

        return pages

    @property
    def extraction_chain(self):
        model = ChatOpenAI(model=self.model, temperature=0, openai_api_key=self.api_key)
        
        prep = RunnableLambda(
            lambda x: [{"input": page.page_content} for page in self.pages]
        )
                
        extraction_model = model.bind(
            functions=[convert_pydantic_to_openai_function(Info)],
            function_call={'name': 'Info'}
        )
        
        extraction_chain = extraction_prompt | extraction_model | JsonKeyOutputFunctionsParser(key_name="questions")
        
        final_chain = prep | extraction_chain.map()
        
        return final_chain.invoke(self.pages)
