import streamlit as st


def init_monty_hall_state():
    """Резервирует места под ответы бэкенда в памяти сессии."""
    if "single_result" not in st.session_state:
        st.session_state.single_result = None

    if "explore_result" not in st.session_state:
        st.session_state.explore_result = None