# TeamFinder
## База данных
Перед началом стоит поднять сервер PostgreSQL и создать базу данных. Вся информация о секретах хранится в файле **.env**. В нём необходимо внести измненения под свой сервер PostgreSQL и созданную БД. Пример `.env`:
```env
# Database
DB_DRIVER=postgresql+asyncpg
DB_HOST=localhost
DB_PORT=5432
DB_NAME=teamup
DB_USER=ваш_пользователь
DB_PASSWORD=ваш_пароль 
```

---

## Установка зависимостей
Проект использует современный пакетный менеджер [**uv**](https://pypi.org/project/uv/) — он устанавливает зависимости асинхронно и работает быстрее `pip`.

### 1. Установка `uv` (глобально):
```bash
pip install uv
# или, если используете pipx:
pipx install uv
```

### 2. Создание и активация виртуального окружения:
```bash
uv venv
# команда для Windows систем:
.venv\Scripts\activate
# команда для Unix систем:
source .venv/bin/activate
```

### 3. Установка зависимостей проекта:
```bash
uv pip install -e .
```

---

## Создание сущностей
Перед тем как запустить сервер надо создать в БД пустые таблицы (убедитесь, что выы подняли сервер PostgreSQL и создали новую базу данных с указанием секретов в .env):
```bash
python -m src.teamup.utils.db_create_all

```

---

## Запуск приложения
```bash
python -m src.teamup.main
```

После запуска сервер будет доступен по адресу: `http://localhost:8000`  
Swagger-документация: `http://localhost:8000/docs`

## Работа с приложением
Для работы с приложением откройти файл "registration.html" в папках public->pages->"registration.html". Страница будет по умолчанию открыта в вашем браузере. 
