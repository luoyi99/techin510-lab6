from tempfile import NamedTemporaryFile
import os

import streamlit as st
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.readers.file import PDFReader
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Cover Letter Assistant",
    page_icon="✒️",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

st.title("Cover Letter Assistant✒️🤖")

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Enter a job description to generate a cover letter!"}
    ]

uploaded_file = st.file_uploader("Upload your resume to get started", type=["pdf"])
if uploaded_file:
    bytes_data = uploaded_file.read()
    with NamedTemporaryFile(delete=False) as tmp:  # open a named temporary file
        tmp.write(bytes_data)  # write data from the uploaded file into it
        with st.spinner(
            text="Analyzing your resume – hang tight! This should take a moment."
        ):
            reader = PDFReader()
            docs = reader.load_data(tmp.name)
            llm = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_API_BASE"),
                model="gpt-3.5-turbo",
                temperature=0.0,
                system_prompt='''
                You are an expert on writing cover letter.
                Use the provided resume file and job description to craft a compelling letter that 
                highlights relevant skills, experiences, and accomplishments. The cover letter should effectively 
                communicate the candidate's suitability for the position and demonstrate a strong fit with the 
                company's needs and values.
                The cover letter should be about 250 to 400 words long, and should include the following sections:
                1. Header - include Full Name, Phone Number, Email, Date, Name of the company I am applying to
                2. Greeting the hiring manager - example: "Dear Hiring Manager,"
                3. Introduction - start with introducing my name, experience, then talk about 2-3 of my top achievements
                4. Body paragraph - Explain why I am the perfect candidate for the job
                5. Third paragraph - Explain why I am a good match for the company
                6. Closing paragraph
                7. Letter ending and signature - example: "
                Sincerely,
                [Full Name]"
                ''',
            )
            index = VectorStoreIndex.from_documents(docs)
    os.remove(tmp.name)  # remove temp file

    if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(
            chat_mode="condense_question", verbose=False, llm=llm
        )

if prompt := st.chat_input(
    "Your question"
):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.stream_chat(prompt)
            st.write_stream(response.response_gen)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)  # Add response to message history