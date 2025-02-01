import streamlit as st
from google_auth_st import add_auth

add_auth(login_sidebar = False)

#after authentication, the email is stored in session state
st.write(st.session_state.email)
