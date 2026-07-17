import streamlit as st

from src.components.render_description import render_description_experiment
from src.state.monty_hall_state import MontyHallState
from src.api.api_monty_hall import post_simulate
from config import MontyHallEndpoints
from enum import Enum
from typing import Dict, Union, Any
from src.components.monty_hall_charts import create_explore_chart


class MontyHallExploreType(str, Enum):
    CLOSED_DOORS = "closed_doors"
    DOORS = "count_doors"
    PRIZES = "count_prizes"


MONTY_HALL_EXPLORE_CONFIGS: dict[MontyHallExploreType, dict[str, Any]] = {
    MontyHallExploreType.CLOSED_DOORS: {
        "description": "Исследуем изменение преимущества смены выбора при росте числа ЗАКРЫТЫХ дверей.",
        "description_x_chart": "Закрытые двери",
        "slider_label": "Диапазон закрытых дверей",
        "slider_min": 1,
        "slider_max": 20,
        "slider_default": (1, 10),
        # Что фиксируем в колонках c1 и c2:
        "c1_param": "count_prizes",
        "c1_label": "Фиксированные призы",
        # СТУПЕНЬ 2: Дописали пропущенные ключи для защиты от KeyError
        "c1_min": 1,
        "c1_default": 1,
        "c2_param": "count_doors",
        "c2_label": "Фиксированное общее число дверей",
        "c2_min": 3,
        "c2_default": 10,
    },
    MontyHallExploreType.DOORS: {
        "description": "Исследуем изменение преимущества смены выбора при росте ОБЩЕГО количества дверей.",
        "description_x_chart": "Двери",
        "slider_label": "Диапазон общего количества дверей (Max)",
        "slider_min": 3,
        "slider_max": 20,
        "slider_default": (3, 10),
        # Что фиксируем в колонках c1 и c2:
        "c1_param": "count_prizes",
        "c1_label": "Фиксированные призы",
        "c1_min": 1,
        "c1_default": 1,
        "c1_max": 18,
        "c2_param": "closed_doors",
        "c2_label": "Фиксированные закрытые двери ведущего",
        "c2_min": 1,
        "c2_default": 1,
        "c2_max": 19
    },
    MontyHallExploreType.PRIZES: {
        "description": "Исследуем изменение преимущества смены выбора при росте количества ПРИЗОВ.",
        "description_x_chart": "Количество призов",
        "slider_label": "Диапазон количества призов",
        "slider_min": 1,
        "slider_max": 10,
        "slider_default": (1, 5),
        # СТУПЕНЬ 3: Исправлена опечатка "total_doors" -> "count_doors" для синхронизации
        "c1_param": "count_doors",
        "c1_label": "Фиксированное общее число дверей",
        "c1_min": 3,
        "c1_default": 10,
        "c2_param": "closed_doors",
        "c2_label": "Фиксированные закрытые двери ведущего",
        "c2_min": 1,
        "c2_default": 1,
    }
}


def valid_data(data: Dict[str, list[Dict[str, Union[int, float, None]]]], index):
    test_data_batch = data["simulations"]

    for batch in test_data_batch:
        count_prizes = batch.get("count_prizes")
        closed_doors = batch.get("closed_doors")
        count_doors = batch.get("count_doors")

        # 1. Валидация на заполненность
        if (count_prizes is None) or (count_doors is None):
            st.error(f"❌ Ошибка в симуляции №{index}: Пожалуйста, заполните все поля числовыми значениями!")
            st.warning("Проблемные данные:")
            st.json(batch)  # Выводим конкретный неправильный кусочек данных
            return False

        # 2. Валидация логики (призы < дверей)
        if count_prizes >= count_doors:
            st.error(f"❌ Ошибка в симуляции №{index}: Количество призов должно быть меньше количества дверей!")
            st.warning("Проблемные данные:")
            st.json(batch)
            return False

        # 3. Математическая валидация парадокса
        if (1 + closed_doors) >= count_doors:
            st.error(
                f"❌ Ошибка в симуляции №{index}: Ведущий не может оставить закрытыми {closed_doors} дв. при общем количестве {count_doors}!")
            st.warning("Проблемные данные:")
            st.json(batch)
            return False

        # 4. Валидация призов и закрытых дверей
        if count_prizes > closed_doors:
            st.error(
                f"❌ Ошибка в симуляции №{index}: Количество призов должно быть меньше или равно количеству закрытых дверей!")
            st.warning("Проблемные данные:")
            st.json(batch)
            return False

    return True


