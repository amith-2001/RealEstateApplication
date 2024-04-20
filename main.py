import streamlit as st

# Example data storage for demo purposes
clients = {"1": {"name": "Alice", "email": "alice@example.com"}}
agents = {"1": {"name": "Agent X", "email": "agentx@example.com"}}
properties = {
    "Property 1": {"image": "https://via.placeholder.com/150", "agents": agents},
    "Property 2": {"image": "https://via.placeholder.com/150", "agents": agents},
    "Property 3": {"image": "https://via.placeholder.com/150", "agents": agents},
}

# Initialize session state if not already set
if 'user_type' not in st.session_state:
    st.session_state['user_type'] = None
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'bookings' not in st.session_state:
    st.session_state['bookings'] = []

def set_user_type(user_type):
    """ Set the type of user (Agent or Client) """
    st.session_state['user_type'] = user_type

def reset_user_type():
    """ Reset user type to None to show initial screen """
    st.session_state['user_type'] = None
    st.session_state['user_id'] = None
    st.session_state['authenticated'] = False

def authenticate_user(user_id, user_type):
    """ Check user credentials based on type """
    if user_type == "Agent":
        return user_id == "1"  # Only "1" is a valid ID for agents
    elif user_type == "Client":
        return user_id == "1"  # Only "1" is a valid ID for clients
    return False

def login_user(user_id):
    """ Simulate a login function with different authentication for agents and clients """
    if authenticate_user(user_id, st.session_state['user_type']):
        st.session_state['user_id'] = user_id
        st.session_state['authenticated'] = True
        st.success(f"Welcome {st.session_state['user_type']} with ID {user_id}!")
    else:
        st.session_state['authenticated'] = False
        st.error("Incorrect ID. Please try again.")

def create_account(user_type):
    """ Function to create a new client or agent account """
    with st.form(key=f"create_{user_type}_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        new_id = st.text_input("ID")
        submit_button = st.form_submit_button(label="Create Account")
        if submit_button:
            if user_type == "Client":
                clients[new_id] = {'name': name, 'email': email}
                st.success("Client account created successfully!")
            else:
                agents[new_id] = {'name': name, 'email': email}
                st.success("Agent account created successfully!")
            login_user(new_id)

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

st.title('Real Estate Management System')

def display_user_dashboard():
    if st.session_state['authenticated']:
        if st.session_state['user_type'] == "Client":
            st.sidebar.write(f"Welcome, {clients.get(st.session_state['user_id'], {}).get('name', 'Unknown Client')}")
            cols = st.columns(3)
            for idx, (property_name, property_info) in enumerate(properties.items()):
                with cols[idx % 3]:
                    st.image(property_info["image"], width=150, caption=property_name)
                    agent_selected = st.selectbox("Choose an agent", list(property_info["agents"].keys()), key=f"agent{idx}")
                    if st.button("Book Appointment", key=f"book{idx}"):
                        book_appointment(property_name, agent_selected)
        elif st.session_state['user_type'] == "Agent":
            st.sidebar.write(f"Welcome, {agents.get(st.session_state['user_id'], {}).get('name', 'Unknown Agent')}")
            st.subheader("Your Appointments:")
            agent_bookings = [b for b in st.session_state['bookings'] if b['agent_id'] == st.session_state['user_id']]
            if agent_bookings:
                for booking in agent_bookings:
                    st.write(f"Client ID: {booking['client_id']} - Property: {booking['property_name']}")
            else:
                st.write("No appointments booked yet.")

# Center content based on user selection
with st.container():
    if st.session_state['user_type'] is None:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.button("Agent", on_click=set_user_type, args=('Agent',))
            st.button("Client", on_click=set_user_type, args=('Client',))
    elif not st.session_state['authenticated']:
        user_type = st.session_state['user_type']
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.subheader(f"Hello {user_type}, please login or create a new account.")
            user_id = st.text_input(f"{user_type} ID")
            if st.button('Login'):
                login_user(user_id)
            if st.button(f"Create New {user_type} Account"):
                create_account(user_type)
            st.button("Go Back", on_click=reset_user_type)
    else:
        display_user_dashboard()

