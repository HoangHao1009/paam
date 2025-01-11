from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel

from langgraph.graph.graph import CompiledGraph

from app.engine import Survey

class AnalyzerAgent:
    def __init__(self, llm: BaseChatModel, survey: Survey):
        self.survey = survey
        self.llm = llm
        self.tools = self._create_tools()
        self.system_message = SystemMessage(content="You are a proffesional in analyze survey data by question code given. You can search for question information and crosstab them to see relationship between variables. If you return a tabl, you always show a result table for user to read.")
        
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
            html_table = ctab.df.to_html().replace("\n", "")
            html_div = f"""
            <div class="table-bordered scrollbar-thin scrollbar-corner-background h-[320px] w-full overflow-scroll rounded-md border-2 border-black font-sans text-[10px]">
            {html_table}
            </div>
            """
            return html_div

        @tool
        def get_question(question_code: str):
            """Use to get question info by question code"""
            return self.survey[question_code].get_describe()

        return [crosstab, get_question]
        
    def initialize(self) -> CompiledGraph:
        return create_react_agent(model=self.llm, tools=self.tools, state_modifier=self.system_message)
        
        
