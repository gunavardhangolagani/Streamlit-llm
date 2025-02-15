# Data Analyst Agent

The Data Analyst Agent is an AI-powered assistant that utilizes GPT-4 for data analysis. It integrates with SQL databases using LLM agents equipped with specialized tools to process user queries efficiently and provide insightful results. 

For results do checkout here : [![Link](https://img.shields.io/badge/Action_Input-link-blue)](https://github.com/gunavardhangolagani/Streamlit-llm/blob/main/Data_Analyst_agent/Action%20input.png)  [![Link](https://img.shields.io/badge/Action_Output-link-blue)](https://github.com/gunavardhangolagani/Streamlit-llm/blob/main/Data_Analyst_agent/Analyst_output.png)

## Features

  - **LLM-Powered Analysis**:  Uses GPT-4 for intelligent data interpretation.

  - **Agent-Based Execution**: Modular tools enable optimized query execution.

  - **SQL Database Support**: Connects to PostgreSQL and also uses sqlite3 for data retrieval.

  - **Containerized Deployment**: Supports Docker for easy setup and scaling.

  - **User-Friendly API**: Provides an accessible interface for data interaction.

## Architecture
   ![Concept map](https://github.com/gunavardhangolagani/Streamlit-llm/assets/163413946/22578503-df18-46b0-a239-4e8c46b697cb)
   
  - GPT-4 Analysis Module: Processes and interprets SQL query results.

  - LLM Agents Module: Utilizes various tools dynamically to enhance output.

  - SQL Database Connection: Interfaces with PostgreSQL to retrieve relevant data.

  - Web API Interface: Exposes endpoints for user interaction.



## Prerequisites

  - There are no strict prerequisites, but users must:

  - Install necessary dependencies from requirements.txt.

  - Set up the required API keys in the .env file.

  - Ensure they have Docker installed for containerized deployment.

## Installation & Setup

### 1. Clone the Repository
```
  https://github.com/gunavardhangolagani/Streamlit-llm.git
```

### 2. Install Dependencies
```
   pip install -r requirements.txt
```

### 3. Setup Environment Variables

Create a .env file and specify necessary API keys and database credentials.
```
  DATABASE_URL=postgresql://user:password@localhost/dbname
```
```
  API_KEY=your_api_key_here
```

### 4. Run the Application
``` fastapi
  uvicorn main:app --host 0.0.0.0 --port 8000
```

## Deployed Agents 
  - [Guna-SQLAgent](https://app-llm-dlwefkp5w3qizqbyhzbubj.streamlit.app/)

  - [Harsha-SqlAgent](https://app-llm-dlwefkp5w3qizqbyhzbubj.streamlit.app/)


# Conclusion

The Data Analyst Agent provides a streamlined way to analyze data using AI and SQL. With its modular tool-based architecture, it ensures optimal query execution and insightful results. Deploy it with Docker for scalability and ease of use.

