# user_interface.py
import streamlit as st
from authentication import login_user, create_account

def user_type_selection():
    if 'user_type' not in st.session_state:
        st.session_state['user_type'] = None
    if st.session_state['user_type'] is None:
        if st.button("Agent"):
            st.session_state['user_type'] = 'Agent'
        if st.button("Client"):
            st.session_state['user_type'] = 'Client'

def user_login_and_creation():
    if st.session_state['user_type']:
        user_type = st.session_state['user_type']
        st.write(f"Hello {user_type}, please login or create a new account.")
        user_id = st.text_input(f"{user_type} ID", key="user_id")

        if st.button('Login'):
            message = login_user(user_id, user_type)
            st.success(message)

        if st.button(f"Create New {user_type} Account"):
            message = create_account(user_type)
            st.success(message)
