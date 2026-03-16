import streamlit as st
from .Explore import Explore


class ExplorePrize(Explore):
    field_name = "Призы"
    const = 1

    def explore(self, url, text_validation):
        with st.container(border=True):
            st.write("Выясним, как растет преимущество смены выбора с увеличением общего числа призов.")
            # 1. Блок ввода параметров
            c1, c2, c3 = st.columns(3)
            max_prize = st.slider("Конечное количество призов", 6, 20, 10)
            min_prize = st.number_input("Начальное количество призов", 1, max_prize - 5, 1)
            it = c3.select_slider("Итераций", options=[50, 75, 100, 150], value=75)
            doors = c2.number_input("Количество дверей", max_prize + 2, 22, max_prize + 2)
            close_doors = c1.number_input("Количество закрытых дверей", max_prize, doors - 2, max_prize)
            st.markdown(f"### 🚀 Симуляция стартует с **{min_prize}** и до **{max_prize}** призов.")

            # 2. Кнопка запуска
            if st.button("Запустить масштабное исследование", type="primary"):
                results = self.run_simulation(max_prize=max_prize,
                                              min_prize=min_prize,
                                              doors=doors,
                                              it=it,
                                              url=url,
                                              text_validation=text_validation,
                                              close_doors=close_doors)

                if results:
                    st.session_state.data_set = results
            if st.session_state.data_set is not None:
                self.process_and_render_results()

    def run_simulation(self, min_prize, close_doors, max_prize, doors, it, text_validation, url):
        """Бизнес-логика: сбор данных через API."""
        data_set = []
        # Валидация всех шагов перед запуском
        for prize in range(min_prize, max_prize + 1):
            response_valid_test = self.valid_input_data(prize, doors, close_doors)
            if not response_valid_test["status"]:
                st.error(response_valid_test["text"])
                return None

        status_text = st.empty()
        for prize in range(min_prize, max_prize + 1):
            status_text.text(f"⏳ Симуляция для {prize} призов...")
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
