import streamlit as st
import google.generativeai as genai
from PIL import Image

# Page Configuration
st.set_page_config(page_title="AI ChatGPT Portfolio", page_icon="🤖", layout="centered")

st.title("🤖 My Complete AI ChatGPT Portfolio")
st.write("A full ChatGPT-style assistant with Chat History, Image Upload, and Text support.")

# Configure Gemini API
import os
import streamlit as st
import google.generativeai as genai

api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

if api_key:
    genai.configure(api_key=api_key)
    
    # Model configuration (Using gemini-pro to avoid 1.5/2.5 version number errors)
    model = genai.GenerativeModel('gemini-3.8-flash')

    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Sidebar for Image Upload option
    st.sidebar.header("Multimodal Settings")
    uploaded_file = st.sidebar.file_uploader("Upload an Image (Optional)", type=["jpg", "jpeg", "png"])
    
    image = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.sidebar.image(image, caption='Uploaded Image', use_column_width=True)
    else:
        st.sidebar.info("No image selected")

    # Display prior chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if "image" in message and message["image"] is not None:
                st.image(message["image"], width=200)
            st.markdown(message["content"])

    # Accept user input via chat input bar at the bottom
    prompt = st.chat_input("Ask anything to the AI...")

    if prompt:
        # Save user message and image in session state history
        user_message = {"role": "user", "content": prompt}
        if image is not None:
            user_message["image"] = image

        st.session_state.messages.append(user_message)

        # Display user message
        with st.chat_message("user"):
            if image is not None:
                st.image(image, width=200)
            st.markdown(prompt)

        # Generate response from Gemini AI
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    if image is not None:
                        response = model.generate_content([image, prompt])
                    else:
                        response = model.generate_content(prompt)
                    
                    bot_response = response.text
                    st.markdown(bot_response)
                    
                    # Save assistant response in chat history
                    st.session_state.messages.append({"role": "assistant", "content": bot_response})
                except Exception as e:
                    error_msg = f"An error occurred: {e}"
                    st.error(error_msg)
