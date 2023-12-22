# Overview
# frontend app for interacting with database

# Dependencies

# app
import streamlit as st

# api
import requests

# constants
from constants import *

# App

# headers
st.title("Scrolling LED Sign")

# form
with st.form("my_form", clear_on_submit=True):
    text = st.text_input("send a message")
    submitted = st.form_submit_button("Submit")

# process

if submitted:

    ## post
    r = requests.put(URL_API + "/text", params = {'text': text})

    ## get
    params = {
        'requested': False,
        'asc': False,
        'limit': 10
    }
    r = requests.get(URL_API + "/texts", params = params)
    st.write(r.url)
    st.write(r.json())