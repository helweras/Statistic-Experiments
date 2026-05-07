import streamlit as st
from typing import Dict, Optional, Any


class InputForm:
    """
    Класс для управления формами ввода параметров симуляции.
    """

    @staticmethod
    def get_data() -> Optional[Dict[str, Any]]:
        """
        Отрисовывает форму Streamlit для сбора параметров эксперимента.

        Функция группирует поля ввода в `st.form` и возвращает словарь с данными
        только после нажатия кнопки отправки (submit).

        Returns:
            Optional[Dict[str, Any]]: Словарь с параметрами симуляции, если форма отправлена:
                - "count_prize" (int): Количество призов.
                - "count_doors" (int): Общее количество дверей.
                - "closed_doors" (int): Количество дверей, остающихся закрытыми.
                - "iterable" (int): Количество итераций эксперимента.
            Возвращает None, если кнопка "Симуляция" еще не нажата.
        """

        with st.form("input_data_form"):
            st.subheader("Параметры эксперимента")

            # Ввод параметров
            count_prize = st.number_input(
                label="Количество призов",
                min_value=1,
                max_value=30,
                value=1
            )

            count_doors = st.number_input(
                label="Количество дверей",
                min_value=3,
                max_value=99,
                value=3
            )

            closed_doors = st.number_input(
                label="Количество закрытых дверей",
                min_value=1,
                max_value=99,
                value=1
            )

            iterable = st.number_input(
                label="Количество итераций",
                min_value=10,
                max_value=1000,
                value=100
            )

            # Кнопка отправки формы
            submitted = st.form_submit_button("Симуляция")

            if submitted:
                # Валидация логики (пример: призов не может быть больше, чем дверей)
                if count_prize >= count_doors:
                    st.error("Количество призов должно быть меньше количества дверей!")
                    return None

                return {
                    "count_prize": int(count_prize),
                    "count_doors": int(count_doors),
                    "closed_doors": int(closed_doors),
                    "iterable": int(iterable)
                }

        return None
