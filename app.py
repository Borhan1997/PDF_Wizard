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