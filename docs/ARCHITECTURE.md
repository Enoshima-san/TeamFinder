# Примерный вариант backend архитектуры 
Сгенерирован с учётом многочисленных правок и замечаний. На данной стадии лишь примерный, так как точный стек не установлен, возможны изменения (исключение чего-либо).
---
```
TeamFinder/
├── .env                          # Локальные переменные окружения (НЕ коммитить!)
├── .env.example                  # Шаблон для разработчиков (по итогу просто используем его, прятать на нечего)
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
├── README.md
├── main.py                       # Точка входа FastAPI приложения
│
├── alembic/                      # Миграции базы данных
│   ├── versions/
│   ├── env.py
│   └── alembic.ini
│
└── src/
    └── TeamFinder/
        ├── __init__.py
        │
        ├── api/                  # Presentation Layer (Internal Adapters HTTP/GraphQL)
        │   ├── routes/
        │   ├── schemas/          # Pydantic модели для API
        │   ├── dependencies.py   # FastAPI Depends (auth, pagination, session)
        │   ├── middleware.py     # CORS, logging, rate limiting
        │   └── websocket/        # WebSocket handlers для чата/уведомлений
        │
        ├── application/          # Application Layer (Use Cases/Services)
        │   ├── __init__.py
        │   ├── services/         # Оркестраторы (не прямая работа с БД и API, в общем - наша бизнес-логики)
        │   ├── use_cases/        # Конкретные сценарии (опционально)
        │   └── interfaces/       # Абстракции репозиториев (Protocol)
        │
        ├── core/                 #  Core (Config, Constants, Base Classes)
        │   ├── settings.py       # Pydantic Settings (все конфиги в Singleton-классе)
        │   ├── config/           # Разделённые конфиги 
        │   ├── security.py       # JWT, password hashing (JWT под вопросом, хэширование делаем)
        │   └── logging.py        # Конфигурация логгера
        │
        ├── domain/               # Domain Layer (Business Logic)
        │   ├── entities/         # Чистые бизнес-объекты
        │   └── repositories/     # Абстрактные интерфейсы 
        │
        └── infrastructure/       # Infrastructure Layer (External Adapters) <- реализуют технические детали для Application/Domain слоев
            ├── database/
            │   ├── mappers/      # Классы для переводов domain-сущностей в ORM-модели
            │   ├── session.py    # SQLAlchemy session factory (база)
            │   ├── base.py       # DeclarativeBase (база)
            │   ├── models/       # ORM модели
            │   └── migrations/   # Alembic migrations (можно в соответстующей папке в корне разместить)
            │
            ├── repositories/     # Реализации репозиториев
            │
            ├── cache/            # Redis клиент и кэш-сервисы
            │   ├── client.py     # Redis connection
            │   └── services.py   # Кэш-логика (сессии, rate limit)
            │
            ├── auth/             # Аутентификация
            │   ├── jwt.py        # JWT token generation/validation (мб Редиса хватит хз)
            │   └── oauth/        # OAuth провайдеры (Steam, Discord, VK)
            │
            │
            └── external/         # Сторонние API (Discord, Steam, VK)
```
---
Последнее обновление: 2026-03-04
Ответственный за сопровождение: [mkken1]
