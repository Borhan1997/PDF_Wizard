import streamlit as st
from html_templates import bot_template, user_template, css

def render_message(message, is_bot=False):
    template = bot_template if is_bot else user_template
    st.markdown(template.replace("{{MSG}}", message), unsafe_allow_html=True)

# Apply CSS
st.markdown(css, unsafe_allow_html=True)

# Example usage
st.title("Chatbot Example")
render_message("Hello, I am the chatbot!", is_bot=True)
render_message("Hi, I am the user!", is_bot=False)
