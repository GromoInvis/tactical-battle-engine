# ⚔️ Tactical Battle Engine

[![Battle Engine CI/CD](https://github.com/GromoInvis/tactical-battle-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/GromoInvis/tactical-battle-engine/actions/workflows/ci.yml)

Високопродуктивний мікросервіс тактичних бойових розрахунків на базі **FastAPI**, спроєктований за сучасними стандартами **DevOps**: мультиконтейнерна архітектура, ізоляція через зворотний проксі, безперервна інтеграція та доставка (CI/CD), керування інфраструктурою як кодом (IaC) та спостережуваність (Observability).

---

## 🛠 Технологічний стек

* **Бекенд:** Python 3.11, FastAPI, Pydantic, Uvicorn
* **Тестування:** Pytest, HTTPX
* **База даних:** PostgreSQL 15 (Alpine)
* **Зворотний проксі:** Nginx (Alpine)
* **Контейнеризація:** Docker, Docker Compose
* **CI/CD:** GitHub Actions, GitHub Container Registry (`ghcr.io`)
* **IaC:** Terraform (Docker Provider)
* **Моніторинг:** Prometheus (`prometheus-fastapi-instrumentator`)

---

## 🏗 Архітектура системи

1. **Nginx (Reverse Proxy):** слухає зовнішній HTTP-порт `80`, забезпечує проксування запитів, приховує внутрішню мережу та прокидає оригінальні клієнтські заголовки (`Host`, `X-Real-IP`).
2. **FastAPI Engine:** бойовий рушій, що працює на внутрішньому порту `8000`. Оперує виключно у внутрішній мережі Docker і не світить порт назовні.
3. **PostgreSQL:** персистентне сховище з виділеним іменованим томом (`pgdata`).
4. **Health Checks:** багаторівневий контроль працездатності:
   * База даних перевіряється через `pg_isready`.
   * Бекенд опитується утилітою `curl` кожні 10 секунд на ендпоінті `/health`.
   * Запуск контейнерів регулюється через `condition: service_healthy`.

---

## 🚀 Швидкий запуск

### 1. Локальна розробка (Docker Compose)
Підняти весь мультиконтейнерний стек:
```bash
docker compose up -d --build