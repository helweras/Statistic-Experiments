import streamlit as st
from typing import Dict, List, Tuple, Optional, Any


def render_choice_weight(country_data: Dict[str, Tuple[float, ...]]) -> Dict[str, Any]:
    """
    Отрисовывает интерфейс выбора страны и управляет весами распределения детей.

    Функция обновляет session_state при выборе страны и возвращает данные
    для дальнейшей отрисовки графиков или расчетов.

    Args:
        country_data (Dict[str, List[float]]): Словарь, где ключ — название страны,
            а значение — список из 5 весов (от 1 до 5 детей).

    Returns:
        Dict[str, Any]: Словарь с результатами:
            - "country_name" (str|None): Название выбранной страны.
            - "kids_data" (Tuple): Кортеж с лейблами, значениями и ключами.
            - "select_flag" (bool): Выбрана ли страна в данный момент.
    """

    # Константы для структуры данных
    KEYS = ["one_child", "two_child", "three_child", "four_child", "five_child"]
    LABELS = ["1 ребенком", "2 детьми", "3 детьми", "4 детьми", "5 детьми"]
    SHORT_KEYS = ["one", "two", "three", "four", "five"]
    DEFAULT_WEIGHTS = (55.0, 33.0, 9.0, 2.0, 1.0)

    def on_country_change():
        """Callback для синхронизации выбора с session_state."""
        selected = st.session_state.get("select_weight")
        if selected in country_data:
            new_values = country_data[selected]
            # Обновляем глобальное состояние значениями из словаря
            for key, value in zip(KEYS, new_values):
                st.session_state[key] = float(value)

    # Отрисовка селектора
    choice_country = st.selectbox(
        label="Выберите распределение",
        options=list(country_data.keys()),
        key="select_weight",
        index=None,
        placeholder="Нажмите сюда",
        on_change=on_country_change,
    )

    # Получение текущих весов (выбранных или по умолчанию)
    current_weights = country_data.get(choice_country, DEFAULT_WEIGHTS)

    # Формирование структурированных данных для вывода
    kids_data = tuple(zip(LABELS, current_weights, SHORT_KEYS))

    return {
        "country_name": choice_country,
        "kids_data": kids_data,
        "select_flag": bool(choice_country),
        "weights": current_weights
    }
