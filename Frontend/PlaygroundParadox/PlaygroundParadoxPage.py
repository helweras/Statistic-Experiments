import streamlit as st
import requests
from .Plot import Plot
from . import Components


class PlayGroundPage:
    prefix = "/playground"
    endpoints = ("/info", "/simulate")
    url = 'https://statistic-experiments.onrender.com/'
    text = """# 👨‍👩‍👧‍👦 Парадокс детской площадки
### Почему наши глаза видят больше детей с братьями и сестрами, чем официальные отчеты?

---

#### 📍 Точка отсчета: Реальность
Официальная статистика говорит нам, что в России семьи распределены так:

*   **55% семей** — воспитывают всего одного ребенка.
*   **33% семьи** — двоих детей.
*   **12% семей** — многодетные (три и более ребенка).

Глядя на эти цифры, кажется очевидным: **большинство детей в стране — единственные у родителей.** Ведь таких семей больше половины! 

#### 🕵️‍♂️ Но так ли это на самом деле?
Если вы выйдете во двор или зайдете в школьный класс, вы заметите странную вещь: детей с братьями и сестрами там будет гораздо больше, чем предсказывает эта статистика. 

**Куда исчезают «одиночки» и откуда берутся большие семьи?** Давайте проверим вашу интуицию, прежде чем заглянуть в закулисье математики."""
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
            Components.render_title()
            Components.render_instruction()
            data = Components.render_setting_family()
            self.plot.render_two_plots(data)
            Components.render_explanations()
            Components.render_midl_metric(data)
            Components.render_explanations()
            Components.render_finish()

    def render(self):
        st.markdown(self.text)
        Components.ratio()
        self.config_family()
