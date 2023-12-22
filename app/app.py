# Overview
# frontend app for interacting with database

# Dependencies

# app
import streamlit as st

# App

# headers
st.title("Scrolling LED Sign")

# form
with st.form("my_form", clear_on_submit=True):
    text = st.text_input("send a message")
    submitted = st.form_submit_button("Submit")

# process
