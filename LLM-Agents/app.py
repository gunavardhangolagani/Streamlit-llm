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

# Connect to the SQLite database (create it if it doesn't exist)
conn = sqlite3.connect('sql_lite_database.db')
cursor = conn.cursor()

# Create tables
create_table_queries = [
    """
    CREATE TABLE IF NOT EXISTS AGENTS (
        AGENT_CODE CHAR(6) NOT NULL PRIMARY KEY,
        AGENT_NAME CHAR(40),
        WORKING_AREA CHAR(35),
        COMMISSION NUMBER(10,2),
        PHONE_NO CHAR(15),
        COUNTRY VARCHAR2(25)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS CUSTOMER (
        CUST_CODE VARCHAR2(6) NOT NULL PRIMARY KEY,
        CUST_NAME VARCHAR2(40) NOT NULL,
        CUST_CITY CHAR(35),
        WORKING_AREA VARCHAR2(35) NOT NULL,
        CUST_COUNTRY VARCHAR2(20) NOT NULL,
        GRADE NUMBER,
        OPENING_AMT NUMBER(12,2) NOT NULL,
        RECEIVE_AMT NUMBER(12,2) NOT NULL,
        PAYMENT_AMT NUMBER(12,2) NOT NULL,
        OUTSTANDING_AMT NUMBER(12,2) NOT NULL,
        PHONE_NO VARCHAR2(17) NOT NULL,
        AGENT_CODE CHAR(6) NOT NULL REFERENCES AGENTS
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS ORDERS (
        ORD_NUM NUMBER(6,0) NOT NULL PRIMARY KEY,
        ORD_AMOUNT NUMBER(12,2) NOT NULL,
        ADVANCE_AMOUNT NUMBER(12,2) NOT NULL,
        ORD_DATE DATE NOT NULL,
        CUST_CODE VARCHAR2(6) NOT NULL REFERENCES CUSTOMER,
        AGENT_CODE CHAR(6) NOT NULL REFERENCES AGENTS,
        ORD_DESCRIPTION VARCHAR2(60) NOT NULL
    );
    """
]

for query in create_table_queries:
    cursor.execute(query)

# Insert data into tables
insert_queries = [
    "INSERT OR IGNORE INTO AGENTS VALUES ('A007', 'Ramasundar', 'Bangalore', '0.15', '077-25814763', '')",
    "INSERT OR IGNORE INTO AGENTS VALUES ('A003', 'Alex', 'London', '0.13', '075-12458969', '')",
    # Add more insert statements here...
]

for query in insert_queries:
    cursor.execute(query)

conn.commit()

# Setup LangChain SQL agent
db = SQLDatabase.from_uri('sqlite:///sql_lite_database.db')

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
st.title("SQL LLM Agent")

query = st.text_input("Enter your SQL query:")

if st.button("Execute"):
    if query:
        result = agent_executor.invoke(query)
        st.write(result)
    else:
        st.write("Please enter a query.")

# Close the cursor and connection
cursor.close()
conn.close()
