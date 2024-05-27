import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_anthropic import ChatAnthropic
from PIL import Image
import os
import io
import base64
import httpx

# Function to get API key securely
def get_api_key():
    return st.secrets["ANTHROPIC_API_KEY"]

# Initialize the ChatAnthropic model
def initialize_model(api_key, temperature):
    os.environ['ANTHROPIC_API_KEY'] = api_key
    model = ChatAnthropic(
        temperature=temperature,
        api_key=api_key,
        model_name="claude-3-opus-20240229"
    )
    return model

# Function to analyze the uploaded image and return a response from Claude
def analyze_image_with_claude(api_key, model_name, image_data, image_media_type):
    client = anthropic.Anthropic(api_key)
    response = client.messages.create(
        model=model_name,
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image_media_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": "Describe this image."
                    }
                ],
            }
        ],
    )
    return response['completion']

# Load API key
api_key = get_api_key()

# Initialize the model with default temperature
temperature = st.sidebar.slider("Set Model Temperature", 0.0, 1.0, 0.5)
model = initialize_model(api_key, temperature)

# Initialize session state variables for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear chat history
def clear_chat_history():
    st.session_state.messages = []

st.sidebar.button("Clear Chat History", on_click=clear_chat_history)

# App title
st.title("Anthropic-Cloud-3")

# Upload image
uploaded_image = st.file_uploader("Upload an image for analysis", type=["png", "jpg", "jpeg"])

if uploaded_image is not None:
    # Display the uploaded image
    image = Image.open(uploaded_image)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Convert image to base64
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()
    image_data = base64.b64encode(img_bytes).decode("utf-8")
    image_media_type = uploaded_image.type

    # Analyze the image with Claude
    response_content = analyze_image_with_claude(api_key, "claude-3-opus-20240229", image_data, image_media_type)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response_content)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_content})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response for user input
    system_message = SystemMessage(content="You are a helpful assistant")
    human_message = HumanMessage(content=prompt)

    response = model.invoke([system_message, human_message])

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response.content)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response.content})

st.write("Powered by [Anthropic AI](https://anthropic.com)")
