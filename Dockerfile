# Базовий шар: беремо легкий офіційний образ Python 3.11 Debian Slim (~120 МБ)
FROM python:3.11-slim

# Робоча директорія всередині контейнера для всіх подальших інструкцій
WORKDIR /app

# Встановлюємо curl для перевірки здоров'я контейнера (healthcheck)
# apt-get update && apt-get install -y: встановлення без інтерактивних запитів
# rm -rf /var/lib/apt/lists/*: очищення списків пакетів, щоб зменшити вагу образу
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Копіюємо файл залежностей requirements.txt окремим шаром для кешування
COPY requirements.txt .

# Встановлюємо залежності без збереження кешу завантажень pip
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо решту файлів проєкту в робочу папку /app
COPY . .

# HEALTHCHECK: регулярна перевірка доступності нашого API всередині контейнера
# --interval=10s: робити перевірку кожні 10 секунд
# --timeout=3s: вважати спробу невдалою, якщо відповіді немає довше 3 секунд
# --start-period=5s: час на перший старт додатку (щоб не вважати його зламаним при запуску)
# --retries=3: кількість невдалих спроб перед тим, як статус зміниться на unhealthy
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Команда запуску FastAPI сервера через Uvicorn на всіх інтерфейсах (0.0.0.0)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]