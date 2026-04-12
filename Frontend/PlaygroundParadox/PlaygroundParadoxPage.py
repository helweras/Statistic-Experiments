import streamlit as st
import requests
from .Plot import Plot
from .Inspector_case.components import (
    render_head,
    render_select_part
)
from .demography_study import Study
from .Inspector_case import InspectorCase


class PlayGroundPage:
    prefix = "/playground"
    endpoints = ("/info", "/simulate")
    url = 'https://statistic-experiments.onrender.com/'
    plot = Plot()
    inspector = InspectorCase()
    study = Study()

    def get_info(self):
        response = requests.get(self.get_url(0))
        return response.json()['rules']

    def get_url(self, end):
        return self.url + self.prefix + self.endpoints[end]

    def post_request(self, data: dict, url):
        response = requests.post(self.get_url(1), json=data, timeout=20)
        return response.json()

    def render(self):
        render_head()
        part = render_select_part()
        if part == "Парадокс Инспектора":
            self.inspector.render()
        elif part == "Родственники в группе":
            self.study.render_study()
