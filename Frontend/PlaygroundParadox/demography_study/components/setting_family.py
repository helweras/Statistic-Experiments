import streamlit as st
from streamlit import columns


def render_setting_family(data):
    """
       Отрисовывает интерфейс настройки распределения детей в семьях.

       Args:
           data (dict): Данные конфигурации. Ожидается:
               - "select_flag" (bool): Использовать ли данные из ключа "kids_data".
               - "kids_data" (list): Список кортежей (лейбл, значение, ключ).

       Returns:
           dict: Распределение семей в формате {Название: Значение}.
       """
    if data["select_flag"]:
        kids_data = data["kids_data"]

    else:
        kids_data = [
            ("1 ребенком", 55.0, "one"),
            ("2 детьми", 33.0, "two"),
            ("3 детьми", 9.0, "three"),
            ("4 детьми", 2.0, "four"),
            ("5 детьми", 1.0, "five")
        ]
    label_translate = {
        "one": "Один ребенок",
        "two": "Два ребенка",
        "three": "Три ребенка",
        "four": "Четыре ребенка",
        "five": "Пять детей"
    }

    weights = []

    family_counts = {}




    st.subheader("Настройка семей")
    with st.container(border=True):
        cols = st.columns(5)

        for i, (label, default, key) in enumerate(kids_data):
            widget_key = f"{key}_child"
            rus_key = label_translate[key]
            params = {
                "label": label,
                "min_value": 0.0,
                "max_value": 100.0,
                "key": widget_key,
                "step": 1.0
            }

            if widget_key not in st.session_state:
                params["value"] = default

            family_counts[rus_key] = cols[i].number_input(**params)
            weights.append(st.session_state[widget_key])

    with st.container(border=True):
        st.subheader("Настройка параметров симуляции")
        family_count, iter_count, max_value = st.columns(3)
        num_of_family = family_count.number_input(
            label="Количество семей",
            min_value=75,
            max_value=500,
            value=100,
            key="family_count"
        )
        count_sim = iter_count.slider(
            label="Число итераций",
            min_value=100,
            max_value=1000,
            value=250,  # Значение по умолчанию
            step=50,
            key="family_iter_count"
        )
        value = max_value.number_input(
            label="Максимальный размер группы",
            min_value=3,
            max_value=30,
            value=20,
            key="count_group"
        )

    setting_simulate = {
        "weight": tuple(weights),
        "value": value,
        "count_sim": count_sim,
        "num_of_family": num_of_family
    }

    response_data = {"for_plot": family_counts,
                     "for_sim": setting_simulate}

    st.text(response_data)
    return response_data
