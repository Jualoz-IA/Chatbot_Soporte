import streamlit as st

# Crear páginas
""" TODO: Hacer el tema de login, que se muestren ciertas  """

chat_page = st.Page("components/chat.py", title="ChatBot", icon=":material/smart_toy:")
colletions_page = st.Page("components/collections.py", title="Collections", icon=":material/smart_toy:")
doc_gestion_page = st.Page("components/doc-gestion.py", title="Documents Gestion", icon=":material/ar_on_you:")
parameters_page = st.Page("components/parameters.py", title="Models Parameters", icon=":material/multiple_stop:")
user_gestion_page = st.Page("components/user-gestion.py", title="User Gestion", icon=":material/ar_on_you:")

""" Sera un modal """
login_page = st.Page("components/login.py", title="Login", icon=":material/multiple_stop:") 

st.set_page_config(page_title="Chatbot", page_icon=":material/business_messages:")