# app.py
import streamlit as st
from user_interface import user_type_selection, user_login_and_creation

st.title('Real Estate Management System')

user_type_selection()
user_login_and_creation()
