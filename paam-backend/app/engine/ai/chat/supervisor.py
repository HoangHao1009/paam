from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import Command
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph.graph import CompiledGraph
from langgraph.graph.state import CompiledStateGraph

from typing_extensions import TypedDict, Literal, List

from .analyzer_agent import AnalyzerAgent
from .research_agent import ResearchAgent
from app.engine import Survey

class State(MessagesState):
    next: str

class PAAMSupervisor:
    def __init__(self, llm: BaseChatModel, survey: Survey, urls: List[str]=[], tavily_max_result: int=1):
        self.llm = llm
        self.survye = survey
        self.analyzer_agent = AnalyzerAgent(llm, survey).initialize()
        self.research_agent = ResearchAgent(llm, urls, tavily_max_result).initialize() 
        self.members = ["analyzer", "researcher", "chitchater"]     
        self.system_prompt = (
            f"You are a supervisor managing workers: {self.members}. Your task is to assign work based on their specialties."
            "\n\nThe workers' specialties:\n"
            "- **analyzer**: Query information and Crosstab on survey questions.\n"
            "- **researcher**: Research based on given topic.\n"
            "- **chitchater**: Casual chat with a focus on market research and analysis.\n"
            "\nAssign the appropriate worker for the task: 'analyzer', 'researcher', or 'chitchater'. If no work is needed or you unsure, respond with 'FINISH'."
        )  
        
    def analyzer_node(self, state: State) -> Command[Literal["supervisor"]]:
        result = self.analyzer_agent.invoke(state)
        return Command(
            update={
                "messages": HumanMessage(content=result["messages"][-1].content, name="analyzer")
            },
            goto="supervisor"
        )
        
    def research_node(self, state: State) -> Command[Literal["supervisor"]]:
        result = self.research_agent.invoke(state)
        return Command(
            update={
                "messages": HumanMessage(content=result["messages"][-1].content, name="researcher")
            },
            goto="supervisor"
        )
        
    def chitchat_node(self, state: State) -> Command[Literal["supervisor"]]:
        system_message = SystemMessage(content=(
            "You are a professional chitchater skilled in basic chatting, with a focus "
            "on market research and data analysis."
        ))
        result = self.llm.invoke([system_message] + state["messages"])
        return Command(
            update={
                "messages": AIMessage(content=result.content, name="chitchater")
            },
            goto=END
        )
        
    def supervisor_node(self, state: State) -> Command[Literal["analyzer", "researcher", "chitchater", "__end__"]]:
        class Router(TypedDict):
            """Worker to route to next. If no workers needed, route to FINISH."""
            next: Literal["analyzer", "researcher", "chitchater", "FINISH"]
        
        messages = [SystemMessage(content=self.system_prompt)] + state["messages"]
        response = self.llm.with_structured_output(Router).invoke(messages)
        goto = response["next"]
        if goto == "FINISH":
            goto = END
            
        return Command(
            update={
                'next': response["next"]
            },
            goto=goto
        )
    
    def initialize(self) -> CompiledStateGraph:
        builder = StateGraph(State)
        builder.add_node("supervisor", self.supervisor_node)
        builder.add_node("analyzer", self.analyzer_node)
        builder.add_node("researcher", self.research_node)
        builder.add_node("chitchater", self.chitchat_node)
        builder.add_edge(START, "supervisor")
        
        return builder.compile()
