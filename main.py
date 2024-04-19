import streamlit as st

# Placeholder to keep user state during the session
if 'user_type' not in st.session_state:
    st.session_state['user_type'] = None
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None

def set_user_type(user_type):
    st.session_state['user_type'] = user_type

def login_user():
    user_id = st.session_state['user_id']
    user_type = st.session_state['user_type']
    # Here you would add your logic to verify the user ID
    st.write(f"Welcome {user_type} with ID {user_id}!")

def create_account(user_type):
    st.write(f"Create an account for a {user_type}.")
    # Here you would add forms to gather details to create a new account

st.title('Real Estate Management System')

# Ask user if they are an agent or a client
if st.session_state['user_type'] is None:
    st.button("Agent", on_click=set_user_type, args=('Agent',))
    st.button("Client", on_click=set_user_type, args=('Client',))

elif st.session_state['user_type'] == 'Agent' or st.session_state['user_type'] == 'Client':
    user_type = st.session_state['user_type']
    st.write(f"Hello {user_type}, please login or create a new account.")

    user_id = st.text_input(f"{user_type} ID", key="user_id")

    if st.button('Login'):
        login_user()

    if st.button(f"Create New {user_type} Account"):
        create_account(user_type)
