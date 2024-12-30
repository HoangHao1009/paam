from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage

from langgraph.graph.graph import CompiledGraph
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain_core.language_models.chat_models import BaseChatModel

class ResearchAgent:
    def __init__(self, llm: BaseChatModel, urls: list=[], tavily_max_result: int=1):
        self.llm = llm
        self.urls = urls
        self.max_result = tavily_max_result
        self.tools = self._create_tools()
        self.system_message = SystemMessage(content="You are a proffesional in research for information.")
        
    def _create_tools(self):
        #retriever_tool
        # docs = [WebBaseLoader(url).load() for url in self.urls]
        # docs_list = [item for sublist in docs for item in sublist]
        
        # text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        #     chunk_size=100, chunk_overlap=50
        # )
        
        # doc_splits = text_splitter.split_documents(docs_list)

        # vectorstore = Chroma.from_documents(
        #     documents=doc_splits,
        #     collection_name="rag-chroma",
        #     embedding=OpenAIEmbeddings(),
        # )

        # retriever_tool = create_retriever_tool(
        #     vectorstore.as_retriever(),
        #     "retrieve_blog_posts",
        #     "Search and return information about Lilian Weng blog posts on LLM agents, prompt engineering, and adversarial attacks on LLMs.",
        # )
        # #search tool
        search_tool = TavilySearchResults(max_results=self.max_result)
        
        # return [retriever_tool, search_tool]
        return [search_tool]
        
    def initialize(self) -> CompiledGraph:
        return create_react_agent(model=self.llm, tools=self.tools, state_modifier=self.system_message)
        
        
