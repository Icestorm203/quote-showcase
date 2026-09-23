# Quote Showcase

Витрина цитатника, реализованная на FastAPI.

Сервис принимает снимки каталога цитат, хранит данные в памяти процесса, предоставляет API для чтения, редактирования и удаления цитат, а также обращается к внешнему каталогу при отсутствии данных в локальном кеше.

Проект выполнен в рамках тестового задания на позицию Python Backend Developer.

---

## Основные возможности

### Для читателей

- Получение цитаты по идентификатору
- Получение данных из локального кеша
- Получение данных из внешнего каталога при отсутствии цитаты локально
- Заголовок `X-Source` для определения источника ответа

Значения заголовка:

```text
LOCAL
```

Цитата была получена из локального кеша.

```text
CATALOG
```

Для получения цитаты выполнялся запрос во внешний каталог.

---

### Для редакции

- Импорт полного снимка каталога
- Добавление новой цитаты
- Обновление существующей цитаты
- Удаление цитаты

---

### Для эксплуатации

- Health-check эндпоинт
- Сбор статистики работы сервиса
- Подсчёт локальных выдач
- Подсчёт обращений к каталогу
- Учёт размера локального кеша
- Подсчёт вытеснений из кеша

---

## Используемые технологии

- Python 3.12
- FastAPI
- Uvicorn
- HTTPX
- Pydantic
- Docker

---

## Структура проекта

```text
app/
├── api/
│   ├── catalog.py
│   ├── health.py
│   ├── quotes.py
│   └── stats.py
│
├── core/
│   ├── lru.py
│   ├── memory.py
│   ├── state.py
│   └── stats.py
│
├── models/
│   └── requests.py
│
├── services/
│   └── catalog_client.py
│
└── main.py

requirements.txt
Dockerfile
README.md
.gitignore
```

---

## API

### Проверка состояния сервиса

```http
GET /health
```

Ответ:

```json
{
  "status": "healthy"
}
```

---

### Установка адреса каталога

```http
POST /catalog/source
```

Тело запроса:

```json
{
  "url": "http://catalog.internal:9000"
}
```

Ответ:

```json
{
  "source": "http://catalog.internal:9000"
}
```

---

### Импорт снимка каталога

```http
POST /import
```

Тело запроса:

```json
{
  "quotes": [
    {
      "id": "q-1",
      "author": "Marcus Aurelius",
      "text": "The happiness of your life depends upon the quality of your thoughts."
    }
  ]
}
```

Ответ:

```json
{
  "imported": 1,
  "dropped": 0
}
```

---

### Добавление или изменение цитаты

```http
PUT /catalog/{quote_id}
```

Тело запроса:

```json
{
  "author": "Marcus Aurelius",
  "text": "The happiness of your life depends upon the quality of your thoughts."
}
```

Ответ:

```json
{
  "id": "q-1",
  "author": "Marcus Aurelius",
  "text": "The happiness of your life depends upon the quality of your thoughts."
}
```

---

### Удаление цитаты

```http
DELETE /catalog/{quote_id}
```

Ответ:

```json
{
  "deleted": true
}
```

---

### Получение цитаты

```http
GET /quotes/{quote_id}
```

Ответ:

```json
{
  "id": "q-1",
  "author": "Marcus Aurelius",
  "text": "The happiness of your life depends upon the quality of your thoughts."
}
```

Заголовок ответа:

```http
X-Source: LOCAL
```

или

```http
X-Source: CATALOG
```

---

### Получение статистики

```http
GET /stats
```

Пример ответа:

```json
{
  "served_local": 12,
  "served_from_catalog": 3,
  "catalog_reads": 5,
  "evictions": 0,
  "local": 15,
  "bytes": 2478,
  "catalog": 15
}
```

Описание полей:

| Поле | Значение |
|--------|--------|
| served_local | Количество ответов из локального кеша |
| served_from_catalog | Количество ответов через каталог |
| catalog_reads | Количество запросов к каталогу |
| evictions | Количество вытеснений из кеша |
| local | Количество локально хранимых записей |
| bytes | Размер локального кеша в байтах |
| catalog | Количество известных цитат |

---

## Особенности реализации

### Локальный кеш

Для хранения цитат используется кеш в памяти процесса.

При отсутствии записи в локальном кеше выполняется обращение к внешнему каталогу.

### LRU-механизм

Для ограничения размера кеша используется политика вытеснения Least Recently Used (LRU).

Наименее используемые записи удаляются автоматически.

### Повторные запросы к каталогу

При ответе каталога:

```http
503 Service Unavailable
```

выполняются повторные попытки с учётом заголовка:

```http
Retry-After
```

### Обработка ошибок сети

Поддерживается обработка:

- Timeout
- ConnectError
- временной недоступности каталога

### Защита от одновременных запросов

Для одного идентификатора цитаты используется блокировка через `asyncio.Lock`, что позволяет избежать дублирующих запросов в каталог при одновременных обращениях.

---

## Локальный запуск

Создание виртуального окружения:

```bash
python -m venv .venv
```

Активация (Windows PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

Установка зависимостей:

```bash
pip install -r requirements.txt
```

Запуск приложения:

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## Запуск через Docker

Сборка образа:

```bash
docker build -t quote-showcase .
```

Запуск контейнера:

```bash
docker run -p 8000:8000 quote-showcase
```

Проверка:

```text
http://127.0.0.1:8000/docs
```

---

## Автор

Мустафа Муратов

Тестовое задание на позицию Python Backend Developer.
``