import streamlit as st
from .components import (
    render_description,
    render_explanations,
    render_finish,
    render_head,
    render_instruction,
    render_midl_explanations,
    render_midl_metric,
    render_ratio,
    render_select_part,
    render_setting_family,
    render_title
)
from ..Plot import Plot

class InspectorCase:

    plot = Plot()

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
