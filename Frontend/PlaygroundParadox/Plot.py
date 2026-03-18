import plotly.graph_objects as go
import streamlit as st


class Plot:
    def render_plot_family(self, data: dict):
        colors = ["#1fcecb", "#731fce", "#ce1f22", "#7ace1f", "#cecb1f"]
        label = list(data.keys())
        value = list(data.values())
        value_midl = sum(list(
            map(
                lambda x: ((x[0] + 1) * x[-1]),
                tuple(enumerate(data.values()))
            )
        )
        ) / sum(tuple(data.values()))
        total = sum(value)
        text_labels = [f"{round(v / total * 100, 1)}%" for v in value]
        fig = go.Figure(data=[
            go.Bar(x=label,
                   y=value,
                   name="",
                   marker=dict(color=colors),
                   orientation='v',
                   text=text_labels
                   )
        ])
        st.text(f"{value_midl:.2f}")
        st.plotly_chart(fig, width="content")

    def render_plot_children(self, data: dict):
        value = list(map(lambda x: (x[0] + 1) * x[-1], tuple(enumerate(data.values()))))
        one = value[0]
        many = sum(value) - one
        label_data = ("Один ребенок", "Есть братья/сестры")
        colors = ("#ffdc33", "#3356ff")

        fig = go.Figure(data=[
            go.Bar(x=label_data,
                   y=(one, many),
                   name="",
                   marker=dict(color=colors),
                   orientation='v',
                   )
        ])
        st.plotly_chart(fig, width="content")

    def render_two_plots(self, data: dict):
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Первый график")
            self.render_plot_family(data)

        with col2:
            st.subheader("второй график")
            self.render_plot_children(data)
