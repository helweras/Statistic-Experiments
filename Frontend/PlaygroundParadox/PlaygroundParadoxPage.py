import streamlit as st
import requests
from .Plot import Plot


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

    def ratio(self):
        with st.container(border=True):
            st.markdown("### 🧐 Быстрая проверка интуиции")
            st.write(
                "Представьте город, где **90% семей** имеют всего **1 ребенка**, а остальные **10%** — по **5 детей**.")

            answer = st.radio(
                "Как вы думаете, какой процент детей в этом городе растет БЕЗ братьев и сестер?",
                ["90%", "50%", "Менее 50%"],
                index=None,
            )

            if answer:
                if answer == "Менее 50%":
                    st.success("✅ **Абсолютно верно!** Только **45%** детей будут единственными в семье.")
                    st.info("""
                        **Математика проста:** 
                        В 100 семьях будет 90 детей-одиночек и 50 детей из больших семей (10 семей * 5 детей). 
                        Итого: 90 одиночек из 140 детей ≈ **64%** имеют братьев или сестер!
                    """)
                else:
                    st.error("❌ **Не совсем так!** Кажется, что ответ 90%, но это ловушка.")
                    st.write(
                        "Хотя таких семей 90%, детей в них меньше половины от общего числа. Давайте разберем почему.")

    @st.fragment
    def config_family(self):
        with st.container(border=True):
            st.subheader("Настройка семей")
            cols = st.columns(5)
            kids_data = [
                ("1 ребенком", 55, "one"),
                ("2 детьми", 33, "two"),
                ("3 детьми", 12, "three"),
                ("4 детьми", 2, "four"),
                ("5 детьми", 1, "five")
            ]
            label_translate = {
                "one": "Один ребенок",
                "two": "Два ребенка",
                "three": "Три ребенка",
                "four": "Четыре ребенка",
                "five": "Пять детей"
            }

            family_counts = {}

            for i, (label, default, key) in enumerate(kids_data):
                rus_key = label_translate[key]
                family_counts[rus_key] = cols[i].number_input(
                    label=label,
                    min_value=0,
                    max_value=500,
                    value=default,
                    key=f"{key}_child"
                )
            self.plot.render_two_plots(family_counts)

    def render(self):
        st.markdown(self.text)
        self.ratio()
        self.config_family()

