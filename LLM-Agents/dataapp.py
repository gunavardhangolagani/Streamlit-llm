import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from langchain_openai import OpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

# Load environment variables
load_dotenv()

st.title("DataAnalyst Agent")

# Enter your OpenAI API private access key here.
api_key = st.secrets["OPENAI_API_KEY"]
os.environ['OPENAI_API_KEY'] = api_key

# Load the dataset
df = pd.read_csv("customers.csv")

# Create the data analysis agent
data_analysis_agent = create_pandas_dataframe_agent(OpenAI(temperature=0), df, verbose=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to generate and plot graphs based on user prompts
def generate_plot(prompt, dataframe):
    plot_functions = {
        "top 5 countries": plot_top_countries,
        "customer distribution by age": plot_age_distribution,
        # Add more keywords and their corresponding functions here
    }
    
    for key, func in plot_functions.items():
        if key in prompt.lower():
            return func(dataframe)
    
    return "No specific graph-related instructions found."

def plot_top_countries(dataframe):
    country_counts = dataframe['Country'].value_counts().head(5)
    fig, ax = plt.subplots()
    country_counts.plot(kind='bar', ax=ax)
    ax.set_title('Top 5 Countries with Most Customers')
    ax.set_xlabel('Country')
    ax.set_ylabel('Number of Customers')
    st.pyplot(fig)
    return "Here's the graph for the top 5 countries with the most customers."

def plot_age_distribution(dataframe):
    if 'Age' in dataframe.columns:
        fig, ax = plt.subplots()
        dataframe['Age'].plot(kind='hist', bins=20, ax=ax)
        ax.set_title('Customer Distribution by Age')
        ax.set_xlabel('Age')
        ax.set_ylabel('Frequency')
        st.pyplot(fig)
        return "Here's the age distribution of customers."
    else:
        return "The 'Age' column is not present in the dataset."

# User input
if prompt := st.chat_input("Ask a question about the data:"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if any(word in prompt.lower() for word in ["show data", "display data", "view data"]):
            st.dataframe(df.head(10))  # Display the first 10 rows of the dataframe
            response = "Here are the first few rows of the dataset."
        elif any(word in prompt.lower() for word in ["plot", "graph", "visualize", "chart"]):
            response = generate_plot(prompt, df)
        else:
            response = data_analysis_agent.invoke(prompt)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})