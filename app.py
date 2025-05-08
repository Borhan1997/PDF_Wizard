import streamlit as st 
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from backend import Processing
from stream_handler import StreamHandler

def handle_user_input(question):
    with st.chat_message("Human"):
        st.markdown(question)
    with st.chat_message("AI"):
        stream_handler = StreamHandler(st.empty())
        response = st.session_state.conversation.invoke(
                {'question': question},
                config = {"callbacks": [stream_handler]}
        )
    st.session_state.chat_history.append(HumanMessage(content=question))
    st.session_state.chat_history.append(AIMessage(content=stream_handler.final_answer))

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with Multiple PDFs", page_icon=":books:")
    st.title("PDF Wizard :male_mage:")
    st.subheader("Your solution to chat with multiple PDFs :books:")

    if "openai_key" not in st.session_state:
        st.session_state.openai_key = None

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)
        else:
            with st.chat_message("AI"):
                st.markdown(message.content)

    user_question = st.chat_input("Ask a question about your documents:")
    # Answering the new question
    if user_question is not None and user_question != "":
        handle_user_input(user_question)

    with st.sidebar:
        st.header("API Keys")
        openai_key = st.text_input("Enter your OpenAI API key:", type="password")
        if openai_key:
            st.session_state.openai_key = openai_key
            st.success("API key saved!")

            # Add the file uploader once the user enters his API Key
            st.subheader("Your documents")
            pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
            if st.button("Process"):
                with st.spinner("Processing"):
                    # Create Conversation Chain
                    st.session_state.conversation = Processing().get_conversation_chain(pdf_docs)
                    
        else:
            st.warning("Please enter your OpenAI API key to proceed.")



if __name__ == "__main__":
    main()