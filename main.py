# import mongodb
import streamlit as st
from pymongo import MongoClient
import time

uri = "mongodb+srv://pranshuacharya:StockManagementSystem@cluster0.zmlvecl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['RealEstate']
agentCollection = db['Agent']
clientCollection = db['Client']
propertyCollection = db['Property']
AppointmentCollection = db['Appointment']


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
if 'user_name' not in st.session_state:
    st.session_state['user_name'] = None
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'bookings' not in st.session_state:
    st.session_state['bookings'] = []
if 'edit_mode' not in st.session_state:
    st.session_state['edit_mode'] = False
if 'create_account_form_values' not in st.session_state:
    st.session_state['create_account_form_values'] = {
        'user_type': None, 'name': '', 'email': '', 'new_id': ''}


def reset_user_type():
    """ Reset user type to None to show initial screen """
    st.session_state['user_type'] = None
    st.session_state['user_id'] = None
    st.session_state['authenticated'] = False
    st.session_state['edit_mode'] = False
    st.experimental_rerun()


def set_user_type(user_type):
    """ Set the type of user (Agent or Client) """
    st.session_state['user_type'] = user_type


def reset_user_type():
    """ Reset user type to None to show initial screen """
    st.session_state['user_type'] = None
    st.session_state['user_id'] = None
    st.session_state['authenticated'] = False
    st.session_state['user_name'] = None
    st.session_state['edit_mode'] = False
    st.experimental_rerun()


def authenticate_user(user_id, user_type):
    """ Check user credentials based on type """
    # Parse the user_id to int
    user_id = int(user_id)
    if user_type == "Agent":
        # Find the user_id in the database
        agent = agentCollection.find_one({"AgentId": user_id})
        if agent:
            st.session_state['user_name'] = agent['Name']
            return True
        # return user_id == "1"  # Only "1" is a valid ID for agents
    elif user_type == "Client":
        # Find the user_id in the database
        client = clientCollection.find_one({"ClientId": user_id})
        if client:
            st.session_state['user_name'] = client['Name']
            return True
        # return user_id == "1"  # Only "1" is a valid ID for clients
    return False


def login_user(user_id):
    """ Simulate a login function with different authentication for agents and clients """
    if authenticate_user(user_id, st.session_state['user_type']):
        # Get the client name from the database
        print("Authenticated")
        st.session_state['user_id'] = user_id
        st.session_state['authenticated'] = True
        st.success(
            f"Welcome {st.session_state['user_type']} : {st.session_state['user_name']}!")
    else:
        st.session_state['authenticated'] = False
        st.error("Incorrect ID. Please try again.")


def add_account(user_type, name, email, new_id):
    """ Function to create a new client or agent account """
    print("Name:", name)
    print("Email:", email)
    print("ID:", new_id)
    if user_type == "Client":
        # Insert the new client into the database
        clientCollection.insert_one(
            {"ClientId": int(new_id), "Name": name, "Email": email})
        st.success("Client account created successfully!")
    else:
        # Insert the new agent into the database
        agentCollection.insert_one(
            {"AgentId": int(new_id), "Name": name, "Email": email})
        st.success("Agent account created successfully!")
    login_user(new_id)


def handle_account_creation(user_type, name, email, new_id):
    """ Function to handle the account creation process """
    user_type = form_values['user_type']
    name = form_values['name']
    email = form_values['email']
    new_id = form_values['new_id']

    print("Name:", name)
    print("Email:", email)
    print("ID:", new_id)
    add_account(user_type, name, email, new_id)
    st.success(f"{user_type} account created successfully!")
    login_user(new_id)


def create_account(user_type):
    """ Function to create a new client or agent account """
    form_key = f"create_{user_type}_form"
    with st.form(key=form_key):
        name = st.text_input(
            "Name", value=st.session_state['create_account_form_values']['name'])
        email = st.text_input(
            "Email", value=st.session_state['create_account_form_values']['email'])
        new_id = st.text_input(
            "ID", value=st.session_state['create_account_form_values']['new_id'])
        submitted = st.form_submit_button(label="Create Account")

        st.session_state['create_account_form_values'] = {
            'user_type': user_type, 'name': name, 'email': email, 'new_id': new_id}
        time.sleep(10)
        # print create account form values
        print(st.session_state['create_account_form_values'])
        if submitted:
            handle_account_creation(
                st.session_state['create_account_form_values'])


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


# i changed this update profile

def update_profile(user_id, user_type, name, email):
    """ Update client or agent profile information in MongoDB """
    if user_type == "Agent":
        agentCollection.update_one({"AgentId": user_id}, {
                                   "$set": {"Name": name, "Email": email}})
    elif user_type == "Client":
        clientCollection.update_one({"ClientId": user_id}, {
                                    "$set": {"Name": name, "Email": email}})
    st.success("Profile updated successfully!")

