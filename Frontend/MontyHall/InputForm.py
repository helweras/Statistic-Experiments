import streamlit as st


class InputForm:
    @staticmethod
    def get_data():
        with st.form("input_data"):
            st.subheader("Параметры эксперимента")

            count_prize = st.number_input("Количество призов", min_value=1, max_value=30, value=1)
            count_doors = st.number_input("Количество дверей", min_value=3, value=3)
            closed_doors = st.number_input(label="Количество закрытых дверей", min_value=1, max_value=99, value=1)
            iterable = st.number_input(label="Количество итераций", min_value=10, max_value=1000, value=100)

            #  Специальная кнопка для отправки всей формы
            submitted = st.form_submit_button("Симуляция")

            if submitted:
                #  Собираем всё в один словарь для FastAPI
                payload = {
                    "count_prize": count_prize,
                    "count_doors": count_doors,
                    "closed_doors": closed_doors,
                    "iterable": iterable
                }
                # Возвращаем данные, чтобы отправить их через requests.post
                return payload
        return None
