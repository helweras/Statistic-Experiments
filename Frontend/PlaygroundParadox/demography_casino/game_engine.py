import streamlit as st
from .components import (
    render_intro,
    render_rules
)


def casino():
    with st.container(border=True):
        render_intro()
        render_rules()
