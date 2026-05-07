import streamlit as st


def render_explore(data: dict):
    option_list = [name for name in data.keys()]
    with st.container(border=True):
        st.write("Выберете модель распределения")
        model = st.selectbox(
        label="Выберете модель",
        options=option_list,
        key="select_model",  # Уникальный ключ для фрагмента
        index=None,
        placeholder="Нажмите сюда"
    )

