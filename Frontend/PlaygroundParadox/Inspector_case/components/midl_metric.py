import streamlit as st


def render_midl_metric(data: dict):
    midl_ratio_family = sum(list(
        map(
            lambda x: ((x[0] + 1) * x[-1]),
            tuple(enumerate(data.values()))
        )
    )
    ) / sum(tuple(data.values()))

    value = list(map(lambda x: (x[0] + 1) * x[-1], tuple(enumerate(data.values()))))
    total_kids = sum(value)
    midl_ratio_kids = round(sum(map(lambda x: (x[0] + 1) * x[-1], tuple(enumerate(value)))) / total_kids, 2)

    with st.container(border=True):
        st.subheader("Как посчитать среднее число детей?")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("🏠 **Опросить семьи**")
            st.caption("Взгляд демографа: считаем по семьям.")
        with col2:
            st.markdown("👦 **Опросить детей**")
            st.caption("Взгляд социолога: считаем личный опыт.")

        col1, col2 = st.columns(2)
        col1.metric("Среднее значение при опросе семей", f"{midl_ratio_family:.2f} реб.")
        col2.metric("Среднее значение при опросе детей", f"{midl_ratio_kids:.2f} реб.",
                    f"{midl_ratio_kids - midl_ratio_family:.2f}")
