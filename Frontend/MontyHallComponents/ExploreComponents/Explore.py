import streamlit as st
import pandas as pn
import plotly.graph_objects as go
from ..ServiceClass import Service


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
            name="Т Изменить",
            line=dict(color="#bdecb6", width=7),
            mode='lines'
        ))

        fig.add_trace(go.Scatter(
            x=pandas_table.index, y=pandas_table["T_Stay"],
            name="Т Оставить",
            line=dict(color="#fadbd8", width=7),
            mode='lines'
        ))

        # 2. Линия Симуляции (яркая, с точками, чтобы подчеркнуть реальные опыты)
        fig.add_trace(go.Scatter(
            x=pandas_table.index, y=pandas_table["Change"],
            name="Изменить",
            line=dict(color="#228b22", width=2),
            marker=dict(size=5),
            mode='lines+markers'
        ))

        # Повторяем для "Остаться"

        fig.add_trace(go.Scatter(
            x=pandas_table.index, y=pandas_table["Stay"],
            name="Оставить",
            fill='tonexty',
            fillcolor='rgba(46, 204, 113, 0.2)',
            line=dict(color="#e74c3c", width=2),
            marker=dict(size=5),
            mode='lines+markers'
        ))

        fig.update_layout(
            hovermode="x unified",  # Общая подсказка для всех линий при наведении
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=0.7),
            margin=dict(l=0, r=0, t=30, b=0),
            yaxis=dict(ticksuffix="%"),
            xaxis_title=self.field_name
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
                "text": f"""количество дверей  - 1 должно быть больше чем количество закрытых дверей и при этом 
                количество закрытых дверей должно быть >= количеству призов

    количество дверей  - 1 = {count_door - 1}
    количество закрытых дверей ={closed_door} 
    количество призов = {count_prize}"""
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
