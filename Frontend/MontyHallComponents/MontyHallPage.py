import streamlit as st
import requests
from .InputForm import InputForm
from .ServiceClass import Service
from .ExploreDoors import ExploreDoors, ExploreCloseDoors, Explore


class MontyHallPage:
    prefix = "/monty_hall"
    endpoints = ("/info", "/simulate")
    url = 'https://statistic-experiments.onrender.com/'
    text = """
# 🧠 Парадокс Монти Холла

Представьте: вы на телешоу. Перед вами **три двери**. За одной скрывается **автомобиль** 🏎️, а за двумя другими — 
**козы** 🐐.

1. **Ваш выбор:** Вы указываете на одну из дверей (например, №1). Шанс угадать сразу — всего **1/3**.
2. **Ход ведущего:** Монти Холл знает, где спрятан приз. Он открывает одну из оставшихся дверей (например, №3) и 
показывает там **козу**.
3. **Момент истины:** Ведущий спрашивает: *«Желаете ли вы изменить свой выбор и выбрать дверь №2?»*

---

### 📊 Математический секрет
Большинство людей думает, что шансы теперь 50/50, но это не так. **Вам выгодно сменить дверь!**

* **Почему?** Когда вы выбирали в первый раз, вы ошиблись с вероятностью **2/3**. 
* Ведущий своим действием «отфильтровал» один ложный вариант. 
* В итоге все те **2/3 вероятности** ошибки при первом выборе теперь перешли на оставшуюся закрытую дверь.

> **Итог:** Оставаясь при своем выборе, вы побеждаете в **33%** случаев. Меняя дверь — в **66%**.
"""
    text_description = """
---
### 🧪 Запустите свою симуляцию

Проверьте, как меняется математика игры при разных условиях! Попробуйте настроить количество дверей, призов и 
открытых вариантов.

> 💡 **Классический случай:** 1 приз, 3 двери и 1 открытая ведущим — это база, где шансы при смене выбора удваиваются.

**Готовы настроить свои параметры и увидеть магию чисел?** 👇
"""
    text_validation = """
                                                        **Требования для запуска:**
                                                        * Все числа должны быть **больше 0**.
                                                        * Общее число дверей должно быть **минимум на 2 больше**, чем количество призов.
                                                        * Ведущий должен закрыть **не меньше**, чем количество призов, 
                                                        но **не все** оставшиеся двери.
                                                        """
    input_form = InputForm()
    service = Service()

    explore_doors = ExploreDoors()
    explore_close_doors = ExploreCloseDoors()

    # Реестр классов экспериментов (не экземпляров!)
    EXPERIMENTS = {
        "Количество дверей": ExploreDoors,
        "Количество закрытых дверей": ExploreCloseDoors,
        "Количество призов": None,
    }

    def get_info(self):
        response = requests.get(self.get_url(0))
        return response.json()['rules']

    def get_url(self, end):
        return self.url + self.prefix + self.endpoints[end]

    def post_request(self, data: dict, url):
        response = requests.post(self.get_url(1), json=data, timeout=20)
        return response.json()

    def check_response(self, response):
        if response["status"] == "Good":
            return True
        st.error(response['msg'])
        st.info(self.text_validation)
        return False

    def check_data_set(self, data_set):
        if data_set is not None:
            return True
        return False

    @st.fragment
    def research_mode(self):
        st.subheader("🚀Масштабирование")

        if "data_set" not in st.session_state:
            st.session_state.data_set = None

        scenario = self.select_params()
        if scenario:
            experiment: Explore = self.EXPERIMENTS[scenario]()
            experiment.explore(self.get_url(1), text_validation=self.text_validation)

        # Настройки внутри фрагмента


    def select_params(self):
        scenario = st.selectbox(
            label="Выберете зависимую переменную",
            options=list(self.EXPERIMENTS.keys()),
            key="scenario_select",  # Уникальный ключ для фрагмента
            index=None,
            placeholder="Нажмите сюда"
        )
        return scenario

    def start_simulate(self, data):
        response = self.service.post_request(data, url=self.get_url(1))
        with st.expander("Посмотреть сырые данные от сервера"):
            st.json(response)
        if self.check_response(response):
            result = response["data"]["Customizable"]

            stay_rate = result['Stay']
            switch_rate = result['Change']

            col1, col2 = st.columns(2)
            col1.metric("Побед при смене выбора", f"{switch_rate:.1f}%", f"{switch_rate - 50:.1f}%")
            col2.metric("Побед без смены", f"{stay_rate:.1f}%", f"{stay_rate - 50:.1f}%")

    def render(self):
        st.write(self.text)
        st.markdown(self.get_info())
        st.markdown(self.text_description)
        data = self.input_form.get_data()
        if data:
            self.start_simulate(data)

        self.research_mode()
