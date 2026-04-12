import streamlit as st
from .components import (
    render_intro,
    render_rules,
    gen_random_weight,
    render_select_game,
    render_setting_family,
    render_choice_weight
)
from ..Plot import Plot

class Study:
    demographic_profiles = {
        "Россия (среднее)": (58.0, 33.0, 7.0, 1.5, 0.5),
        "Россия (Москва)": (67.0, 26.0, 5.0, 1.5, 0.5),
        "Южная Корея": (85.0, 13.0, 1.8, 0.1, 0.1),
        "Евросоюз (среднее)": (50.0, 38.0, 9.0, 2.0, 1.0),
        "США": (42.0, 35.0, 15.0, 5.0, 3.0),
        "Ирландия": (40.0, 38.0, 15.0, 5.0, 2.0),
        "Нигерия": (12.0, 15.0, 22.0, 20.0, 31.0),
        "Израиль": (18.0, 25.0, 25.0, 17.0, 15.0)
    }
    plot = Plot()

    def simulate(self, data):
        pass


    def render_study(self):
        with st.container(border=True):
            render_intro()
            render_rules()
            set_data = render_choice_weight(self.demographic_profiles)
            data_user = render_setting_family(set_data)
            self.plot.render_plot_family(data_user["for_plot"])


