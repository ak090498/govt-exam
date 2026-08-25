import streamlit as st
import pypdf as pdf
from utility import Utility
import tempfile
import re
import os
import requests
from io import StringIO
import json
if 'clicked' not in st.session_state:
    st.session_state.clicked=False  

def click_button():
    st.session_state.clicked=True 

uploaded_file=st.file_uploader("upload file",type="pdf")

st.button('upload',on_click=click_button)
if st.session_state.clicked:
    if uploaded_file is not None:
           UPLOAD_DIR="stream_uploads"
           if not os.path.exists(UPLOAD_DIR):
                os.makedirs(UPLOAD_DIR)
           file_path=os.path.join(UPLOAD_DIR,uploaded_file.name)     
           with open(file_path,"wb") as f:
                f.write(uploaded_file.getvalue())
           with open(file_path,"rb") as f:
                response=requests.post("http://127.0.0.1:8000/upload/pdf",files={"file":f})
                if response.status_code==200:
                     st.write("your exam pdf is uploaded successfully")
                     st.write("Your questions are coming shortly")
           os.remove(file_path)          
with st.form(key="my-input"):
     text_input=st.text_input("Enter your topic")
     submitted=st.form_submit_button("ask")
     if submitted:
        response=requests.post(url="http://127.0.0.1:8000/ask",json={"query":text_input},headers={'Content-Type': 'application/json'})
        if response.status_code==200:
          response_dict=response.json()
         #print(response_dict['response']['content'])
          response_str=response_dict['response']['content']
          q_and_a_str=response_str[7:len(response_str)-3]
          json_obj = json.loads(q_and_a_str)
          for i in range(0,len(json_obj)):
               st.write(json_obj[i]['question'])
               st.write(json_obj[i]['options'])
               st.write(json_obj[i]['correct_answer'])


                  




        
    



