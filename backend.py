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
    