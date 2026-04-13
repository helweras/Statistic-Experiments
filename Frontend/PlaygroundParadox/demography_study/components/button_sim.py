import streamlit as st

def render_sim_button(label: str, button_key: str):
    """
    Отрисовывает кнопку и обрабатывает нажатие.

    Args:
        label (str): Текст на кнопке.
        button_key (str): Уникальный идентификатор кнопки.

    Returns:
        bool: Состояние нажатия кнопки.
    """
    # type primary делает кнопку яркой (обычно красной/синей)
    if st.button(label, key=button_key, type="primary", width="stretch"):
        return True
    return False