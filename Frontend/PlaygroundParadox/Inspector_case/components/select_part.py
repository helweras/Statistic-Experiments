import streamlit as st


def render_select_part():
    part = st.selectbox(
        label="Выберете раздел",
        options=list(["Разбор парадокса",
                      "Играть в казино"]),
        key="select_part",  # Уникальный ключ для фрагмента
        index=None,
        placeholder="Нажмите сюда"
    )
    return part
