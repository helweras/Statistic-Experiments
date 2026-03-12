import streamlit as st
import pandas as pn
from .ServiceClass import Service


class Explore:
    service = Service()
    field_name = ""
    const = 0

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

    def create_pandas_table(self, data_set):
        df = pn.DataFrame(data_set)
        df[self.field_name] = df.index + self.const
        df = df.set_index(self.field_name)
        return df

    @staticmethod
    def valid_input_data(count_prize, count_door, closed_door):
        """Валидация принимаемых значений"""
        first = count_prize <= count_door - 2
        if not first:
            response = {
                "status": False,
                "text": f"""количество призов = {count_prize} и количество дверей = {count_door} не соответствуют условию "Общее число дверей 
должно быть минимум на 2 больше, чем количество призов" """
            }
            return response
        second = count_door - 1 > closed_door >= count_prize
        if not second:
            response = {
                "status": False,
                "text": f"""количество дверей  - 1 должно быть больше чем  и при это 
                количество закрытых дверей должно быть >= количеству призов
{count_door - 1}(количество дверей  - 1) > 
{closed_door}(количество закрытых дверей) >= {count_prize}(количество призов)"""
            }
            return response
        three = count_prize > 0 and count_door > 0 and closed_door > 0
        if not three:
            response = {
                "status": False,
                "text": f"""Все числа должны быть положительны
                количество дверей = {count_door}
                количество закрытых дверей = {closed_door}
                количество призов = {count_prize}
"""
            }
            return response
        if all((first, second, three)):
            response = {
                "status": True
            }
            return response

    def run_simulation(self, start_params, s_fixed, max_d, close_doors, it, text_validation, url):
        """Бизнес-логика: сбор данных через API."""
        pass

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

    def explore(self, url, text_validation):
        pass


class ExploreDoors(Explore):
    field_name = "двери"
    const = 3

    def explore(self, url, text_validation):
        with st.container(border=True):
            st.write("Выясним, как растет преимущество смены выбора с увеличением общего числа дверей.")

            # 1. Блок ввода параметров
            c1, c2, c3 = st.columns(3)
            max_doors = st.slider("Конечное количество дверей", 8, 20, 10)
            min_doors = st.number_input("Начальное количество дверей", 3, max_doors - 5, 3)
            it = c3.select_slider("Итераций", options=[50, 75, 100, 150], value=75)
            close_doors = c2.number_input("Количество закрытых дверей", 1, min_doors - 2, 1)
            prize = c1.number_input("Количество призов", 1, close_doors, 1)
            st.markdown(f"### 🚀 Симуляция стартует с **{min_doors}** и до **{max_doors}** дверей.")

            # 2. Кнопка запуска
            if st.button("Запустить масштабное исследование", type="primary"):
                results = self.run_simulation(start_door=min_doors,
                                              end_doors=max_doors,
                                              prize=prize,
                                              close_doors=close_doors,
                                              it=it,
                                              text_validation=text_validation,
                                              url=url
                                              )

                if results:
                    st.session_state.data_set = results
            if st.session_state.data_set is not None:
                self.process_and_render_results()

    def run_simulation(self, start_door, prize, end_doors, close_doors, it, text_validation, url):
        """Бизнес-логика: сбор данных через API."""
        data_set = []
        # Валидация всех шагов перед запуском
        for door in range(start_door, end_doors + 1):
            response_valid_test = self.valid_input_data(prize, door, close_doors)
            if not response_valid_test["status"]:
                st.error(response_valid_test["text"])
                return None

        status_text = st.empty()
        for door in range(close_doors + 2, end_doors + 1):
            status_text.text(f"⏳ Симуляция для {door} дверей...")
            payload = {
                "count_prize": prize,
                "count_doors": door,
                "closed_doors": close_doors,
                "iterable": it
            }
            response = self.service.post_request(payload, url)

            if self.service.check_response(response):
                data_set.append(response["data"]["Customizable"])
            else:
                return None
        return data_set


class ExploreCloseDoors(Explore):
    field_name = "Закрытые двери"
    const = 1

    def explore(self, url, text_validation):
        with st.container(border=True):
            st.write("Выясним, как растет преимущество смены выбора с увеличением общего числа закрытых дверей.")
            # 1. Блок ввода параметров
            c1, c2, c3 = st.columns(3)
            s_fixed = c1.number_input("Количество призов", 1, 10, 1)
            doors = c2.number_input("Количество дверей", 1, 20, 1)
            it = c3.select_slider("Итераций", options=[50, 75, 100, 150], value=75)
            max_close_doors = st.slider("Конечное количество закрытых дверей", 5, 20, 10)
            min_close_doors = st.slider("Начальное количество закрытых дверей", s_fixed, max_close_doors - 5, s_fixed)

            # 2. Кнопка запуска
            if st.button("Запустить масштабное исследование", type="primary"):
                results = self.run_simulation(s_fixed=s_fixed,
                                              max_close_doors=max_close_doors,
                                              doors=doors, it=it,
                                              url=url,
                                              text_validation=text_validation,
                                              min_close_doors=min_close_doors)

                if results:
                    st.session_state.data_set = results
            if st.session_state.data_set is not None:
                self.process_and_render_results()

    def run_simulation(self, min_close_doors, s_fixed, max_close_doors, doors, it, text_validation, url):
        """Бизнес-логика: сбор данных через API."""
        data_set = []
        # Валидация всех шагов перед запуском
        for close_doors in range(min_close_doors, max_close_doors + 1):
            response_valid_test = self.valid_input_data(s_fixed, doors, close_doors)
            if not response_valid_test["status"]:
                st.error(response_valid_test["text"])
                return None

        status_text = st.empty()
        for close_doors in range(min_close_doors, max_close_doors + 1):
            status_text.text(f"⏳ Симуляция для {close_doors} закрытых дверей...")
            payload = {
                "count_prize": s_fixed,
                "count_doors": doors,
                "closed_doors": close_doors,
                "iterable": it
            }
            response = self.service.post_request(payload, url)

            if self.service.check_response(response):
                data_set.append(response["data"]["Customizable"])
            else:
                return None
        return data_set