# def display_user_dashboard():
#
#     if st.session_state['authenticated']:
#         if st.session_state['user_type'] == "Client":
#             st.sidebar.write(
#                 f"Welcome, {st.session_state['user_name']}")
#             cols = st.columns(3)
#
#
#             # Get list of Agents from the database
#             agents = agentCollection.find()
#
#             # Convert agents to a an array of agent id and name
#             # agents = [{"AgentId": agents["AgentId"], "Name": agents["Name"]}]
#
#             agents = {agent["AgentId"]: agent["Name"] for agent in agents}
#
#             # Get List of Properties  from the database
#             properties = propertyCollection.find()
#
#             print("HEREEEEEE", agents)
#
#             c = 0
#             for property in properties:
#
#                 with cols[c % 3]:
#                     st.image(property["img"],
#                              width=150, caption=property["Address"])
#
#                     # agents = agentCollection.find()
#                     # agent_names = [agent["Name"] for agent in agents]
#                     # agent_selected = st.selectbox("Choose an agent", agent_names, key="Name")
#                 c += 1
#
#             agent_selected = st.selectbox("Choose an agent", list(
#                 agents.values()), key=f"agent")
#             print("AGENTTTTT", agent_selected)
#             if st.button("Book Appointment", key=f"book"):
#                 book_appointment(
#                     st.session_state["user_id"], agent_selected)
#             # for idx, (property_name, property_info) in enumerate(properties.items()):
#             #     with cols[idx % 3]:
#             #         st.image(property_info["image"],
#             #                  width=150, caption=property_name)
#             #         agent_selected = st.selectbox("Choose an agent", list(
#             #             property_info["agents"].keys()), key=f"agent{idx}")
#             #         if st.button("Book Appointment", key=f"book{idx}"):
#             #             book_appointment(property_name, agent_selected)
#
#
#
#
#         elif st.session_state['user_type'] == "Agent":
#             st.sidebar.write(
#                 f"Welcome, {st.session_state['user_name']}")
#             st.subheader("Your Appointments:")
#
#             # Get all appointments from the database where the AgentId matches the current agent
#             agent_bookings = AppointmentCollection.find(
#                 {"AgentId": int(st.session_state['user_id'])})
#             # agent_bookings = [b for b in st.session_state['bookings']
#             #                   if b['agent_id'] == st.session_state['user_id']]
#             if agent_bookings:
#                 print("There are agents", agent_bookings)
#                 # Display now all the clients and convert into dictionary with client id as key and name as value
#                 clients = clientCollection.find()
#                 clients = {client["ClientId"]: client["Name"]
#                            for client in clients}
#                 for booking in agent_bookings:
#                     print(booking)
#                     st.write(
#                         f"Client ID: {booking['ClientId']} | Client Name: {clients[booking['ClientId']]} - Date: {booking['Date']}")
#             else:
#                 st.write("No appointments booked yet.")
#
#         if st.button("Logout"):
#             reset_user_type()

# i defined this new function instead of the above


def display_user_dashboard():
    """ Display user dashboard with options to edit profile, view properties, and manage appointments """
    if st.session_state['authenticated']:
        user_data = clientCollection if st.session_state['user_type'] == "Client" else agentCollection
        user_profile = user_data.find_one(
            {"AgentId" if st.session_state['user_type'] == "Agent" else "ClientId": int(st.session_state['user_id'])})

        # Edit profile section
        if st.session_state['edit_mode']:
            with st.form("profile_form"):
                print("INSIDE EDIT PROFILE")
                print(user_profile)
                new_name = st.text_input("Name", value=user_profile['Name'])
                new_email = st.text_input("Email", value=user_profile['Email'])
                if st.form_submit_button("Save Changes"):
                    update_data = {
                        "$set": {"Name": new_name, "Email": new_email}}
                    user_data.update_one(
                        {"AgentId" if st.session_state['user_type'] == "Agent" else "ClientId": int(st.session_state['user_id'])}, update_data)
                    st.session_state['edit_mode'] = False
                    st.success("Profile updated successfully!")
                    # Update the name in the session state
                    st.session_state['user_name'] = new_name
        else:
            st.sidebar.write(f"Welcome, {st.session_state['user_name']}")
            if st.sidebar.button("Edit Profile"):
                st.session_state['edit_mode'] = True
            if st.button("Logout"):
                reset_user_type()

        # Display properties and bookings for clients
        if st.session_state['user_type'] == "Client":
            cols = st.columns(3)
            agents = {agent["AgentId"]: agent["Name"]
                      for agent in agentCollection.find()}
            properties = propertyCollection.find()
            for index, property in enumerate(properties):
                with cols[index % 3]:
                    st.image(property["img"], width=150,
                             caption=property["Address"])
            agent_selected = st.selectbox(
                "Choose an agent", list(agents.values()), key=f"agent")
            if st.button("Book Appointment", key=f"book"):
                book_appointment(st.session_state["user_id"], agent_selected)

        # Display bookings for agents
        elif st.session_state['user_type'] == "Agent":
            st.subheader("Your Appointments:")
            agent_bookings = agentCollection.find(
                {"AgentId": st.session_state['user_id']})
            clients = {client["ClientId"]: client["Name"]
                       for client in clientCollection.find()}
            for booking in agent_bookings:
                st.write(
                    f"Client ID: {booking['ClientId']} | Client Name: {clients[booking['ClientId']]} - Date: {booking['Date']}")
            if not agent_bookings:
                st.write("No appointments booked yet.")


def book_appointment(client_id, agent_id):
    """ Function to book an appointment """
    # appointments = st.session_state['bookings']
    # appointments.append({'client_id': client_id, 'agent_id': agent_id})
    # st.session_state['bookings'] = appointments

    # Get Agent Id based on the agent name
    agent = agentCollection.find_one({"Name": agent_id})

    # Insert the new appointment into the database
    AppointmentCollection.insert_one(
        {"ClientId": int(client_id), "AgentId": int(agent["AgentId"]), "Date": "2021-10-10"})
    st.success("Appointment booked successfully!")


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
            st.subheader(
                f"Hello {user_type}, please login or create a new account.")
            user_id = st.text_input(f"{user_type} ID")
            if st.button('Login'):
                login_user(user_id)
            if st.button(f"Create New {user_type} Account"):
                create_account(user_type)
            st.button("Go Back", on_click=reset_user_type)
    else:
        display_user_dashboard()
