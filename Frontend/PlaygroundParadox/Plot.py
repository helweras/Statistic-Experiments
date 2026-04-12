import plotly.graph_objects as go
import streamlit as st


class Plot:
    def render_plot_family(self, data: dict):
        colors = ["#1fcecb", "#731fce", "#ce1f22", "#7ace1f", "#cecb1f"]
        label = list(data.keys())
        value = list(data.values())
        total = sum(value)
        value = list(map(lambda x: x / total * 100, value))
        text_labels = [f"{v:.1f}%" for v in value]
        fig = go.Figure(data=[
            go.Bar(x=label,
                   y=value,
                   name="",
                   marker=dict(color=colors),
                   orientation='v',
                   text=text_labels
                   )
        ])

        fig.update_layout(yaxis_title="Доля семей (%)", yaxis=dict(range=[0, 100]), height=400)
        st.plotly_chart(fig, width="content")

    def render_plot_children(self, data: dict):
        value = list(map(lambda x: (x[0] + 1) * x[-1], tuple(enumerate(data.values()))))
        total_kids = sum(value)
        one_kid_perc = round(value[0] / total_kids * 100, 1)
        many_kids_perc = round((total_kids - value[0]) / total_kids * 100, 1)
        label_data = ("Один ребенок", "Есть братья/сестры")

        colors = ("#ffdc33", "#3356ff")

        fig = go.Figure(data=[
            go.Bar(x=label_data,
                   y=(one_kid_perc, many_kids_perc),
                   name="",
                   marker=dict(color=colors),
                   orientation='v',
                   text=[f"{t}%" for t in (one_kid_perc, many_kids_perc)]
                   )
        ])
        fig.update_layout(yaxis_title="Доля детей (%)", yaxis=dict(range=[0, 100]), height=400)
        st.plotly_chart(fig, width="content")



    def render_two_plots(self, data: dict):
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Первый график")
            self.render_plot_family(data)

        with col2:
            st.subheader("Второй график")
            self.render_plot_children(data)
