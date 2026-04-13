import streamlit as st
import requests
from ..client_servise import ClientService
from .components import (
    render_intro,
    render_rules,
    gen_random_weight,
    render_select_game,
    render_setting_family,
    render_choice_weight,
    render_sim_button
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
    url = 'https://statistic-experiments.onrender.com'
    prefix = "/playground"
    endpoints = ("/info", "/start_blood_tiles")
    client = ClientService(f'https://statistic-experiments.onrender.com{prefix}')


    def simulate(self, data, status_btn):
        if status_btn:
            max_value = data["value"]
            response_data = []

            for n in range(2, max_value):
                payload = {
                    'weight': data["weight"],
                     'value': n,
                     'count_sim': data["count_sim"],
                     'num_of_family': data["num_of_family"]
                }

                response_data.append(self.client.post_data(self.endpoints[1], payload))
            return response_data



    def render_study(self):
        with st.container(border=True):
            render_intro()
            render_rules()
            set_data = render_choice_weight(self.demographic_profiles)
            data_user = render_setting_family(set_data)
            self.plot.render_plot_family(data_user["for_plot"])
            status_btn = render_sim_button("start", "playground_sim_btn")
            x = self.simulate(data_user["for_sim"], status_btn)
            st.text(x)


