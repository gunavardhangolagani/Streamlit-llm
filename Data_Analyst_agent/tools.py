# Import things that are needed generically
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from typing import Optional, Type
from pydantic import BaseModel
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from sqlalchemy import create_engine
from langchain.tools import BaseTool

class CalculatorInput(BaseModel):
    a: int
    b: int

class CustomCalculatorTool(BaseTool):
    name = "Calculator"
    description = "useful for when you need to answer questions about math"
    args_schema: Type[BaseModel] = CalculatorInput
    return_direct: bool = True

    def _run(
        self, a: int, b: int, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        return str(a * b)

    async def _arun(
        self,
        a: int,
        b: int,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError("Calculator does not support async")

class SQLQueryInput(BaseModel):
    query: str

class QueryDatabaseTool(BaseTool):
    name = "Query_Database"
    description = "useful for querying a database with SQL queries"
    args_schema: Type[BaseModel] = SQLQueryInput
    return_direct: bool = True

    def __init__(self, database_file_path: str):
        self.engine = create_engine(database_file_path)

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        with self.engine.connect() as connection:
            result = connection.execute(query)
            return str([dict(row) for row in result])

    async def _arun(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError("Query_Database does not support async")

class MemoryInput(BaseModel):
    question: str
    memory_content: Optional[str] = None

class GenerateFinalAnswerTool(BaseTool):
    name = "Generate_Final_Answer"
    description = "use this tool to generate the final answer, checking if it can be given with memory"
    args_schema: Type[BaseModel] = MemoryInput
    return_direct: bool = True

    def _run(
        self, question: str, memory_content: Optional[str] = None, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        if memory_content:
            return f"Answer from memory: {memory_content}"
        else:
            return "Answer requires additional tools to provide."

    async def _arun(
        self,
        question: str,
        memory_content: Optional[str] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        raise NotImplementedError("Generate_Final_Answer does not support async")