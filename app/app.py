# Overview
# frontend app for interacting with database

# Dependencies

# general
from datetime import datetime
import time

# app
import streamlit as st

# api
import asyncio
from postgrest import AsyncPostgrestClient

# constants
from constants import *

# Funcs

async def insert_text(text: str):
    '''
    insert text into db
    '''

    # get
    # async with AsyncPostgrestClient(URL_API) as client:
    #     # client.auth(token = os.environ['SERVER_JWT_TOKEN'])
    #     r = await client.from_("texts").select("*").execute()
    #     res = r.data
    # st.write(res)

    # put
    async with AsyncPostgrestClient(URL_API) as client:
        client.auth(token = os.environ['SERVER_JWT_TOKEN'])
        await client.from_("texts").insert({ "text": text }).execute()

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
        # insert_text(text)
        asyncio.run(insert_text(text))