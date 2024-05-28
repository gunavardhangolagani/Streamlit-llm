import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import matplotlib.pyplot as plt
import io
import matplotlib.pyplot as plt

# Load environment variables
load_dotenv()

# Set the OpenAI API key from the environment variable
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

def main():
    st.title("Data Analysis Chat Agent")

    # Ensure the API key is available
    if os.getenv("OPENAI_API_KEY"):
        # Initialize the OpenAI model
        llm = OpenAI(temperature=0, verbose=True, openai_api_key=os.getenv("OPENAI_API_KEY"))
        
        # Load the CSV file into a DataFrame
        df = pd.read_csv("customers.csv")

        # Create the Langchain data analysis agent
        data_analysis_agent = create_pandas_dataframe_agent(llm, df, verbose=True)

        # Initialize the chat history
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        # Text area for user input
        user_input = st.text_input("You:", "")

        # Display chat history
        for message in st.session_state.chat_history:
            st.write(f"{message['role']}: {message['content']}")

        # Execute button
        if st.button("Execute"):
            if user_input:
                # Append user's message to chat history
                st.session_state.chat_history.append({'role': 'User', 'content': user_input})

                try:
                    # Invoke the agent with the user input
                    response = data_analysis_agent.invoke(user_input)
                    # Append agent's response to chat history
                    st.session_state.chat_history.append({'role': 'Agent', 'content': response})

                    # Check if the response contains a plot request
                    if 'graph' in response.lower():
                        plot_graph(response, data_analysis_agent)

                except Exception as e:
                    st.error(f"Error analyzing data: {e}")

                # Clear the input field after sending the message
                st.rerun()

    else:
        st.info("Please ensure your OpenAI API key is set in the environment variables.")

def plot_graph(response, data_analysis_agent):
    try:
        # Execute the agent's response to generate the plot
        plot_response = data_analysis_agent.invoke(response)
        
        # Convert the Axes object into a Figure object
        fig = plot_response.get_figure()

        # Display the plot in Streamlit
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error generating plot: {e}")


# Run the main function
if __name__ == "__main__":
    main()