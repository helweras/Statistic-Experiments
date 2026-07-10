import streamlit as st
from typing import Dict, Optional, Any
from src.components.render_description import render_description_experiment


def _render_explore():
    with st.container(border=True):
        st.write("Выясним, как меняется преимущество смены выбора с увеличением общего числа закрытых дверей.")
        # 1. Блок ввода параметров
        c1, c2, c3 = st.columns(3)
        max_close_doors = st.slider("Конечное закрытых количество дверей", 6, 20, 10)
        min_close_doors = st.number_input("Начальное количество закрытых дверей", 1, max_close_doors - 5, 1)
        it = c3.select_slider("Итераций", options=[50, 75, 100, 150], value=75)
        doors = c2.number_input("Количество дверей", max_close_doors + 2, 22, max_close_doors + 2)
        prize = c1.number_input("Количество призов", 1, min_close_doors, 1)
        st.markdown(f"### 🚀 Симуляция стартует с **{min_close_doors}** и до **{max_close_doors}** закрытых дверей.")
        if st.button("Запустить исследование", type="primary"):
            print({
                "it": it,
                "doors": doors,
                "prize": prize
            })





def _render_input_form() -> Optional[Dict[str, Any]]:
    """
    Отрисовывает форму Streamlit для сбора параметров эксперимента.
    """
    with st.form("input_data_form"):
        st.subheader("Параметры эксперимента")

        count_prize = st.number_input(
            label="Количество призов",
            min_value=1, max_value=30, value=1
        )

        count_doors = st.number_input(
            label="Количество дверей",
            min_value=3, max_value=99, value=3
        )

        closed_doors = st.number_input(
            label="Количество закрытых дверей",
            min_value=1, max_value=99, value=1
        )

        iterable = st.number_input(
            label="Количество итераций",
            min_value=10, max_value=1000, value=100
        )

        submitted = st.form_submit_button("Симуляция")

        if submitted:
            if count_prize is None or count_doors is None:
                st.error("Пожалуйста, заполните все поля числовыми значениями!")
                return None

            # Валидация логики
            if count_prize >= count_doors:
                st.error("Количество призов должно быть меньше количества дверей!")
                return None

            # Математическая валидация парадокса
            if (1 + closed_doors) >= count_doors:
                st.error(f"Ведущий не может оставить закрытыми {closed_doors} дв. при общем количестве {count_doors}!")
                return None

            return {
                "count_prize": count_prize,
                "count_doors": count_doors,
                "closed_doors": closed_doors,
                "iterable": iterable
            }

    return None



def render():
    render_description_experiment("Monty_Hall")
    _render_input_form()
    _render_explore()