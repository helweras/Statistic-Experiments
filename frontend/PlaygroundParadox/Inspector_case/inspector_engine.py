import streamlit as st
from .components import (
    render_description,
    render_explanations,
    render_finish,
    render_head,
    render_instruction,
    render_midl_explanations,
    render_midl_metric,
    render_ratio,
    render_select_part,
    render_setting_family,
    render_title
)
from ..Plot import Plot


class InspectorCase:
    """Класс для управления логикой и визуализацией кейса 'Парадокс инспектора'.

    Данный класс координирует отображение интерфейса, настройку параметров
    распределения семей и отрисовку графиков через соответствующие компоненты.

    Attributes:
        plot (Plot): Экземпляр класса Plot для визуализации графиков.
    """

    plot = Plot()

    @st.fragment
    def config_family(self):
        """Отрисовывает интерактивную часть конфигурации семейного состава.

        Метод обернут в `st.fragment`, что позволяет обновлять состояние
        графиков и метрик без полной перезагрузки страницы приложения.

        Выполняет:
            - Вывод заголовка и инструкции.
            - Сбор данных из виджетов настроек.
            - Отрисовку сравнительных графиков.
            - Вывод пояснений и расчетных метрик.
        """
        with st.container(border=True):
            render_title()
            render_instruction()

            # Получение данных о распределении семей
            data = render_setting_family()

            # Визуализация данных
            self.plot.render_two_plots(data)

            render_explanations()
            render_midl_metric(data)
            render_midl_explanations()
            render_finish()

    def render(self):
        """Точка входа для отрисовки всей страницы кейса.

        Метод последовательно выводит статическое описание, вводные данные
        и вызывает фрагмент для динамической настройки эксперимента.
        """
        render_description()
        render_ratio()
        self.config_family()
