import plotly.graph_objects as go
import pandas as pd


def create_explore_chart(df: pd.DataFrame, x_axis_description: str, x_scatters:list[int]) -> go.Figure:
    if df.empty:
        fig = go.Figure()
        return fig

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_scatters,
        y=df["Change"],  # Точное имя колонки винрейта при смене двери из вашего JSON
        name="Смена выбора 🟢",
        mode="lines+markers",  # Линия + точки на графике
        line=dict(color="#00CC96", width=3),  # Зеленый цвет линии
        marker=dict(size=8)
    ))

    fig.add_trace(go.Scatter(
        x=x_scatters,
        y=df["Stay"],  # Точное имя колонки винрейта без смены двери из вашего JSON
        name="Оставить выбор 🔴",
        mode="lines+markers",
        line=dict(color="#EF553B", width=3),  # Красный цвет линии
        marker=dict(size=8)
    ))

    # 4. Настраиваем внешний вид (сетка, оси, заголовки)
    fig.update_layout(
        title="<b>🔬 Анализ изменения процента побед</b>",
        xaxis_title=f"Изменяемый параметр: {x_axis_description}",
        yaxis_title="Процент побед (%)",
        hovermode="x unified",  # Подсказка показывается для обеих линий сразу при наведении
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),  # Горизонтальная легенда сверху
        height=450
    )

    fig.update_yaxes(range=[0, 100], showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')

    return fig
