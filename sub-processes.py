import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect
import openai
import re

# Get response from openAI
def get_response(user_input):
  response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=user_input,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
    ).choices[0].text
  return response

# Modify response to add hyperlinks for selected keywords
def modify_response(response, rows):
  # Replace Strings, ignoring case
  for i in range(0, len(rows)):
        to_replace = rows[i][0] # first is row = i, second is column, 0 = Keywords to replace, 1 = Links
        replace_with = "[" + rows[i][0] + "](" + rows[i][1] + ")"
        compiled = re.compile(re.escape(to_replace), re.IGNORECASE)
        response = compiled.sub(replace_with, response)
  return response
