import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="Medanta Admin", page_icon="🏥", layout="wide")

st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: bold; color: #8B1538; text-align: center; }
    .stButton>button { background-color: #8B1538; color: white; }
</style>
""", unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state.auth = False
if 'data' not in st.session_state: st.session_state.data = []

DATA_FILE = "submissions.json"
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f: return json.load(f)
    return []

if not st.session_state.data: st.session_state.data = load_data()

def login():
    st.markdown('<h1 class="main-header">🏥 Medanta Admin Dashboard</h1>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        if st.text_input("User") == "admin" and st.text_input("Pass", type="password") == "medanta2024":
            st.session_state.auth = True
            st.rerun()
        elif st.button("Login"): st.error("Wrong!")

def dashboard():
    st.markdown('<h1 class="main-header">🏥 Medanta Admin Dashboard</h1>', unsafe_allow_html=True)
    with st.sidebar:
        p = st.radio("Menu", ["📊 Stats", "👥 Data", "💾 Export"])
        st.info(f"Total: {len(st.session_state.data)}")
        if st.button("Logout"): st.session_state.auth = False; st.rerun()
    
    d = st.session_state.data
    if not d: st.warning("No data yet!"); return
    
    if p == "📊 Stats":
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total", len(d))
        c2.metric("Depts", len(set(x.get('dept','') for x in d)))
        c3.metric("Today", len([x for x in d if datetime.now().strftime('%Y-%m-%d') in x.get('time','')]))
        scores = [x.get('score',0) for x in d if x.get('score')]
        c4.metric("Avg", f"{sum(scores)/len(scores):.1f}%" if scores else "0%")
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            depts = {}
            for x in d: depts[x.get('dept','Unknown')] = depts.get(x.get('dept','Unknown'),0)+1
            st.plotly_chart(px.pie(values=list(depts.values()), names=list(depts.keys()), color_discrete_sequence=['#8B1538','#C41E3A']), use_container_width=True)
        with col2:
            st.markdown("#### Recent")
            for x in sorted(d, key=lambda x: x.get('time',''), reverse=True)[:5]:
                st.write(f"• {x.get('name','N/A')} - {x.get('dept','N/A')}")
    
    elif p == "👥 Data":
        st.dataframe(pd.DataFrame(d), use_container_width=True)
    
    else:
        df = pd.DataFrame(d)
        st.download_button("📥 Excel", df.to_excel(index=False), f"medanta_{datetime.now().strftime('%Y%m%d')}.xlsx")
        st.download_button("📥 JSON", json.dumps(d, indent=2), f"medanta_{datetime.now().strftime('%Y%m%d')}.json")

if not st.session_state.auth: login()
else: dashboard()
st.markdown("---")
st.markdown("<p style='text-align:center'>© 2024 Medanta</p>", unsafe_allow_html=True)
