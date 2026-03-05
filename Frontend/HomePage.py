import streamlit as st
import requests
from MontyHall import MontyHallPage


class HomePage:
    url = "https://statistic-experiments.onrender.com"
    data: dict | None = None
    endpoints = {'Monty_Hall': "/monty_hall"}
    pages = {'Monty_Hall': MontyHallPage()}

    def __init__(self):
        self.start()

    def get_response(self):
        return requests.get(url=self.url)

    def get_data(self):
        response = self.get_response()
        self.data = response.json()

    def start(self):
        self.get_data()

    def config(self):
        st.set_page_config(
            page_title="Вероятность",
            page_icon="🚀",
            layout="wide"  # "centered" (по центру) или "wide" (на весь экран)
        )

    def side_bar(self):
        st.sidebar.title("выбор эксперимента")
        experiments_name = list(i['name'] for i in self.data['experiments'])
        with st.sidebar:
            st.header("Эксперименты")
            status_filter = st.selectbox(
                label="Выбор эксперимента",
                options=experiments_name,
                index=None,
                placeholder="Нажмите сюда"
            )
            return status_filter

    def render(self):
        self.config()

        selected_experiment = self.side_bar()

        # 3. Логика переключения
        if selected_experiment in self.pages:
            page = self.pages[selected_experiment]
            page.render()  # Предполагая, что у того класса есть метод render
        else:
            # Главная страница по умолчанию
            st.title("Добро пожаловать в Лабораторию Вероятностей")
            st.write(selected_experiment)


home = HomePage()
home.render()
