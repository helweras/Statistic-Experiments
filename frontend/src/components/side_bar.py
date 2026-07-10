import streamlit as st


def render(page_list: list):
    menu_ids = [item["id"] for item in page_list]
    current_index = menu_ids.index(st.session_state.current_page) if st.session_state.current_page in menu_ids else 0

    with st.sidebar:
        st.header("Выбор эксперимента")
        page = st.selectbox(label="Эксперимент",
                            options=page_list,
                            key="side_bar",
                            format_func=lambda option: option["title"],
                            index=current_index)
        return page
