from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph.graph import CompiledGraph
from app.engine import Survey

from typing import List
from langchain_community.tools.tavily_search import TavilySearchResults

class AIOAgent:
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
        self.max_result = 3
        self.tools = self._create_tools()
        self.system_message = SystemMessage(content=self._system_message_guidance)
        
    def add_survey(self, survey: Survey):
        self.survey = survey

    def set_tavily_max_result(self, n: int):
        self.max_result = n
    
    def _create_tools(self):
        @tool
        def crosstab(base: str, target: str, alpha: float=0, pct: bool=False):
            """Use to see relationship between two varibles by looking for crosstable of them.
            Args:
            - base: Question in header of cross table.
            - target: Question in row of cross table.
            - alpha: alpha of statistical test in cross table.
            - pct: decide cross table summarize in count or count percentage format.
            """
            ctab = self.survey.crosstab(base=base, target=target, alpha=alpha, pct=pct)
            return ctab.df_html

        @tool
        def get_question(question_code: str):
            """Use to get question info by question code"""
            return self.survey[question_code].get_describe()

        search_tool = TavilySearchResults(max_results=self.max_result)

        return [crosstab, get_question, search_tool]
    
    def initialize(self, checkpointer) -> CompiledGraph:
        return create_react_agent(
            model=self.llm, tools=self.tools, 
            state_modifier=self.system_message,
            checkpointer=checkpointer
        )
        
    @property
    def _system_message_guidance(self):
        """Returns the System Message Guidance."""
        return (
            "You are a highly capable assistant specialized in **market research and survey data analysis**. "
            "Your primary role is to process, analyze, and retrieve data to assist researchers effectively. "
            "Follow these instructions while performing your tasks:\n\n"
            "1. **Crosstab Analysis**\n"
            "- Use the `crosstab` tool to generate a relationship summary between two survey variables.\n"
            "- Ensure proper handling of parameters:\n"
            "  - `base`: The question to be placed in the header.\n"
            "  - `target`: The question to be placed in the rows.\n"
            "  - `alpha`: The level of significance for statistical testing (optional).\n"
            "  - `pct`: Whether to summarize the data in percentage or count format (default: count).\n"
            "- Respond with an HTML-formatted table, wrapped in a scrollable and styled `<div>` container.\n\n"
            "2. **Question Information**\n"
            "- Use the `get_question` tool to retrieve detailed information about a survey question.\n"
            "- Input the `question_code` parameter accurately to fetch the correct description.\n\n"
            "3. **Search Tool**\n"
            "- Leverage the `TavilySearchResults` tool for retrieving relevant search results or references. "
            "Ensure searches are concise and restricted to the set `max_results`.\n\n"
            "4. **General Behavior**\n"
            "- Be concise, precise, and professional in your responses.\n"
            "- Prioritize clarity and accuracy, ensuring users can easily interpret results or insights.\n"
            "- Respond with formatted data or explanations as needed to maximize user comprehension.\n\n"
            "5. **Scope of Expertise**\n"
            "- Your expertise is focused on **survey data**, **statistical relationships**, and **research support**. "
            "Redirect queries outside this domain politely."
        )


