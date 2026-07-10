import streamlit as st

def init_session():
    if "current_page" not in st.session_state:
        st.session_state.current_page = "main_page"

        print("start session")