@st.fragment
def _render_explore_generic(explore_type: MontyHallExploreType, state: MontyHallState):
    cfg = MONTY_HALL_EXPLORE_CONFIGS[explore_type]
    x_axis_description = cfg["description_x_chart"]

    with st.container(border=True):
        st.write(cfg["description"])

        # Разметка на 3 колонки
        c1, c2, c3 = st.columns(3)

        # 1. Главный слайдер исследования (Динамическая переменная)
        min_val, max_val = st.slider(cfg["slider_label"], cfg["slider_min"], cfg["slider_max"], cfg["slider_default"],
                                     key=f"slider_{explore_type.value}")

        # Колонки итераций (она всегда одинаковая во всех тестах)
        iterable = c3.select_slider("Итераций", options=[50, 75, 100, 150], value=75, key=f"it_{explore_type.value}")

        # 2. Динамическая отрисовка ФИКСИРОВАННЫХ параметров в c1 и c2
        fix_val_1 = int(
            c1.number_input(cfg["c1_label"], min_value=cfg["c1_min"], value=cfg["c1_default"], step=1,
                            key=f"fix1_{explore_type.value}"))
        fix_val_2 = int(
            c2.number_input(cfg["c2_label"], min_value=cfg["c2_min"], value=cfg["c2_default"], step=1,
                            key=f"fix2_{explore_type.value}"))

        st.markdown(f"### 🚀 Симуляция запускается в диапазоне от **{min_val}** до **{max_val}**."
                    f"Всего будет {max_val - min_val + 1} точек на графике")

        if st.button("Запустить исследование", type="primary", key=f"btn_{explore_type.value}"):
            if max_val - min_val + 1 < 5:
                st.error("Количество точек на графике должно быть 5 или больше")
                return
            data_batch = {"simulations": []}
            index = 0

            for current_step in range(min_val, max_val + 1):
                index += 1
                # Создаем пустую заготовку под итерацию
                sim_data = {"iterable": int(iterable)}

                # Заполняем динамическую переменную (ту, по которой идет цикл)
                sim_data[explore_type.value] = current_step

                # Заполняем первую фиксированную переменную из колонки c1
                sim_data[cfg["c1_param"]] = fix_val_1

                # Заполняем вторую фиксированную переменную из колонки c2
                sim_data[cfg["c2_param"]] = fix_val_2

                payload = {
                    cfg["c1_param"]: fix_val_1,
                    cfg["c2_param"]: fix_val_2,
                    explore_type.value: current_step,  # Динамический ключ пишется прямо здесь!
                    "iterable": iterable
                }

                data_for_test = {"simulations": [payload]}
                if valid_data(data_for_test, index=index):

                    data_batch["simulations"].append(payload)


            # Отправка на бэкенд FastAPI
            simulate_endpoint = MontyHallEndpoints.SIMULATE.value
            with st.spinner("Загрузка данных с бэкенда..."):
                response = post_simulate(data_batch, simulate_endpoint)

            st.success("🎉 Исследование успешно завершено!")
            state.set_explore_result(response)
        x_scatters = list(range(min_val, max_val))
        df = state.explore_df
        plot = create_explore_chart(df, x_axis_description, x_scatters=x_scatters)
        st.plotly_chart(plot)


@st.fragment
def _render_input_form(state: MontyHallState):
    """
    Отрисовывает форму Streamlit для сбора параметров эксперимента.
    """
    with st.form("input_data_form"):
        st.subheader("Параметры эксперимента")

        count_prize = st.number_input(
            label="Количество призов",
            min_value=1, max_value=30, value=1
        )

        count_doors = st.number_input(
            label="Количество дверей",
            min_value=3, max_value=99, value=3
        )

        closed_doors = st.number_input(
            label="Количество закрытых дверей",
            min_value=1, max_value=99, value=1
        )

        iterable = st.number_input(
            label="Количество итераций",
            min_value=10, max_value=1000, value=100
        )

        submitted = st.form_submit_button("Симуляция")

        if submitted:
            data = {"simulations":
                [
                    {
                        "count_prize": count_prize,
                        "count_doors": count_doors,
                        "closed_doors": closed_doors,
                        "iterable": iterable
                    }]}

            if valid_data(data, 1):
                simulate = MontyHallEndpoints.SIMULATE.value
                response = post_simulate(data, simulate)
                state.set_single_result(response)


def _render_explore_section(state: MontyHallState):
    st.markdown("---")
    st.subheader("🔬 Исследование зависимостей")

    explore_options = {
        "Количество призов": MontyHallExploreType.PRIZES,
        "Общее количество дверей": MontyHallExploreType.DOORS,
        "Количество закрытых дверей": MontyHallExploreType.CLOSED_DOORS
    }

    # Отрисовываем меню
    selected_label = st.selectbox(
        label="Выберите переменную для исследования зависимости:",
        options=list(explore_options.keys()),
        index=0,
        key="mh_explore_variable_selector",
        on_change=state.delite_explore_result()  # Привязали сброс данных
    )

    chosen_type = explore_options[selected_label]

    # Весь блок эксперимента (слайдеры, кнопка, циклы) уходит сюда:
    _render_explore_generic(explore_type=chosen_type, state=state)


def render():
    state = MontyHallState()
    render_description_experiment("Monty_Hall")
    _render_input_form(state=state)
    _render_explore_section(state=state)
