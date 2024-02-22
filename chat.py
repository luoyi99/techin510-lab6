from tempfile import NamedTemporaryFile
import os

import streamlit as st
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.readers.file import PDFReader
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
)

st.set_page_config(
    page_title="Chat with the PDF",
    page_icon="🦙",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

st.title("Cover Letter Generator📄🤖")

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Upload your resume or company job description to get started"}
    ]


# # Function to generate cover letter
# def generate_cover_letter(resume_docs, job_description):
#     llm = OpenAI(
#         model="gpt-3.5-turbo",
#         temperature=0.0,
#         system_prompt="You are an expert on the content of the document, provide detailed answers to the questions. Use the document to support your answers.",
#     )

#     resume_index = VectorStoreIndex.from_documents(resume_docs)

#     chat_engine = resume_index.as_chat_engine(
#         chat_mode="condense_question", verbose=False, llm=llm
#     )

#     cover_letter = chat_engine.stream_chat(job_description)

#     return cover_letter.response

# if "resume_docs" not in st.session_state.keys():
#     st.session_state.resume_docs = None


resume = st.file_uploader("Upload your resume to get started", type=["pdf"])
if resume:
    bytes_data = resume.read()
    if "job_description" not in st.session_state:
        st.session_state.job_description = None

    if "messages" not in st.session_state.keys():  # Initialize the chat messages history
        st.session_state.messages = [
            {"role": "assistant", "content": "Please paste the job description below:"}
        ]
    
    job_description = st.chat_input(
        "Your question"
    )# Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": job_description})

    with NamedTemporaryFile(delete=False) as tmp:  # open a named temporary file
        tmp.write(bytes_data)  # write data from the uploaded file into it
        with st.spinner(
            text="Loading and indexing the Streamlit docs – hang tight! This should take 1-2 minutes."
        ):
            reader = PDFReader()
            docs = reader.load_data(tmp.name)
            llm = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_API_BASE"),
                model="gpt-3.5-turbo",
                temperature=0.0,
                system_prompt='''
                You are an expert on writing cover letters, your task is to generate a cover letter based on the uploaded resume file and
                a specific job application. The job description is: ''' + job_description + '''.
                Use the provided resume file and job description to craft a compelling letter that highlights relevant skills, experiences, and accomplishments. 
                The cover letter should effectively communicate my suitability for the position and demonstrate a strong fit with the company's 
                needs and values.
                ''',
            )
            index = VectorStoreIndex.from_documents(docs)
    os.remove(tmp.name)  # remove temp file
    

    if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
        st.write("Chat engine not in session state")
        st.session_state.chat_engine = index.as_chat_engine(
            chat_mode="condense_question", verbose=False, llm=llm
        )

    # if "job_description" not in st.session_state:
    #     st.write("Job description not in session state")
    #     st.session_state.job_description = None

    # if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    #     st.write("Messages not in session state")
    #     st.session_state.messages = [
    #         {"role": "assistant", "content": "Please paste the job description below:"}
    #     ]
    #     st.session_state.job_description = st.chat_input(
    #         "Your question",
    #         key="job_description"
    #     )# Prompt for user input and save to chat history
    #     st.session_state.messages.append({"role": "user", "content": st.session_state.job_description})

    # content = ("This is the content of my resume: " + resume + 
    #            "Write a cover letter for the following job description: " + 
    #            st.session_state.job_description)
    # response = st.session_state.chat_engine.stream_chat(content)

    for message in st.session_state.messages:  # Display the prior chat messages
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
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





# if st.session_state.resume_docs is not None:
#     st.write("Resume uploaded successfully!")
#     if "job_description" not in st.session_state:
#         st.session_state.job_description = None

#         if "messages" not in st.session_state.keys():  # Initialize the chat messages history
#             st.session_state.messages = [
#                 {"role": "assistant", "content": "Please paste the job description below:"}
#             ]
        
#         job_description = st.chat_input(
#             "Your question"
#         )# Prompt for user input and save to chat history
#         st.session_state.messages.append({"role": "user", "content": job_description})


#         if job_description:
#             st.session_state.job_description = job_description
#             generated_cover_letter = generate_cover_letter(st.session_state.resume_docs, st.session_state.job_description)
#             st.session_state.messages.append({"role": "assistant", "content": f"Generated Cover Letter: {generated_cover_letter}"})
#             st.session_state.messages.append({"role": "assistant", "content": "If you'd like to edit the cover letter, please enter your message below:"})


#     if prompt := st.chat_input(
#         "Your question"
#     ):  # Prompt for user input and save to chat history
#         st.session_state.messages.append({"role": "user", "content": prompt})

#     for message in st.session_state.messages:  # Display the prior chat messages
#         with st.chat_message(message["role"]):
#             st.write(message["content"])

#     # If last message is not from assistant, generate a new response
#     if st.session_state.messages[-1]["role"] != "assistant":
#         with st.chat_message("assistant"):
#             with st.spinner("Thinking..."):
#                 response = st.session_state.chat_engine.stream_chat(prompt)
#                 st.write_stream(response.response_gen)
#                 message = {"role": "assistant", "content": response.response}
#                 st.session_state.messages.append(message)  # Add response to message history


