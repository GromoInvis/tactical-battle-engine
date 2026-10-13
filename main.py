"""
main.py
Точка входу FastAPI: ініціалізація, моніторинг та підключення роутерів.
"""
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.routers import character, dungeon

app = FastAPI(
    title="Alonar Game API",
    description="Модульний бекенд покрокової RPG у стилі Alonar",
    version="1.0.0"
)

# Метрики
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Підключення роутерів
app.include_router(character.router)
app.include_router(dungeon.router)


@app.get("/health", tags=["Monitoring"])
def health_check():
    return {"status": "healthy", "service": "alonar-game"}