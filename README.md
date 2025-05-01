# PDF Wizard
Hello, I'm trying to build a python chatbot using langchain and streamlit, that answers questions related to attached pdf documents. The code is composed of 2 python files only : "app.py" and "backend.py".
Here is the code of "app.py":
<<<
import streamlit as st 
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from backend import Processing

def handle_user_input(question):
    response = st.session_state.conversation({'question': question})
    st.session_state.chat_history = response['chat_history']

    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)
        else:
            with st.chat_message("AI"):
                st.markdown(message.content)

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with Multiple PDFs", page_icon=":books:")
    st.header("Chat with multiple PDFs :books:")
    user_question = st.chat_input("Ask a question about your documents:")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    # Answering the new question
    if user_question is not None and user_question != "":
        handle_user_input(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        
        if st.button("Process"):
            with st.spinner("Processing"):
                # Create Conversation Chain
                st.session_state.conversation = Processing().get_conversation_chain(pdf_docs)

if __name__ == "__main__":
    main()
>>>
and here is the code of "backend.py":
<<<
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import HuggingFaceHub

class Processing():
    def get_pdf_text(self,docs):
        """
        Extract the text from all the documents attached
        Returns a raw text
        """
        text = ""
        for pdf in docs:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                text += page.extract_text()

        return text

    def get_text_chunks(self,text):
        """
        Get the text chunks from the raw text
        Returns a list of chunks
        """
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        return chunks

    def get_vector_store(self,chunks):
        """
        Create the Vector Store
        """
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_texts(texts=chunks, embedding=embeddings)
        return vector_store

    def get_conversation_chain(self,docs):
        """
        Create Conversation Memory
        """
        # Get the pdf text
        raw_text = self.get_pdf_text(docs)

        # Get the text chunks
        text_chunks = self.get_text_chunks(raw_text)

        # Create Vector Store
        vector_store = self.get_vector_store(text_chunks)

        llm = ChatOpenAI()

        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm = llm,
            retriever=vector_store.as_retriever(),
            memory = memory
        )
        return conversation_chain
>>>
Also, I'm getting the following warning when I run the App :
"""
/workspaces/PDF_Wizard/backend.py:61: LangChainDeprecationWarning: Please see the migration guide at: https://python.langchain.com/docs/versions/migrating_memory/
  memory = ConversationBufferMemory(
/workspaces/PDF_Wizard/app.py:7: LangChainDeprecationWarning: The method `Chain.__call__` was deprecated in langchain 0.1.0 and will be removed in 1.0. Use :meth:`~invoke` instead.
  response = st.session_state.conversation({'question': question})
"""
I want the answer of the chatbot to be streamed and to not appear all at once. Can you fix both issues please ?
