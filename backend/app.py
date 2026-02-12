import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.set_page_config(page_title="Medanta Admin", page_icon="🏥")

st.title("🏥 Medanta Induction Dashboard")

# Login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == "admin" and pwd == "medanta2024":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Wrong password!")
else:
    st.success("Welcome Admin!")
    st.write("No data yet. This is a test.")
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
