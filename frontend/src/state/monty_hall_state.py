import streamlit as st
import pandas as pd


class MontyHallState:

    def __init__(self):
        """Резервирует места под ответы бэкенда в памяти сессии."""
        if "single_result" not in st.session_state:
            st.session_state.single_result = None


        if "explore_result" not in st.session_state:
            st.session_state.explore_result = None



    @property
    def explore_df(self) -> pd.DataFrame:
        """Возвращает DataFrame исследования, если он есть, иначе пустой."""
        if st.session_state.explore_result is None:
            return pd.DataFrame()
        raw_df = pd.DataFrame(st.session_state.explore_result)

        df = pd.DataFrame(raw_df["data_experiments"].tolist())
        return df

    @staticmethod
    def set_explore_result(data):
        """Записывает ответ от бэкенда для исследования."""
        st.session_state.explore_result = data

    @staticmethod
    def set_single_result(data):
        st.session_state.single_result = data

    @staticmethod
    def delite_explore_result():
        st.session_state.explore_result = None

    @staticmethod
    def delite_single_result():
        st.session_state.single_result = None
