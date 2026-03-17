import streamlit as st
from .Explore import Explore


class ExploreCloseDoors(Explore):
    field_name = "Закрытые двери"
    const = 1

    def explore(self, url, text_validation):
        with st.container(border=True):
            st.write("Выясним, как растет преимущество смены выбора с увеличением общего числа закрытых дверей.")
            # 1. Блок ввода параметров
            c1, c2, c3 = st.columns(3)
            max_close_doors = st.slider("Конечное закрытых количество дверей", 6, 20, 10)
            min_close_doors = st.number_input("Начальное количество закрытых дверей", 1, max_close_doors - 5, 1)
            it = c3.select_slider("Итераций", options=[50, 75, 100, 150], value=75)
            doors = c2.number_input("Количество дверей", max_close_doors + 2, 22, max_close_doors + 2)
            prize = c1.number_input("Количество призов", 1, min_close_doors, 1)
            st.markdown(f"### 🚀 Симуляция стартует с **{min_close_doors}** и до **{max_close_doors}** закрытых дверей.")

            # 2. Кнопка запуска
            if st.button("Запустить масштабное исследование", type="primary"):
                results = self.run_simulation(prize=prize,
                                              max_close_doors=max_close_doors,
                                              doors=doors, it=it,
                                              url=url,
                                              text_validation=text_validation,
                                              min_close_doors=min_close_doors)

                if results:
                    st.session_state.data_set = results
            if st.session_state.data_set is not None:
                self.process_and_render_results()

    def run_simulation(self, min_close_doors, prize, max_close_doors, doors, it, text_validation, url):
        """Бизнес-логика: сбор данных через API."""
        data_set = []
        # Валидация всех шагов перед запуском
        for close_doors in range(min_close_doors, max_close_doors + 1):
            response_valid_test = self.valid_input_data(prize, doors, close_doors)
            if not response_valid_test["status"]:
                st.error(response_valid_test["text"])
                return None

        status_text = st.empty()
        for close_doors in range(min_close_doors, max_close_doors + 1):
            status_text.text(f"⏳ Симуляция для {close_doors} закрытых дверей...")
            payload = {
                "count_prize": prize,
                "count_doors": doors,
                "closed_doors": close_doors,
                "iterable": it
            }
            response = self.service.post_request(payload, url)

            if self.service.check_response(response):
                theory_data = self.get_theory(doors=doors, prize=prize, closed=close_doors)
                response["data"]["Customizable"].update(theory_data)
                data_set.append(response["data"]["Customizable"])
            else:
                return None
        return data_set
