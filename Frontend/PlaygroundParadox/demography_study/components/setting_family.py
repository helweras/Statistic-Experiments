import streamlit as st


def render_setting_family(data):
    st.subheader("Настройка семей")
    cols = st.columns(5)
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

    family_counts = {}

    for i, (label, default, key) in enumerate(kids_data):
        widget_key = f"{key}_child"
        rus_key = label_translate[key]
        family_counts[rus_key] = cols[i].number_input(
            label=label,
            min_value=0.0,
            value=default,
            max_value=100.0,
            key=widget_key,
            step=1.0
        )

    return family_counts
