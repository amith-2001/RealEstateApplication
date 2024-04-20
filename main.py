import streamlit as st

# Initialize session state if not already set
if 'user_type' not in st.session_state:
    st.session_state['user_type'] = None
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None

def set_user_type(user_type):
    """ Set the type of user (Agent or Client) """
    st.session_state['user_type'] = user_type

def reset_user_type():
    """ Reset user type to None to show initial screen """
    st.session_state['user_type'] = None

def login_user():
    """ Simulate a login function """
    user_id = st.session_state['user_id']
    user_type = st.session_state['user_type']
    st.success(f"Welcome {user_type} with ID {user_id}!")

def create_account(user_type):
    """ Placeholder for account creation """
    st.info(f"Create an account for a {user_type}. (Functionality to be implemented)")

# Custom CSS to center content and style the app
st.markdown("""
    <style>
    .main {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .block-container {
        padding-top: 5rem;
    }
    .stButton>button {
        width: 100%;
        padding: 0.5rem;
        margin-top: 0.5rem;
    }
    .stTextInput>div>div>input {
        margin-top: -1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Page title
st.title('Real Estate Management System')

# Center content based on user selection
with st.container():
    if st.session_state['user_type'] is None:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.button("Agent", on_click=set_user_type, args=('Agent',))
            st.button("Client", on_click=set_user_type, args=('Client',))
    else:
        user_type = st.session_state['user_type']
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.subheader(f"Hello {user_type}, please login or create a new account.")
            user_id = st.text_input(f"{user_type} ID", key="user_id")
            st.button('Login', on_click=login_user)
            st.button(f"Create New {user_type} Account", on_click=lambda: create_account(user_type))
            st.button("Go Back", on_click=reset_user_type)
