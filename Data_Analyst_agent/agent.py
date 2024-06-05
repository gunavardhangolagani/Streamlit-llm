import openai
import streamlit as st
import os
from langchain_community.utilities import SQLDatabase
from langchain_openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.tools import BaseTool
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.agents.agent_types import AgentType
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

st.title("Data Analyst Agent")

api_key = st.secrets["OPENAI_API_KEY"]
os.environ['OPENAI_API_KEY'] = api_key

# Define your custom tools
class CustomCalculatorTool(BaseTool):
    name = "custom_calculator"
    description = "Tool to perform custom calculations."

    def _run(self, query: str):
        # Example implementation
        try:
            result = eval(query)
            return result
        except Exception as e:
            return str(e)

class QueryDatabaseTool(BaseTool):
    name = "query_database"
    description = "Tool to query the SQL database."

    def _run(self, query: str):
        try:
            db = SQLDatabase.from_uri("sqlite:///sql_lite_database.db")
            result = db.run(query)
            return result
        except Exception as e:
            return str(e)

class GenerateFinalAnswerTool(BaseTool):
    name = "generate_final_answer"
    description = "Tool to generate final answers based on provided information."

    def _run(self, input_text: str):
        # Example implementation
        try:
            return f"Final Answer: {input_text}"
        except Exception as e:
            return str(e)

# Initialize the database
db = SQLDatabase.from_uri('sqlite:///sql_lite_database.db')

# Choose the LLM model
llm = ChatOpenAI(
    temperature=0,
    model_name="gpt-4",
    verbose=True,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)

# Initialize your custom tools
calculator_tool = CustomCalculatorTool()
query_database_tool = QueryDatabaseTool()
generate_final_answer_tool = GenerateFinalAnswerTool()

# Setup the toolkit with only the database and LLM
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Create the agent with custom tools
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    additional_tools=[calculator_tool, query_database_tool, generate_final_answer_tool],
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = str(agent_executor.invoke(prompt)["output"])
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})