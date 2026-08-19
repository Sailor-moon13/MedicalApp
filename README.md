# MedicalApp

Данный проект предоставляет пользователю простой веб-интерфейс, благодаря которому можно провести анализ рентгеновского снимка / МРТ.

## Структура проекта

```
MedicalApp/
│
├── app/
│   ├── main.py
│   ├── predictor.py
│   │
│   ├── routers/
│   │   └── predict.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       │
│       └── js/
│           └── script.js
│
├── models/
│   └── # Downloaded automatically
│
├── download_models.py
├── run.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Sailor-moon13/MedicalApp.git
   cd MedicalApp
2. Создайте и активируйте виртуальное окружение:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```
4. Запустите приложение:
   ```
   python run.py
   ```

5. Откройте интерфейс в браузере:
   ```
   http://127.0.0.1:8000
   ```


## Примечания

Результаты являются исследовательскими/образовательными и не являются медицинской диагностикой. Автор не несет никакой ответсвенности.


## Автор

Малютин Александр (https://github.com/Sailor-moon13).
