import os
import sqlite3
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase

# Load environment variables
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

# Connect to the SQLite database
db = SQLDatabase.from_uri('sqlite:///inventory_management.db')

llm = OpenAI(
    temperature=0,
    verbose=True,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True
)

# Streamlit interface
st.title("Inventory Management LLM Agent")

query = st.text_input("Enter your inventory management query:")

if st.button("Execute"):
    if query:
        result = agent_executor.invoke(query)
        st.write(result)
    else:
        st.write("Please enter a query.")
