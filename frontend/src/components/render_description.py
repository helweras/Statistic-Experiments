import streamlit as st


@st.fragment
def render_description_experiment(name_dir_experiment):
    with open(f"texts/{name_dir_experiment}/description", "r", encoding="utf-8") as text:
        description = text.read()
        st.markdown(description)
