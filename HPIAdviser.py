# Import libraries
import streamlit as st
import openai
from google.oauth2 import service_account
from gsheetsdb import connect
import pandas as pd
from pandas import DataFrame
import numpy as np
import sub_processes
from sub_processes import get_response, modify_response

# Get_keywords_from_GoogleSheet() & Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets",],)
conn = connect(credentials=credentials)

# Perform SQL query on the Google Sheet. Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows
sheet_url = st.secrets["private_gsheets_url"] # Links tab in Google Sheet
rows = run_query(f'SELECT * FROM "{sheet_url}"')
sheet_url_config = st.secrets["private_gsheets_url_config"] # Links tab in Google Sheet
app_config = run_query(f'SELECT * FROM "{sheet_url_config}"')

# Get User Input, modify and write responseopenai.api_key = st.secrets["api_key"]
st.title(app_config[1][1])                   # 1) Title
user_input = st.text_input(app_config[2][1]) # 2) Prompt
st.caption(app_config[3][1])                 # 3) Caption below prompt
user_input = app_config[4][1] + " " + user_input # 4) Add relevant Keyword in front of user-input
response = get_response(user_input)  
response = modify_response(response, rows)
st.write("Response: ", response)
st.write(app_config[5][1])                # 5) BottomMessage
st.caption(app_config[6][1])              # 6) Disclaimer
