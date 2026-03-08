import streamlit as st
import requests
import pandas as pn
from .InputForm import InputForm


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
    text_validation = """
                                                        **Требования для запуска:**
                                                        * Все числа должны быть **больше 0**.
                                                        * Общее число дверей должно быть **минимум на 2 больше**, чем количество призов.
                                                        * Ведущий должен закрыть **не меньше**, чем количество призов, 
                                                        но **не все** оставшиеся двери.
                                                        """
    input_form = InputForm()

    def get_info(self):
        response = requests.get(self.get_url(0))
        return response.json()['rules']

    def get_url(self, end):
        return self.url + self.prefix + self.endpoints[end]

    def post_request(self, data: dict):
        response = requests.post(self.get_url(1), json=data, timeout=20)
        return response.json()

    def check_response(self, response):
        if response["status"] == "Good":
            return True
        st.error(response['msg'])
        st.info(self.text_validation)
        return False

    def check_data_set(self, data_set):
        if data_set is not None:
            return True
        return False

    def create_pandas_table(self, data_set):
        df = pn.DataFrame(data_set)
        df["двери"] = df.index + 3
        df = df.set_index("двери")
        return df

    def render_graph(self, pandas_table):
        st.write("### 📈 Динамика вероятности выигрыша")
        st.line_chart(
            pandas_table,
            y=["Change", "Stay"],  # Берем только эти две колонки для линий
            color=["#2ecc71", "#e74c3c"]  # Зеленый для смены, Красный для "остаться"
        )

    def get_pandas_table(self, pandas_table):
        with st.expander("🔬 Посмотреть детальную таблицу"):
            st.dataframe(pandas_table)

    def select_params(self):
        scenario = st.selectbox(
            "Выберете зависимую переменную",
            ["Количество дверей", "Количество призов", "Количество закрытых дверей"],
            key="scenario_select",  # Уникальный ключ для фрагмента
            index=None,
            placeholder="Нажмите сюда"
        )
        return scenario

    def explore_close_doors(self):
        with st.container(border=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                s_fixed = st.number_input("Фикс. количество призов", 1, 10, 1)
            with col2:
                it = st.select_slider("Итераций в каждой точке", options=[50, 75, 100, 150], value=75)
            with col3:
                door = st.number_input("Фикс. количество дверей", 1, 10, 1)

            max_close_doors = st.slider("До какого количества закрытых дверей дойти?", 5, 20, 10)

            if st.button("Запустить масштабное исследование", type="primary"):
                data_set = []
                with st.status("Запуск симуляции...", expanded=True) as status:
                    for close_door in range(s_fixed, max_close_doors + 1):
                        status.update(label=f"Проведение эксперимнта №: {door - 2} ...")
                        payload = {
                            "count_prize": s_fixed,
                            "count_doors": door,
                            "closed_doors": close_door,
                            "iterable": it
                        }
                        response = self.post_request(payload)
                        if self.check_response(response):
                            st.write(f"⚙️ успешно выполнено для {door} дверей...")
                            result = response["data"]["Customizable"]
                            data_set.append(result)

                st.session_state.data_set = data_set
            if self.check_data_set(st.session_state.data_set):
                pandas_table = self.create_pandas_table(st.session_state.data_set)
                self.render_graph(pandas_table)

    @staticmethod
    def valid_input_data(count_prize, count_door, closed_door):
        """Валидация принимаемых значений"""
        first = count_prize <= count_door - 2
        second = count_door - 1 > closed_door >= count_prize
        three = count_prize > 0 and count_door > 0 and closed_door > 0
        if all((first, second, three)):
            return True
        return False

    def run_simulation(self, s_fixed, max_d, close_doors, it):
        """Бизнес-логика: сбор данных через API."""
        data_set = []
        # Валидация всех шагов перед запуском
        for door in range(close_doors + 2, max_d + 1):
            if not self.valid_input_data(s_fixed, door, close_doors):
                st.error(f"Ошибка валидации для {door} дверей: {self.text_validation}")
                return None

        status_text = st.empty()
        for door in range(close_doors + 2, max_d + 1):
            status_text.text(f"⏳ Симуляция для {door} дверей...")
            payload = {
                "count_prize": s_fixed,
                "count_doors": door,
                "closed_doors": close_doors,
                "iterable": it
            }
            response = self.post_request(payload)

            if self.check_response(response):
                data_set.append(response["data"]["Customizable"])
            else:
                return None
        return data_set

    def process_and_render_results(self):
        """Бизнес-процесс обработки и отрисовки."""
        if not st.session_state.get("data_set"):
            return

        df = self.create_pandas_table(st.session_state.data_set)

        # Отладочная проверка: если здесь пусто, график упадет
        if df.empty:
            st.warning("Таблица данных пуста. Проверьте ответ от API.")
            return

        st.subheader("Результаты исследования")
        self.get_pandas_table(df)  # Посмотрите, есть ли там колонка "Change"

        # Вызываем рендер только если данные валидны
        if "Change" in df.columns:
            self.render_graph(df)
        else:
            st.error(f"Столбец 'Change' не найден. Доступные столбцы: {list(df.columns)}")

    def explore_doors(self):
        with st.container(border=True):
            # 1. Блок ввода параметров
            c1, c2, c3 = st.columns(3)
            s_fixed = c1.number_input("Фикс. количество призов", 1, 10, 1)
            close_doors = c2.number_input("Фикс. закрытых дверей", 1, 10, 1)
            it = c3.select_slider("Итераций", options=[50, 75, 100, 150], value=75)
            max_d = st.slider("Макс. количество дверей", 5, 20, 10)

            # 2. Кнопка запуска
            if st.button("Запустить масштабное исследование", type="primary"):
                results = self.run_simulation(s_fixed, max_d, close_doors, it)

                if results:
                    st.session_state.data_set = results
                    self.process_and_render_results()

    @st.fragment
    def research_mode(self):
        st.subheader("🚀 Сценарий: Масштабирование (D от 3 до 20)")
        st.write("Выясним, как растет преимущество смены выбора с увеличением общего числа дверей.")

        if "data_set" not in st.session_state:
            st.session_state.data_set = None

        scenario = self.select_params()

        # Настройки внутри фрагмента
        self.explore_doors()

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
        data = self.input_form.get_data()
        if data:
            self.start_simulate(data)

        self.research_mode()
