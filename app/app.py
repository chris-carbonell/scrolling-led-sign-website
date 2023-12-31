# Overview
# frontend app for interacting with database

# Dependencies

# general
import time

# app
import streamlit as st

# api
import requests

# constants
from constants import *

# Funcs

def insert_text(text: str):
    '''
    insert text into db
    '''
    
    # post
    r = requests.put(URL_API + "/text", params = {'text': text})

    # get
    params = {
        'requested': False,
        'asc': False,
        'limit': 10
    }
    r = requests.get(URL_API + "/texts", params = params)

# App

# headers
st.title("Scrolling LED Sign")

# initialize
if 'access_granted' not in st.session_state:
    st.session_state['access_granted'] = False  # True = access granted, False = no access
    st.session_state['access_code'] = None  # what access code did they try?
    st.session_state['access_tries'] = 0  # how many times did they hit the submit button on the access form?

# access denied
if not st.session_state['access_granted']:
    
    # access code form
    with st.form("form_access", clear_on_submit=True):
        st.title("Access")
        name = st.text_input("your name")
        st.session_state['access_code'] = st.text_input("access code")
        submitted = st.form_submit_button("Submit")

    # give feedback on access code
    if submitted:
        if st.session_state['access_code'] in ACCESS_CODE_WHITELIST:
            st.session_state['access_granted'] = True  # grant access
            st.success(f"welcome, {name}!")  # welcome message
            time.sleep(1)  # wait so user can read the welcome message
            st.rerun()  # rerun so we can show the input form
        else:
            st.error("access denied")

# access granted
if st.session_state['access_granted']:
    
    # get input text
    with st.form("form_text", clear_on_submit=True):
        st.title("Send Message")
        text = st.text_input("send a message")
        submitted = st.form_submit_button("Submit")

    if submitted:
        insert_text(text)