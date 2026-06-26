from pydantic import BaseModel
from typing import List

# Схема для одного эксперимента
class ExperimentInfo(BaseModel):
    id: str
    title: str
    description: str
    complexity: str  # Можно заменить на Enum (Easy, Medium, Hard)
    route: str       # Путь на фронтенде (Streamlit)

# Схема для списка (удобно для ответа API)
class ExperimentList(BaseModel):
    experiments: List[ExperimentInfo]

# Сами данные
EXPERIMENTS_DATA = [
    ExperimentInfo(
        id="monty-hall",
        title="Парадокс Монти Холла",
        description="Вероятностная задача о трех дверях.",
        complexity="Easy",
        route="/monty-hall"
    ),
    ExperimentInfo(
        id="playground-paradox",
        title="Парадокс детской площадки",
        description="Анализ семейного состава и вероятностей.",
        complexity="Medium",
        route="/playground-paradox"
    )
]

EXPERIMENTS_RESPONSE = ExperimentList(experiments=EXPERIMENTS_DATA)