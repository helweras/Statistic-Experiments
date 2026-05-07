import streamlit as st


def render_setting_family():
    st.subheader("Настройка семей")
    cols = st.columns(5)
    kids_data = [
        ("1 ребенком", 55, "one"),
        ("2 детьми", 33, "two"),
        ("3 детьми", 9, "three"),
        ("4 детьми", 2, "four"),
        ("5 детьми", 1, "five")
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
        rus_key = label_translate[key]
        family_counts[rus_key] = cols[i].number_input(
            label=label,
            min_value=0,
            max_value=500,
            value=default,
            key=f"{key}_child"
        )
    return family_counts
