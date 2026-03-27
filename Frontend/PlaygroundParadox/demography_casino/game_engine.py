import streamlit as st
from .components import (
    render_intro,
    render_rules,
    gen_random_weight,
    render_select_game
)
from .type_games.blood_ties import render_kinship


class Casino:
    name_game = {"Кровные узы": render_kinship,
                 "Точка невозврата": None,
                 "Большой куш": None,
                 "Охота за головами": None}

    def render_casino(self):
        with st.container(border=True):
            render_intro()
            render_rules()
            select_game = render_select_game()
            if select_game is not None:
                self.name_game[select_game]()
