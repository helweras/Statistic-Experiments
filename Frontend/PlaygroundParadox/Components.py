import streamlit as st


def render_title():
    st.title("🔍 Лаборатория: Анализ статистического смещения")
    st.markdown("""
            Этот блок позволяет смоделировать структуру общества и увидеть, как **количественный учет семей** 
            трансформируется в **социальный опыт ребенка**.
            """)


def render_instruction():
    with st.expander("🛠 **Инструкция к эксперименту**", expanded=True):
        st.markdown("""
        1. **Загрузите реальные данные:** Введите в поля настроек цифры **55, 33, 9, 2, 1**. Это примерное распределение семей в России.
        2. **Смоделируйте дисбаланс:** Установите 100 семей с одним ребенком и добавьте всего 10 семей с пятью детьми. 
        3. **Сравните показатели:** Обратите внимание на смену соотношения сил между графиками.
        """)

    st.divider()


def render_explanations():
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


def render_katarsys():
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


def render_midl_explanations():
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


def render_finish():
    st.divider()
    with st.container(border=False):
        c1, c2 = st.columns([1, 4], vertical_alignment="center")
        c1.markdown("<h2 style='text-align: center; margin: 0;'>🎯</h2>", unsafe_allow_html=True)
        c2.markdown("""
            **Главный парадокс:** когда «Взгляд ребенка» перевешивает «Взгляд демографа», 
            общество ощущается **многодетным**, даже если сухие отчеты говорят об обратном.
        """)


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


def ratio():
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


def render_setting_family():
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
    return family_counts
