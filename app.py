import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_fireworks import ChatFireworks
import os

# Function to get API key securely
def get_api_key():
    return st.secrets["FIREWORKS_API_KEY"]

# Initialize the ChatFireworks model
def initialize_model(api_key):
    os.environ['FIREWORKS_API_KEY'] = api_key
    model = ChatFireworks(
        model="accounts/fireworks/models/mixtral-8x7b-instruct",
        temperature=0.0,
        verbose=True
    )
    return model

# Load API key
api_key = get_api_key()

# Initialize the model
model = initialize_model(api_key)

# Initialize session state variables
if "chats" not in st.session_state:
    st.session_state.chats = []
if "current_chat" not in st.session_state:
    st.session_state.current_chat = []
if "chat_names" not in st.session_state:
    st.session_state.chat_names = []
if "current_chat_name" not in st.session_state:
    st.session_state.current_chat_name = ""
if "chat_id" not in st.session_state:
    st.session_state.chat_id = 0

def handle_user_input():
    user_input = st.session_state.user_input
    print("User Input:", user_input)  # Print user input
    if user_input:
        # Create system and human messages
        system_message = SystemMessage(content="You are a helpful assistant ")
        human_message = HumanMessage(content=user_input)

        # Get the model's response
        response = model.invoke([system_message, human_message])
        print("Bot Response:", response.content)  # Print bot response

        # Update the current chat history
        st.session_state.current_chat.append({"role": "user", "content": user_input})
        st.session_state.current_chat.append({"role": "bot", "content": response.content})
        
        # Update the current chat name
        st.session_state.current_chat_name = user_input[:30] if not st.session_state.current_chat_name else st.session_state.current_chat_name
        print("Current Chat:", st.session_state.current_chat)  # Print current chat
        
        # Clear the input field
        st.session_state.user_input = ""


# Function to save current chat and start a new one
def save_and_new_chat():
    if st.session_state.current_chat:
        chat_name = st.session_state.current_chat_name or f"Chat {st.session_state.chat_id}"
        st.session_state.chats.append({"id": st.session_state.chat_id, "messages": st.session_state.current_chat, "name": chat_name})
        st.session_state.current_chat = []
        st.session_state.current_chat_name = ""
        st.session_state.chat_id += 1

# Sidebar for past chats
st.sidebar.title("Chat History")
if st.sidebar.button("New Chat"):
    save_and_new_chat()
for chat in st.session_state.chats:
    if st.sidebar.button(chat["name"]):
        st.session_state.current_chat = chat["messages"]
        st.session_state.current_chat_name = chat["name"]

# Chat interface
st.title("Chatbot Interface")
chat_container = st.container()

# Display the chat history
with chat_container:
    for message in st.session_state.current_chat:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**Bot:** {message['content']}")

# Text input for user message at the bottom using st.chat_input
user_input = st.chat_input("Type your message here...")
if user_input:
    st.session_state.user_input = user_input
    handle_user_input()

# Streamlit footer
st.write("Powered by [Fireworks AI](https://fireworks.ai)")
