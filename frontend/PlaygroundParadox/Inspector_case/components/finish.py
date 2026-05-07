import streamlit as st


def render_finish():
    st.divider()
    with st.container(border=False):
        c1, c2 = st.columns([1, 4], vertical_alignment="center")
        c1.markdown("<h2 style='text-align: center; margin: 0;'>🎯</h2>", unsafe_allow_html=True)
        c2.markdown("""
            **Главный парадокс:** когда «Взгляд ребенка» перевешивает «Взгляд демографа», 
            общество ощущается **многодетным**, даже если сухие отчеты говорят об обратном.
        """)
