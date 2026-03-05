import streamlit as st
import requests


class MontyHallPage:
    prefix = "/monty_hall"
    endpoints = ("/info", "/simulate")
    url = 'https://statistic-experiments.onrender.com/'
    text = """Парадокс Монти Холла — это контринтуитивная задача, в которой игроку предлагают выбрать одну из трех дверей (за одной — авто, за двумя — козы). После того как ведущий открывает одну из дверей с козой, игроку выгоднее изменить свой выбор, чем остаться при первоначальном.
Математически это объясняется тем, что при смене двери вероятность выигрыша удваивается (с 1/3 до 2/3), так как изначально шанс выбрать неверную дверь был значительно выше."""

    def get_info(self):
        response = requests.get(self.url + self.prefix + "/info")
        return response.json()['rules']
    def create_button(self):
        col1, col2 = st.columns(2)
        if col1.button("Правила"):
            st.write(self.get_info())

        if col2.button("Вариант Б"):
            st.write("Вы нажали Б")



    def input_form(self):
        with st.form("my_api_form"):
            st.subheader("Параметры эксперимента")

            # 1. Создаем сколько угодно полей
            name = st.text_input("Название запуска", value="Тест 1")
            count = st.number_input("Количество итераций", min_value=1, value=100)
            door_change = st.checkbox("Менять дверь?", value=True)
            difficulty = st.select_slider("Сложность", options=["Легко", "Средне", "Hard"])

            # 2. Специальная кнопка для отправки всей формы
            submitted = st.form_submit_button("Отправить на сервер")

            if submitted:
                # 3. Собираем всё в один словарь для FastAPI
                payload = {
                    "experiment_name": name,
                    "iterations": count,
                    "switch_door": door_change,
                    "mode": difficulty
                }
                # Возвращаем данные, чтобы отправить их через requests.post
                return payload
        return None

    def start_simulate(self):
        pass

    def render(self):
        st.write(self.text)
        # self.input_form()
        self.create_button()
