import streamlit as st
from .Explore import Explore
import asyncio
import httpx


class ExploreDoors(Explore):
    field_name = "двери"
    const = 3

    async def fetch_door_data(self, client, door, prize, close_doors, it, url):
        """Отдельная асинхронная задача для одной двери"""
        payload = {
            "count_prize": prize,
            "count_doors": door,
            "closed_doors": close_doors,
            "iterable": it
        }

        # Асинхронный POST запрос
        response = await client.post(url, json=payload, timeout=30.0)

        if response.status_code == 200:
            data = response.json()
            # Добавляем теоретические данные (твоя функция get_theory)
            theory_data = self.get_theory(doors=door, prize=prize, closed=close_doors)
            data["data"]["Customizable"].update(theory_data)
            return data["data"]["Customizable"]
        else:
            return None

    async def run_simulation_async(self, start_door, prize, end_doors, close_doors, it, url):
        """Основной цикл, запускающий все запросы разом"""

        # 1. Валидация (оставляем как есть, это быстро)
        for door in range(start_door, end_doors + 1):
            res_valid = self.valid_input_data(prize, door, close_doors)
            if not res_valid["status"]:
                st.error(res_valid["text"])
                return None

        status_text = st.empty()
        status_text.text("🚀 Запуск параллельных симуляций...")

        # 2. Создаем список задач (tasks)
        tasks = []
        # Используем AsyncClient для эффективных соединений
        async with httpx.AsyncClient() as client:
            for door in range(close_doors + 2, end_doors + 1):
                # Создаем "задание", но пока не запускаем его
                task = self.fetch_door_data(client, door, prize, close_doors, it, url)
                tasks.append(task)

            # 3. МАГИЯ: Запускаем все задачи ОДНОВРЕМЕННО
            # gather вернет список результатов в том же порядке
            data_set = await asyncio.gather(*tasks)

        status_text.text("✅ Расчеты завершены!")
        # Фильтруем None, если какие-то запросы упали
        return [d for d in data_set if d is not None]

    def explore(self, url, text_validation):
        with st.container(border=True):
            st.write("Выясним, как растет преимущество смены выбора с увеличением общего числа дверей.")

            # 1. Блок ввода параметров
            c1, c2, c3 = st.columns(3)
            max_doors = st.slider(label="Конечное количество дверей",
                                  min_value=8,
                                  max_value=20,
                                  value=10,
                                  key="max_doors"
                                  )
            min_doors = st.number_input(label="Начальное количество дверей",
                                        min_value=3,
                                        max_value=max_doors - 5,
                                        value=3,
                                        key="min_doors"
                                        )
            close_doors = c2.number_input("Количество закрытых дверей", 1, min_doors - 2, 1, key="close_doors")
            it = c3.select_slider("Итераций", options=[50, 75, 100, 150], value=75)

            prize = c1.number_input("Количество призов", 1, close_doors, 1, key="prize")
            st.markdown(f"### 🚀 Симуляция стартует с **{min_doors}** и до **{max_doors}** дверей.")

            # 2. Кнопка запуска
            if st.button("Запустить масштабное исследование", type="primary"):
                results = self.run_simulation(start_door=min_doors,
                                              end_doors=max_doors,
                                              prize=prize,
                                              close_doors=close_doors,
                                              it=it,
                                              url=url
                                              )

                if results:
                    st.session_state.data_set = results
            if st.session_state.data_set is not None:
                self.process_and_render_results()

    def run_simulation(self, start_door, prize, end_doors, close_doors, it, url):
        """Бизнес-логика: сбор данных через API."""
        data_set = []
        # Валидация всех шагов перед запуском
        for door in range(start_door, end_doors + 1):
            response_valid_test = self.valid_input_data(prize, door, close_doors)
            if not response_valid_test["status"]:
                st.error(response_valid_test["text"])
                return None

        status_text = st.empty()
        for door in range(close_doors + 2, end_doors + 1):
            status_text.text(f"⏳ Симуляция для {door} дверей...")
            payload = {
                "count_prize": prize,
                "count_doors": door,
                "closed_doors": close_doors,
                "iterable": it
            }
            response = self.service.post_request(payload, url)

            if self.service.check_response(response):
                theory_data = self.get_theory(doors=door, prize=prize, closed=close_doors)
                response["data"]["Customizable"].update(theory_data)
                data_set.append(response["data"]["Customizable"])
            else:
                return None
        return data_set
