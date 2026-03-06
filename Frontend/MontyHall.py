import streamlit as st
import requests
import pandas as pn


class MontyHallPage:
    prefix = "/monty_hall"
    endpoints = ("/info", "/simulate")
    url = 'https://statistic-experiments.onrender.com/'
    text = """
# 🧠 Парадокс Монти Холла

Представьте: вы на телешоу. Перед вами **три двери**. За одной скрывается **автомобиль** 🏎️, а за двумя другими — 
**козы** 🐐.

1. **Ваш выбор:** Вы указываете на одну из дверей (например, №1). Шанс угадать сразу — всего **1/3**.
2. **Ход ведущего:** Монти Холл знает, где спрятан приз. Он открывает одну из оставшихся дверей (например, №3) и 
показывает там **козу**.
3. **Момент истины:** Ведущий спрашивает: *«Желаете ли вы изменить свой выбор и выбрать дверь №2?»*

---

### 📊 Математический секрет
Большинство людей думает, что шансы теперь 50/50, но это не так. **Вам выгодно сменить дверь!**

* **Почему?** Когда вы выбирали в первый раз, вы ошиблись с вероятностью **2/3**. 
* Ведущий своим действием «отфильтровал» один ложный вариант. 
* В итоге все те **2/3 вероятности** ошибки при первом выборе теперь перешли на оставшуюся закрытую дверь.

> **Итог:** Оставаясь при своем выборе, вы побеждаете в **33%** случаев. Меняя дверь — в **66%**.
"""
    text_description = """
---
### 🧪 Запустите свою симуляцию

Проверьте, как меняется математика игры при разных условиях! Попробуйте настроить количество дверей, призов и 
открытых вариантов.

> 💡 **Классический случай:** 1 приз, 3 двери и 1 открытая ведущим — это база, где шансы при смене выбора удваиваются.

**Готовы настроить свои параметры и увидеть магию чисел?** 👇
"""

    def get_info(self):
        response = requests.get(self.get_url(0))
        return response.json()['rules']

    def get_url(self, end):
        return self.url + self.prefix + self.endpoints[end]

    def post_request(self, data: dict):
        response = requests.post(self.get_url(1), json=data)
        return response.json()

    def create_button(self):
        if st.button("Правила"):
            st.markdown(self.get_info())

    def input_form(self):
        with st.form("data"):
            st.subheader("Параметры эксперимента")

            # 1. Создаем сколько угодно полей
            count_prize = st.number_input("Количество призов", min_value=1, max_value=30, value=1)
            count_doors = st.number_input("Количество дверей", min_value=3, value=3)
            closed_doors = st.number_input(label="Количество закрытых дверей", min_value=1, max_value=99, value=1)
            iterable = st.number_input(label="Количество итераций", min_value=10, max_value=1000, value=100)

            # 2. Специальная кнопка для отправки всей формы
            submitted = st.form_submit_button("Симуляция")

            if submitted:
                # 3. Собираем всё в один словарь для FastAPI
                payload = {
                    "count_prize": count_prize,
                    "count_doors": count_doors,
                    "closed_doors": closed_doors,
                    "iterable": iterable
                }
                # Возвращаем данные, чтобы отправить их через requests.post
                return payload
        return None

    def check_response(self, response):
        if response["status"] == "Good":
            return True
        st.error(response['msg'])
        st.info("""
                            **Требования для запуска:**
                            * Все числа должны быть **больше 0**.
                            * Общее число дверей должно быть **минимум на 2 больше**, чем количество призов.
                            * Ведущий должен закрыть **не меньше**, чем количество призов, 
                            но **не все** оставшиеся двери.
                            """)

    @st.fragment
    def research_mode(self):
        st.subheader("🚀 Сценарий: Масштабирование (D от 3 до 50)")
        st.write("Выясним, как растет преимущество смены выбора с увеличением общего числа дверей.")

        if "data_set" not in st.session_state:
            st.session_state.data_set = None

        # Настройки внутри фрагмента
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                s_fixed = st.number_input("Фикс. количество призов (S)", 1, 5, 1)
            with col2:
                it = st.select_slider("Итераций в каждой точке", options=[50, 100, 200], value=100)

            max_d = st.slider("До какого количества дверей (D) дойти?", 5, 30, 15)
            num_points = max_d - s_fixed - 1
            st.info(f"📊 Будет проведено **{num_points}** экспериментов (по одной точке на каждое количество дверей).")

            if st.button("Запустить масштабное исследование", type="primary"):
                data_set = []
                with st.status("Запуск симуляции...", expanded=False) as status:
                    for door in range(s_fixed + 2, max_d + 1):
                        status.update(label=f"Проведение эксперимнта №: {door-2} ...")
                        payload = {
                            "count_prize": s_fixed,
                            "count_doors": door,
                            "closed_doors": s_fixed,
                            "iterable": it
                        }
                        response = self.post_request(payload)
                        if self.check_response(response):
                            result = response["data"]["Customizable"]
                            data_set.append(result)
                st.session_state.data_set = data_set
            if st.session_state.data_set is not None:
                st.write(st.session_state.data_set)

    def start_simulate(self, data):
        response = self.post_request(data)
        with st.expander("Посмотреть сырые данные от сервера"):
            st.json(response)
        if self.check_response(response):
            result = response["data"]["Customizable"]

            stay_rate = result['Stay']
            switch_rate = result['Change']

            col1, col2 = st.columns(2)
            col1.metric("Побед при смене выбора", f"{switch_rate:.1f}%", f"{switch_rate - 50:.1f}%")
            col2.metric("Побед без смены", f"{stay_rate:.1f}%", f"{stay_rate - 50:.1f}%")

    def render(self):
        st.write(self.text)
        st.markdown(self.get_info())
        st.markdown(self.text_description)
        data = self.input_form()
        if data:
            self.start_simulate(data)

        self.research_mode()
