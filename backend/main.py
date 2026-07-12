from fastapi import FastAPI
from src.api.v1.api import router as exp01_router
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Симулятор Парадоксов API",
    description="Бэкенд для симуляции математических и вероятностных парадоксов",
    version="1.0.0"
)

origins = [
    "http://localhost:8501",
    "http://127.0.0.1:8501",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Разрешает POST, GET и т.д.
    allow_headers=["*"],
)

app.include_router(exp01_router, prefix="/api/v1")

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    # Вариант А: Перенаправляем сразу в Swagger (очень удобно при разработке)
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)