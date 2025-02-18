import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv("../.env")

st.title("ChatGPT-like clone")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key="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")

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
