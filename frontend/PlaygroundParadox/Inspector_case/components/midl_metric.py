import streamlit as st
from typing import Dict


def render_midl_metric(data: Dict[str, float]) -> None:
    """
    Рассчитывает и отображает метрики среднего количества детей двумя способами.

    Функция вычисляет:
    1. Среднее число детей на одну семью (демографический подход).
    2. Средний размер семьи, в которой живет ребенок (социологический подход/парадокс дружбы).

    Args:
        data (Dict[str, float]): Словарь, где ключ — описание категории,
            а значение — вес или количество семей.
    """

    # Извлекаем веса (количества семей) в список для расчетов
    family_counts = list(data.values())

    # 1. Расчет для семей (Демографический взгляд)
    # Сумма (номер_категории * количество_семей) / общее_количество_семей
    total_kids_in_families = sum((i + 1) * count for i, count in enumerate(family_counts))
    total_families = sum(family_counts)

    midl_ratio_family = total_kids_in_families / total_families if total_families > 0 else 0

    # 2. Расчет для детей (Социологический взгляд)
    # Здесь мы считаем "среднее количество братьев/сестер + 1" для каждого ребенка
    # Вес каждой категории теперь определяется общим числом детей в этой категории
    kids_distribution = [(i + 1) * count for i, count in enumerate(family_counts)]
    total_kids = sum(kids_distribution)

    # Сумма (количество_детей_в_категории * размер_этой_семьи) / общее_число_детей
    weighted_kids_sum = sum((i + 1) * kids for i, kids in enumerate(kids_distribution))
    midl_ratio_kids = round(weighted_kids_sum / total_kids, 2) if total_kids > 0 else 0

    # Отрисовка интерфейса
    with st.container(border=True):
        st.subheader("Как посчитать среднее число детей?")

        # Описательные блоки
        head_col1, head_col2 = st.columns(2)
        with head_col1:
            st.markdown("🏠 **Опросить семьи**")
            st.caption("Взгляд демографа: считаем по семьям.")
        with head_col2:
            st.markdown("👦 **Опросить детей**")
            st.caption("Взгляд социолога: считаем личный опыт.")

        # Метрики
        met_col1, met_col2 = st.columns(2)

        met_col1.metric(
            label="Среднее значение (семьи)",
            value=f"{midl_ratio_family:.2f} реб."
        )

        met_col2.metric(
            label="Среднее значение (дети)",
            value=f"{midl_ratio_kids:.2f} реб.",
            delta=f"{midl_ratio_kids - midl_ratio_family:.2f}"
        )
