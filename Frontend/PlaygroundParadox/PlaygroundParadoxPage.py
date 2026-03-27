import streamlit as st
import requests
from .Plot import Plot
from .components import (
    render_description,
    render_explanations,
    render_finish,
    render_instruction,
    render_midl_explanations,
    render_midl_metric,
    render_ratio,
    render_setting_family,
    render_title
)


class PlayGroundPage:
    prefix = "/playground"
    endpoints = ("/info", "/simulate")
    url = 'https://statistic-experiments.onrender.com/'
    plot = Plot()

    def get_info(self):
        response = requests.get(self.get_url(0))
        return response.json()['rules']

    def get_url(self, end):
        return self.url + self.prefix + self.endpoints[end]

    def post_request(self, data: dict, url):
        response = requests.post(self.get_url(1), json=data, timeout=20)
        return response.json()

    @st.fragment
    def config_family(self):
        with st.container(border=True):
            render_title()
            render_instruction()
            data = render_setting_family()
            self.plot.render_two_plots(data)
            render_explanations()
            render_midl_metric(data)
            render_midl_explanations()
            render_finish()

    def render(self):
        render_description()
        render_ratio()
        self.config_family()
