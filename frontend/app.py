import streamlit as st
from src.state import init_session
from pages_list import REGISTRY_PAGES
from src.components import side_bar



st.set_page_config(
    page_title="Парадоксы Веб-Приложение",
    page_icon="🧠",
    layout="wide",  # Делает интерфейс на весь экран
    initial_sidebar_state="expanded"
)


init_session()

select_page = side_bar.render(REGISTRY_PAGES)

st.session_state.current_page = select_page["id"]

# 3. Запускаем рендеринг страницы
select_page["render_func"]()
