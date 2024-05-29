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

# Memory to keep track of past interactions
memory = []

# Planning module
def plan_next_action(question, memory):
    # Check if we have enough information to generate a final answer
    if "excess inventory" in question.lower():
        if any("quantity" in entry for entry in memory):
            return "Generate Final Answer"
        else:
            return "Query_Database"
    return "Query_Database"

# Streamlit interface
st.title("Inventory Management LLM Agent")

query = st.text_input("Enter your inventory management query:")

if st.button("Execute"):
    if query:
        # Decide next action based on the planning module
        next_action = plan_next_action(query, memory)
        
        if next_action == "Query_Database":
            result = agent_executor.invoke(query)
            memory.append({"query": query, "result": result})
            st.write(result)
        
        elif next_action == "Generate Final Answer":
            # Generate final answer using the memory
            for entry in memory:
                if "quantity" in entry["result"]:
                    quantity = entry["result"]["quantity"]
                    min_required = entry["result"]["min_required"]
                    excess_inventory = quantity - min_required
                    final_answer = f"Based on the retrieved information, you currently have {excess_inventory} units of excess inventory."
                    st.write(final_answer)
                    break
        
        # Log the current query and result in memory
        memory.append({"query": query, "result": result})
    else:
        st.write("Please enter a query.")
