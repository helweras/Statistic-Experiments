import streamlit as st


def render_select_game():
    game = st.selectbox(
        label="Выберете игру",
        options=list(["Кровные узы",
                      "Точка невозврата",
                      "Большой куш",
                      "Охота за головами"]),
        key="select_game",  # Уникальный ключ для фрагмента
        index=None,
        placeholder="Нажмите сюда"
    )
    return game
