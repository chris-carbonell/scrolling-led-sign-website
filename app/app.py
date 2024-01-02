# Overview
# frontend app for interacting with database

# Dependencies

# general
from datetime import datetime
import os
import time

# app
import streamlit as st

# api
import asyncio
from postgrest import AsyncPostgrestClient

# giphy
from giphy import get_gif

# constants
from constants import *

# Funcs

async def get_codes():
    '''
    get valid access codes
    '''
    async with AsyncPostgrestClient(URL_API) as client:
        r = await client.from_("codes").select("code", "is_admin").execute()
        res = r.data  # e.g., [{'code': 'some_code', 'is_admin': True}]

    return {d['code']: d['is_admin'] for d in res}

async def insert_text(name: str, text: str):
    '''
    insert text into db
    '''
    async with AsyncPostgrestClient(URL_API) as client:
        client.auth(token = os.environ['SERVER_JWT_TOKEN'])
        data = {
            'name': name,
            'text': text,
        }
        await client.from_("texts").insert(data).execute()

# App

# set up

# set title in tab
st.set_page_config(page_title=os.environ['DOMAIN'])

# hide 3 dots
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# headers
st.title(os.environ['DOMAIN'])
st.header("Scrolling LED Sign")

# welcome gif
st.image(get_gif(os.environ['APP_MAIN_GIFS'].split(",")))

# initialize
if 'access_granted' not in st.session_state:
    st.session_state['access_granted'] = False  # True = access granted, False = no access
    st.session_state['access_code'] = None  # what access code did they try?
    st.session_state['access_tries'] = 0  # how many times did they hit the submit button on the access form?
    st.session_state['access_granted_admin'] = False  # True = admin access granted, False = no admin access

# access denied
if not st.session_state['access_granted']:
    
    # access code form
    with st.form("form_access", clear_on_submit=True):
        st.header("Access")
        st.session_state['name'] = st.text_input("your name")
        st.session_state['access_code'] = st.text_input("access code")
        submitted = st.form_submit_button("Submit")

    # give feedback on access code
    if submitted:
        codes = asyncio.run(get_codes())
        if st.session_state['access_code'] in codes:
            st.session_state['access_granted'] = True  # grant access
            st.session_state['access_granted_admin'] = codes[st.session_state['access_code']]  # grant admin access if applicable
            st.success(f"welcome, {st.session_state['name']}!")  # welcome message
            time.sleep(1)  # wait so user can read the welcome message
            st.rerun()  # rerun so we can show the input form
        else:
            st.error("access denied")

# access granted
if st.session_state['access_granted']:
    
    # get input text
    with st.form("form_text", clear_on_submit=True):
        st.header("Send Message")
        text = st.text_input("send a message")
        submitted = st.form_submit_button("Submit")

    if submitted:
        asyncio.run(insert_text(st.session_state['name'], text))
        st.success(f"text successfully submitted!")
        st.image(get_gif([
            "success",
            "accomplishment",
            "achievement",
            "victory",
            "win",
            "yes",
            "boom",
        ]))

# admin access