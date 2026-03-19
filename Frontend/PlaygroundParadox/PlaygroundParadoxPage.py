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

    def render_title(self):
        st.title("🔍 Лаборатория: Анализ статистического смещения")
        st.markdown("""
                Этот блок позволяет смоделировать структуру общества и увидеть, как **количественный учет семей** 
                трансформируется в **социальный опыт ребенка**.
                """)

    def render_instruction(self):
        with st.expander("🛠 **Инструкция к эксперименту**", expanded=True):
            st.markdown("""
            1. **Загрузите реальные данные:** Введите в поля настроек цифры **55, 33, 9, 2, 1**. Это примерное распределение семей в России.
            2. **Смоделируйте дисбаланс:** Установите 100 семей с одним ребенком и добавьте всего 10 семей с пятью детьми. 
            3. **Сравните показатели:** Обратите внимание на смену соотношения сил между графиками.
            """)

        st.divider()

    def render_explanations(self):
        st.subheader("📊 Разница в методах подсчета")
        col1, col2 = st.columns(2)

        with col1:
            st.info("**Распределение по семьям** (Слева)")
            st.caption("""
                    Отражает отчеты демографов. Единица измерения — **семья**. 
                    Каждая семья распределена по количеству детей.
                    """)

        with col2:
            st.success("**Распределение по детям** (Справа)")
            st.caption("""
                    Отражает состав условного школьного класса. Единица измерения — **ребенок**. 
                    Семья из 5 детей представлена пятью участниками, усиливая свое влияние в 5 раз.
                    """)
        st.divider()

    def render_katarsys(self):
        st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 20px; border-left: 5px solid #ff4b4b; border-radius: 5px;">
            <h4 style="margin-top: 0;">✨ Момент фиксации парадокса</h4>
            <p style="font-style: italic; font-size: 1.1em;">
                "В обществе малодетных семей дети могут расти в преимущественно <b>многодетной среде</b>."
            </p>
            <hr>
            <small>Это происходит, когда доля единственных детей в выборке падает ниже 50% за счет веса больших семей.</small>
        </div>
        """, unsafe_allow_html=True)

    def midl_explanations(self):
        with st.container(border=False):
            st.subheader("🧮 Почему средние числа разные?")

            col_a, col_b = st.columns(2)

            with col_a:
                st.markdown("**Взгляд демографа**")
                st.caption("""
                Считаем **семьи**. Если есть 1 семья с 5 детьми и 4 семьи с 1 ребенком — среднее **1.8**.  
                *Это сухая статистика рождаемости.*
                """)

            with col_b:
                st.markdown("**Взгляд ребенка****")
                st.caption("""
                Считаем **детей**. Из 9 детей пятеро скажут: «нас в семье много». Среднее по их ответам — **3.2**.  
                *Это реальное окружение ребенка.*
                """)

            st.info(
                "Разрыв возникает, потому что голос одного многодетного родителя в мире детей звучит в 5 раз громче.")

    def render_finish(self):
        st.divider()
        with st.container(border=False):
            c1, c2 = st.columns([1, 4], vertical_alignment="center")
            c1.markdown("<h2 style='text-align: center; margin: 0;'>🎯</h2>", unsafe_allow_html=True)
            c2.markdown("""
                **Главный парадокс:** когда «Взгляд ребенка» перевешивает «Взгляд демографа», 
                общество ощущается **многодетным**, даже если сухие отчеты говорят об обратном.
            """)


    def midl_metric(self, data: dict):
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
            self.render_title()
            self.render_instruction()
            st.subheader("Настройка семей")
            cols = st.columns(5)
            kids_data = [
                ("1 ребенком", 55, "one"),
                ("2 детьми", 33, "two"),
                ("3 детьми", 9, "three"),
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
            self.render_katarsys()
            self.plot.render_two_plots(family_counts)
            self.render_explanations()
            self.midl_metric(family_counts)
            self.midl_explanations()
            self.render_finish()

    def render(self):
        st.markdown(self.text)
        self.ratio()
        self.config_family()
