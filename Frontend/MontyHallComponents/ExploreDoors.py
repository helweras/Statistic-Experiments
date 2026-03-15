import streamlit as st
import pandas as pn
from .ServiceClass import Service
import plotly.graph_objects as go


class Explore:
    service = Service()
    field_name = ""
    const = 0

    def render_graph(self, pandas_table):
        st.write("### 📈 Динамика вероятности выигрыша")
        st.line_chart(
            pandas_table,
            y=["Change", "Stay", "T_Change", "T_Stay"],  # Берем только эти две колонки для линий
            color=["#2ecc71", "#e74c3c", "#a9dfbf", "#fadbd8"]  # Зеленый для смены, Красный для "остаться"
        )

    def render_graph_plotly(self, pandas_table):
        st.write("### 📈 Анализ точности симуляции")

        fig = go.Figure()

        # 1. Линия Теории (делаем её фоновой, широкой и плавной)
        fig.add_trace(go.Scatter(
            x=pandas_table.index, y=pandas_table["T_Change"],
            name="Теория (Изменить)",
            line=dict(color="#bdecb6", width=7),
            mode='lines'
        ))

        fig.add_trace(go.Scatter(
            x=pandas_table.index, y=pandas_table["T_Stay"],
            name="Теория (Оставить)",
            line=dict(color="#fadbd8", width=7),
            mode='lines'
        ))

        # 2. Линия Симуляции (яркая, с точками, чтобы подчеркнуть реальные опыты)
        fig.add_trace(go.Scatter(
            x=pandas_table.index, y=pandas_table["Change"],
            name="Симуляция (Изменить)",
            line=dict(color="#228b22", width=2),
            marker=dict(size=5),
            mode='lines+markers'
        ))

        # Повторяем для "Остаться"

        fig.add_trace(go.Scatter(
            x=pandas_table.index, y=pandas_table["Stay"],
            name="Симуляция (Оставить)",
            fill='tonexty',
            fillcolor='rgba(46, 204, 113, 0.2)',
            line=dict(color="#e74c3c", width=2),
            marker=dict(size=5),
            mode='lines+markers'
        ))

        fig.update_layout(
            hovermode="x unified",  # Общая подсказка для всех линий при наведении
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=0.5),
            margin=dict(l=0, r=0, t=30, b=0),
            yaxis=dict(ticksuffix="%"),
            xaxis_title="Количество дверей"
        )

        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def get_theory(doors, prize, closed):
        stay = (prize / doors) * 100
        change = (prize * (doors - 1)) / (doors * closed) * 100
        result = {"T_Stay": round(stay, 2), "T_Change": round(change, 2)}
        return result

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
            self.render_graph_plotly(df)
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
            max_doors = st.slider(label="Конечное количество дверей",
                                  min_value=8,
                                  max_value=20,
                                  value=10,
                                  key="max_doors"
                                  )
            min_doors = st.number_input(label="Начальное количество дверей",
                                        min_value=3,
                                        max_value=max_doors - 5,
                                        value=3,
                                        key="min_doors"
                                        )
            close_doors = c2.number_input("Количество закрытых дверей", 1, min_doors - 2, 1, key="close_doors")
            it = c3.select_slider("Итераций", options=[50, 75, 100, 150], value=75)

            prize = c1.number_input("Количество призов", 1, close_doors, 1, key="prize")
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
                theory_data = self.get_theory(doors=door, prize=prize, closed=close_doors)
                response["data"]["Customizable"].update(theory_data)
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
            max_close_doors = st.slider("Конечное закрытых количество дверей", 6, 20, 10)
            min_close_doors = st.number_input("Начальное количество закрытых дверей", 1, max_close_doors - 5, 1)
            it = c3.select_slider("Итераций", options=[50, 75, 100, 150], value=75)
            doors = c2.number_input("Количество дверей", max_close_doors + 2, 22, max_close_doors + 2)
            prize = c1.number_input("Количество призов", 1, min_close_doors, 1)
            st.markdown(f"### 🚀 Симуляция стартует с **{min_close_doors}** и до **{max_close_doors}** закрытых дверей.")

            # 2. Кнопка запуска
            if st.button("Запустить масштабное исследование", type="primary"):
                results = self.run_simulation(prize=prize,
                                              max_close_doors=max_close_doors,
                                              doors=doors, it=it,
                                              url=url,
                                              text_validation=text_validation,
                                              min_close_doors=min_close_doors)

                if results:
                    st.session_state.data_set = results
            if st.session_state.data_set is not None:
                self.process_and_render_results()

    def run_simulation(self, min_close_doors, prize, max_close_doors, doors, it, text_validation, url):
        """Бизнес-логика: сбор данных через API."""
        data_set = []
        # Валидация всех шагов перед запуском
        for close_doors in range(min_close_doors, max_close_doors + 1):
            response_valid_test = self.valid_input_data(prize, doors, close_doors)
            if not response_valid_test["status"]:
                st.error(response_valid_test["text"])
                return None

        status_text = st.empty()
        for close_doors in range(min_close_doors, max_close_doors + 1):
            status_text.text(f"⏳ Симуляция для {close_doors} закрытых дверей...")
            payload = {
                "count_prize": prize,
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
