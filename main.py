import streamlit as st

# Example data
clients = {"101": "Alice", "102": "Bob"}
agents = {"201": "Agent X", "202": "Agent Y"}
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
if 'bookings' not in st.session_state:
    st.session_state['bookings'] = []

def set_user_type(user_type):
    """ Set the type of user (Agent or Client) """
    st.session_state['user_type'] = user_type
    st.session_state['user_id'] = None  # Reset user_id whenever user type is set

def reset_user_type():
    """ Reset user type to None to show initial screen """
    st.session_state['user_type'] = None
    st.session_state['user_id'] = None

def login_user():
    """ Simulate a login function """
    user_id = st.session_state['user_id']
    user_type = st.session_state['user_type']
    if user_id in clients or user_id in agents:
        st.success(f"Welcome {user_type} with ID {user_id}!")
    else:
        st.error("Invalid ID. Please try again.")

def create_account(user_type):
    """ Placeholder for account creation """
    st.info(f"Create an account for a {user_type}. (Functionality to be implemented)")

def book_appointment(property_name, agent_id):
    """ Book an appointment with an agent for a property """
    booking_info = {
        'client_id': st.session_state['user_id'],
        'agent_id': agent_id,
        'property_name': property_name
    }
    st.session_state['bookings'].append(booking_info)
    st.success(f"Appointment booked with {agents[agent_id]} for {property_name}")

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
    elif st.session_state['user_id'] is None:
        user_type = st.session_state['user_type']
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.subheader(f"Hello {user_type}, please login or create a new account.")
            user_id = st.text_input(f"{user_type} ID", key="user_id")
            st.button('Login', on_click=login_user)
            st.button(f"Create New {user_type} Account", on_click=lambda: create_account(user_type))
            st.button("Go Back", on_click=reset_user_type)
    else:
        if st.session_state['user_type'] == "Client":
            st.sidebar.write(f"Welcome, {clients.get(st.session_state['user_id'], 'Unknown Client')}")
            cols = st.columns(3)
            for idx, (property_name, property_info) in enumerate(properties.items()):
                with cols[idx % 3]:
                    st.image(property_info["image"], width=150, caption=property_name)
                    agent_selected = st.selectbox("Choose an agent", list(property_info["agents"].keys()), key=f"agent{idx}")
                    if st.button("Book Appointment", key=f"book{idx}"):
                        book_appointment(property_name, agent_selected)
        elif st.session_state['user_type'] == "Agent":
            st.sidebar.write(f"Welcome, {agents.get(st.session_state['user_id'], 'Unknown Agent')}")
            st.subheader("Your Appointments:")
            agent_bookings = [b for b in st.session_state['bookings'] if b['agent_id'] == st.session_state['user_id']]
            if agent_bookings:
                for booking in agent_bookings:
                    st.write(f"Client ID: {booking['client_id']} - Property: {booking['property_name']}")
            else:
                st.write("No appointments booked yet.")
