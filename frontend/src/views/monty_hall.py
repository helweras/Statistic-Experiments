import streamlit as st
from src.components.render_description import render_description_experiment
from src.state.monty_hall_state import MontyHallState
from src.api.api_monty_hall import post_simulate
from config import MontyHallEndpoints
from enum import Enum
from typing import Dict, Union

def _render_explore(state: MontyHallState):
    with st.container(border=True):
        st.write("Выясним, как меняется преимущество смены выбора с увеличением общего числа закрытых дверей.")
        # 1. Блок ввода параметров
        c1, c2, c3 = st.columns(3)
        range_close_doors = st.slider("Диапазон закрытых количество дверей", 6, 20, (6, 10))
        min_close_doors, max_close_doors = range_close_doors
        iterable = c3.select_slider("Итераций", options=[50, 75, 100, 150], value=75)
        count_doors = c2.number_input("Количество дверей", max_close_doors + 2, 22, max_close_doors + 2)
        count_prize = c1.number_input("Количество призов", 1, min_close_doors, 1)
        st.markdown(f"### 🚀 Симуляция стартует с **{min_close_doors}** и до **{max_close_doors}** закрытых дверей.")
        if st.button("Запустить исследование", type="primary"):
            data_batch = {"simulations": []}
            start_range = int(min_close_doors) if min_close_doors is not None else 1
            end_range = int(max_close_doors) if max_close_doors is not None else 10
            for close_doors in range(start_range, end_range + 1):
                data = {
                    "count_prize": count_prize,
                    "count_doors": count_doors,
                    "closed_doors": close_doors,
                    "iterable": iterable
                }
                data_batch["simulations"].append(data)
            simulate = MontyHallEndpoints.SIMULATE.value
            response = post_simulate(data_batch, simulate)
            state.set_explore_result(response)



class MontyHallExploreType(str, Enum):
    CLOSED_DOORS = "closed_doors"
    DOORS = "count_doors"
    PRIZES = "count_prizes"


MONTY_HALL_EXPLORE_CONFIGS = {
    MontyHallExploreType.CLOSED_DOORS: {
        "description": "Исследуем изменение преимущества смены выбора при росте числа ЗАКРЫТЫХ дверей.",
        "slider_label": "Диапазон закрытых дверей",
        # Что фиксируем в колонках c1 и c2:
        "c1_param": "prizes",
        "c1_label": "Фиксированные призы",
        "c2_param": "total_doors",
        "c2_label": "Фиксированное общее число дверей",
    },
    MontyHallExploreType.DOORS: {
        "description": "Исследуем изменение преимущества смены выбора при росте ОБЩЕГО количества дверей.",
        "slider_label": "Диапазон общего количества дверей (Max)",
        # Что фиксируем в колонках c1 и c2:
        "c1_param": "prizes",
        "c1_label": "Фиксированные призы",
        "c2_param": "closed_doors",
        "c2_label": "Фиксированные закрытые двери ведущего",
    },
    MontyHallExploreType.PRIZES: {
        "description": "Исследуем изменение преимущества смены выбора при росте количества ПРИЗОВ.",
        "slider_label": "Диапазон количества призов",
        "slider_min": 1,
        "slider_max": 10,
        "slider_default": (1, 5),
        # Настройки ФИКСИРОВАННОГО поля в c1 (Все двери)
        "c1_param": "total_doors",
        "c1_label": "Фиксированное общее число дверей",
        "c1_min": 3,
        "c1_default": 10,
        # Настройки ФИКСИРОВАННОГО поля в c2 (Закрытые двери)
        "c2_param": "closed_doors",
        "c2_label": "Фиксированные закрытые двери ведущего",
        "c2_min": 1,
        "c2_default": 1,
    }
}



def valid_data(data: Dict[str, list[Dict[str, Union[int, float, None]]]], index):
    test_data_batch = data["simulations"]

    for batch in test_data_batch:
        count_prize = batch.get("count_prize")
        closed_doors = batch.get("closed_doors")
        count_doors = batch.get("count_doors")

        # 1. Валидация на заполненность
        if count_prize is None or count_doors is None:
            st.error(f"❌ Ошибка в симуляции №{index}: Пожалуйста, заполните все поля числовыми значениями!")
            st.warning("Проблемные данные:")
            st.json(batch)  # Выводим конкретный неправильный кусочек данных
            return False

        # 2. Валидация логики (призы < дверей)
        if count_prize >= count_doors:
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
        if count_prize > closed_doors:
            st.error(
                f"❌ Ошибка в симуляции №{index}: Количество призов должно быть меньше или равно количеству закрытых дверей!")
            st.warning("Проблемные данные:")
            st.json(batch)
            return False

    return True


def _render_explore_generic(explore_type: MontyHallExploreType, state: MontyHallState):
    cfg = MONTY_HALL_EXPLORE_CONFIGS[explore_type]

    with st.container(border=True):
        st.write(cfg["description"])

        # Разметка на 3 колонки
        c1, c2, c3 = st.columns(3)

        # 1. Главный слайдер исследования (Динамическая переменная)
        # Он всегда определяет верхнюю границу диапазона (max_val)
        min_val, max_val = st.slider(cfg["slider_label"], cfg["slider_min"], cfg["slider_max"], cfg["slider_default"],
                                     key=f"slider_{explore_type.value}")

        # Колонки итераций (она всегда одинаковая во всех тестах)
        iterable = c3.select_slider("Итераций", options=[50, 75, 100, 150], value=75, key=f"it_{explore_type.value}")

        # 2. Динамическая отрисовка ФИКСИРОВАННЫХ параметров в c1 и c2
        # Мы не знаем заранее, что там будет, пока не заглянем в cfg
        fix_val_1 = int(
            c1.number_input(cfg["c1_label"], min_value=cfg["c1_min"], value=cfg["c1_default"], step=1,
                            key=f"fix1_{explore_type.value}"))
        fix_val_2 = int(
            c2.number_input(cfg["c2_label"], min_value=cfg["c2_min"], value=cfg["c2_default"], step=1,
                            key=f"fix2_{explore_type.value}"))

        st.markdown(f"### 🚀 Симуляция запускается в диапазоне от **{min_val}** до **{max_val}**."
                    f"Всего будет {max_val-min_val+1} точек на графике")

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

                # Приводим ключи словаря к именам, которые строго ожидает Pydantic на бэкенде:
                # На бэкенде поля называются count_prize и count_doors, а в Enum у нас prizes и total_doors
                payload = {
                    cfg["c1_param"]: fix_val_1,
                    cfg["c2_param"]: fix_val_2,
                    explore_type.value: current_step,  # Динамический ключ пишется прямо здесь!
                    "iterable": iterable
                }


                data_for_test = {"simulations": [payload]}
                if valid_data(data_for_test, index=index):

                    data_batch["simulations"].append(payload)
                else:
                    return

            # Отправка на бэкенд FastAPI
            print(data_batch)
            simulate_endpoint = MontyHallEndpoints.SIMULATE.value
            with st.spinner("Загрузка данных с бэкенда..."):
                response = post_simulate(data_batch, simulate_endpoint)

            st.success("🎉 Исследование успешно завершено!")
            state.set_explore_result(response)
            st.text(state.explore_df)
            st.rerun()


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


def render():
    state = MontyHallState()
    render_description_experiment("Monty_Hall")
    _render_input_form(state=state)
    _render_explore_generic(MontyHallExploreType.PRIZES, state)
