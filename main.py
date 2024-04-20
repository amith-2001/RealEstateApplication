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
if 'edit_mode' not in st.session_state:
    st.session_state['edit_mode'] = False

def set_user_type(user_type):
    """ Set the type of user (Agent or Client) """
    st.session_state['user_type'] = user_type

def reset_user_type():
    """ Reset user type to None to show initial screen """
    st.session_state['user_type'] = None
    st.session_state['user_id'] = None
    st.session_state['authenticated'] = False
    st.session_state['edit_mode'] = False
    st.experimental_rerun()

def authenticate_user(user_id, user_type):
    """ Check user credentials based on type """
    if user_type == "Agent":
        return user_id in agents
    elif user_type == "Client":
        return user_id in clients
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

def update_profile(user_id, user_type, name, email):
    """ Update client or agent profile information """
    if user_type == "Client":
        clients[user_id]['name'] = name
        clients[user_id]['email'] = email
    else:
        agents[user_id]['name'] = name
        agents[user_id]['email'] = email
    st.success("Profile updated successfully!")


def book_appointment(property_name, agent_id):
    """ Book an appointment with an agent for a property """
    booking_info = {
        'client_id': st.session_state['user_id'],
        'agent_id': agent_id,
        'property_name': property_name
    }
    st.session_state['bookings'].append(booking_info)
    st.success(f"Appointment booked with {agents[agent_id]['name']} for {property_name}")

def display_user_dashboard():
    """ Display user dashboard with profile and booking information """
    user_data = clients if st.session_state['user_type'] == "Client" else agents
    user_info = user_data.get(st.session_state['user_id'], {})
    if st.session_state['edit_mode']:
        with st.form("profile_form"):
            name = st.text_input("Name", value=user_info['name'])
            email = st.text_input("Email", value=user_info['email'])
            submit_button = st.form_submit_button("Save Changes")
            if submit_button:
                update_profile(st.session_state['user_id'], st.session_state['user_type'], name, email)
                st.session_state['edit_mode'] = False
    else:
        st.sidebar.write(f"Welcome, {user_info.get('name', 'Unknown User')}")
        if st.sidebar.button("Edit Profile"):
            st.session_state['edit_mode'] = True
        if st.sidebar.button("Logout"):
            reset_user_type()
        # Display additional dashboard components like properties or bookings
        if st.session_state['user_type'] == "Client":
            cols = st.columns(3)
            for idx, (property_name, property_info) in enumerate(properties.items()):
                with cols[idx % 3]:
                    st.image(property_info["image"], width=150, caption=property_name)
                    agent_selected = st.selectbox("Choose an agent", list(property_info["agents"].keys()), key=f"agent{idx}")
                    if st.button("Book Appointment", key=f"book{idx}"):
                        book_appointment(property_name, agent_selected)
        elif st.session_state['user_type'] == "Agent":
            st.subheader("Your Appointments:")
            agent_bookings = [b for b in st.session_state['bookings'] if b['agent_id'] == st.session_state['user_id']]
            if agent_bookings:
                for booking in agent_bookings:
                    st.write(f"Client ID: {booking['client_id']} - Property: {booking['property_name']}")

# CSS styles
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

<<<<<<< Updated upstream
=======

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

        print(user_profile)

        # Edit profile section
        if st.session_state['edit_mode']:
            with st.form("profile_form"):
                new_name = st.text_input("Name", value=user_profile['Name'])
                new_email = st.text_input(
                    "Email", value=user_profile['Email'])
                if st.form_submit_button("Save Changes"):
                    update_data = {"$set": {"Name": new_name,
                                            "Email": new_email}}
                    user_data.update_one({"AgentId" if st.session_state['user_type'] == "Agent" else "ClientId": int(
                        st.session_state['user_id'])}, update_data)
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
            agent_bookings = AppointmentCollection.find(
                {"AgentId": int(st.session_state['user_id'])})
            clients = {client["ClientId"]: client["Name"]
                       for client in clientCollection.find()}
            for booking in agent_bookings:
                cols = st.columns([1, 2, 1])
                with cols[1]:
                    st.write(
                        f"Client ID: {booking['ClientId']} | Client Name: {clients[booking['ClientId']]} - Date: {booking['Date']}")
                with cols[2]:
                    if st.button(f"Delete Booking {booking['_id']}", key=str(booking['_id'])):
                        AppointmentCollection.delete_one(
                            {"_id": booking['_id']})
                        st.success(
                            f"Booking with ID {booking['_id']} deleted successfully.")
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


>>>>>>> Stashed changes
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
            # if st.button(f"Create New {user_type} Account"):
            #     create_account(user_type)
            st.button("Go Back", on_click=reset_user_type)
    else:
        display_user_dashboard()
