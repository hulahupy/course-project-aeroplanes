# Курсовая работа: Система мониторинга воздушного пространства

## Описание проекта
Программа для получения информации о самолетах через API OpenSky Network с возможностью фильтрации, сортировки и сохранения данных.

## Функциональность
- Получение данных о самолетах по названию страны
- Сортировка по высоте и скорости
- Фильтрация по стране регистрации и диапазону высот
- Сохранение данных в JSON-файл
- Загрузка и удаление сохраненных данных

## Установка и запуск

### Требования
- Python 3.14+
- UV

### Установка
```
uv venv --python 3.14
.venv\Scripts\activate
uv add requests
uv add --dev pytest ruff black
Запуск программы

python main.py
Запуск тестов

pytest -v
Структура проекта

course-project-aeroplanes/
├── src/
│   ├── api_adapter.py       # Абстрактный класс для API
│   ├── aeroplanes_api.py    # Работа с OpenStreetMap и OpenSky
│   ├── aeroplane.py         # Класс самолёта
│   ├── file_storage.py      # Работа с JSON-файлами
│   └── user_interface.py    # Пользовательский интерфейс
├── tests/
│   ├── test_aeroplane.py
│   └── test_file_storage.py
├── data/                    # Директория для JSON-файлов
├── main.py
├── pyproject.toml
└── README.md
```
## Автор
Владимир