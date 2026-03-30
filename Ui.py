import streamlit as st
import requests

file = st.file_uploader("Upload file")

if file is not None:
        files = {
            "file":(file.name,file.getvalue(),file.type)
        }
        res = requests.post("http://localhost:8000/upload",files=files)
        
        if res.status_code == 200:
            st.write(res.json())
        else:
            st.write("error")