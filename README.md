# Techin510-lab6
This tool is designed to simplify the process of crafting tailored cover letters for job applications. By leveraging user-provided resumes and job descriptions, the generator creates customized cover letters that highlight relevant skills and experiences.

## How to run
Open the terminal and run the following commands:
1. `python -m venv venv`
1. `source venv/bin/activate`
1. `pip install -r requirements.txt`
1. cp .env.sample .env
1. Change the .env file to match your environment
1. `streamlit run app.py`

## What's Included
- `requirements.txt`: Required packages to run the application
- `app.py`: The main application file containing Streamlit code to render the app and handle user interactions.

## Lessons Learned
- Explored different use cases for the OpenAI API, such as generating text and images based on prompts and utilizing pre-trained language models for various tasks.
- Implementing file uploaders feature to enable users to interact with the application by uploading files.
- Exploring advanced Streamlit components, such as the chat input, to create more interactive user experiences.
- Understanding and implementing the concept of Retrieval Augmented Generation (RAG) for enhancing text generation capabilities within the application.
- Learned how to integrate LLamaIndex functionalities into the application to extract and manipulate information from PDF documents.


## Questions
- Can the file uploader be seamlessly integrated into the conversation flow?
- How can I further enhance the response to ensure it maintains a higher level of professionalism?
- How can I utilize user feedback to improve and refine the initial response?