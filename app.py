import streamlit as st 
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import HuggingFaceHub
from html_templates import css, bot_template, user_template
from backend import Processing

def handle_user_input(question):
    response = st.session_state.conversation({'question': question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.markdown(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.markdown(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with Multiple PDFs", page_icon=":books:")

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_user_input(user_question)

    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    with st.sidebar:
        st.subheader("Your documents")
        
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        
        if st.button("Process"):
            with st.spinner("Processing"):
                # Get the pdf text
                raw_text = Processing().get_pdf_text(pdf_docs)

                # Get the text chunks
                text_chunks = Processing().get_text_chunks(raw_text)

                # Create Vector Store
                vector_store = Processing().get_vector_store(text_chunks)

                # Create Conversation Chain
                st.session_state.conversation = Processing().get_conversation_chain(vector_store)

if __name__ == "__main__":
    main()