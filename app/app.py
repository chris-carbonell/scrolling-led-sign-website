# Overview
# frontend app for interacting with database

# Dependencies

# general
from datetime import datetime
import math
import os
import time

# data
import pandas as pd

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

async def insert_code(code: str):
    '''
    insert code into codes
    '''
    async with AsyncPostgrestClient(URL_API) as client:
        client.auth(token = os.environ['SERVER_JWT_TOKEN'])
        data = {
            'dt_entered': datetime.now().isoformat(),
            'code': code,
            'is_admin': False,
        }
        await client.from_("codes").insert(data).execute()

async def insert_text(name: str, text: str):
    '''
    insert text into texts
    '''
    async with AsyncPostgrestClient(URL_API) as client:
        client.auth(token = os.environ['SERVER_JWT_TOKEN'])
        data = {
            'dt_entered': datetime.now().isoformat(),
            'name': name,
            'text': text,
        }
        await client.from_("texts").insert(data).execute()

async def delete_code(code: str):
    '''
    delete code from codes
    '''
    async with AsyncPostgrestClient(URL_API) as client:
        client.auth(token = os.environ['SERVER_JWT_TOKEN'])
        await client.from_("codes").delete().eq("code", code).execute()

async def get_data(table: str, query: str = None):
    '''
    get data
    '''
    async with AsyncPostgrestClient(URL_API) as client:
        
        # get builder
        builder = client.from_(table).select("*")

        # parse query
        # for example:
        # query = "text_id=gt.2&name=eq.carbo"
        # ("text_id", "gt.2") and ("name", "eq.carbo") get added to builder params
        # as of 2024-01, this functionality isn't exposed in the higher levels of `postgrest-py`
        # https://pydoc.dev/httpx/latest/httpx.QueryParams.html
        # https://github.com/supabase-community/postgrest-py/blob/fb0b8c2590a3d53f67c84e9f52917768a13d7153/postgrest/_async/request_builder.py#L28
        if query != "":
            for q in query.split("&"):
                try:
                    key, val = q.split("=")
                    builder.params = builder.params.add(key, val)
                except Exception as e:
                    st.error(f"cannot parse query: {q}")
                    st.error(e)
                    pass
        
        # execute
        r = await builder.execute()
        res = r.data  # e.g., [{'code': 'some_code', 'is_admin': True}]

    return pd.DataFrame.from_records(res)

def split_frame(input_df, rows):
    '''
    split df based on row count (i.e., batch size)

    source: https://medium.com/streamlit/paginating-dataframes-with-streamlit-2da29b080920
    '''
    df = [input_df.loc[i : i + rows - 1, :] for i in range(0, len(input_df), rows)]
    return df

def get_paginated_table(table: str):
    '''
    build table with pagination
    '''

    def _get_key(id: str):
        '''
        create key based on the table
        to help differentiate this paginated table from other paginated tables
        '''
        return f"{table}_{id}"

    paginated_table = st.container()

    paginated_table.subheader(table)

    # top menu
    # query params
    query_params = paginated_table.text_input(
        label="PostgREST query params",
        value="",
        key=_get_key("text_input"),
    )
    paginated_table.caption("e.g., `text_id=gt.2&name=eq.carbo&dt_entered=gte.2024-01-02`")
    paginated_table.caption("https://postgrest.org/en/stable/references/api/tables_views.html")

    # get data
    data = asyncio.run(get_data(table, query_params))
    
    # bottom menu
    # pagination
    bottom_menu = st.columns((4, 1, 1))
    with bottom_menu[2]:
        batch_size = st.selectbox("Page Size", options=[5, 10, 20], key=_get_key("selectbox"))
    with bottom_menu[1]:
        total_pages = math.ceil(len(data) / batch_size)
        current_page = st.number_input(
            "Page", min_value=1, max_value=total_pages, step=1,
            key=_get_key("number_input"),
        )
    with bottom_menu[0]:
        st.markdown(f"Page **{current_page}** of **{total_pages}** ")

    pages = split_frame(data, batch_size)
    paginated_table.dataframe(data=pages[current_page - 1], use_container_width=True, hide_index=True)

    return paginated_table

# App

# set up

# set title in tab
st.set_page_config(page_title=os.environ['DOMAIN'])

# hide 3 dots
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# headers

header = st.columns(2)
with header[0]:
    st.title(os.environ['DOMAIN'])  # title
with header[1]:
    st.image(get_gif(os.environ['APP_MAIN_GIFS'].split(",")))  # welcome gif

st.header("Scrolling LED Sign")

# initialize
if 'access_granted' not in st.session_state:
    st.session_state['access_granted'] = False  # True = access granted, False = no access
    st.session_state['access_code'] = None  # what access code did they try?
    st.session_state['access_tries'] = 0  # how many times did they hit the submit button on the access form?
    st.session_state['access_granted_admin'] = False  # True = admin access granted, False = no admin access

# access denied
if not st.session_state['access_granted']:
    
    # access code form
    st.header("Access")
    with st.form("form_access", clear_on_submit=True):
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
    st.header("Send Message")
    with st.form("form_text", clear_on_submit=True):
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
if st.session_state['access_granted_admin']:

    # Data
    # paginated tables
    st.header("Data")
    texts_table = get_paginated_table("texts")
    codes_table = get_paginated_table("codes")

    # Code Management
    
    st.header("Code Management")

    with st.form("form_code_management", clear_on_submit=True):
        radio_form_code_management = st.radio("add or delete", options=["add", "delete"])
        code_form_code_management = st.text_input("code")
        submitted_form_code_management = st.form_submit_button("Submit")

    if submitted_form_code_management:
        if radio_form_code_management == "add":
            asyncio.run(insert_code(code_form_code_management))
        elif radio_form_code_management == "delete":
            # prevent deletion of admin code
            if code_form_code_management != os.environ['APP_ADMIN_PASSWORD']:
                asyncio.run(delete_code(code_form_code_management))
        else:
            pass