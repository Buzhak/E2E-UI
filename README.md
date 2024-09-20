# E2E-UI Тестирование сайта

Тесты для проверки сценария покупки товара на сайте saucedemo.com

Я использовал python и библиотеку playwright + pytest.

Сделано два теста:
* test_saucedemo.py - быстрый тест сценария покупки товара
* test_saucedemo_separate.py - тест разделён на шаги для наглядности, но работает медленнее

## Запуск тестов

1. Копируем репозиторий
```
git clone git@github.com:Buzhak/E2E-UI.git
```

2. Переходим в папку
```
cd E2E-UI
```

3. Создаём виртуальное окружение
```
python3 -m venv env
```

4. Запускаем виртуальное окружение
win
```
env\Scripts\activate
```
linux\mac
```
source env/bin/activate
```

5. устанавливаем зависимости
```
pip install -r requirements.txt
```

6. Создаем файлик .env и заполняем его по примеру
```
login=standard_user
password=secret_sauce
```

7. Запускаем тесты:
### Запуск быстрого теста 

с открытием браузера:
```
pytest --headed ./test/test_saucedemo.py
```
без отрытия браузера
```
pytest ./test/test_saucedemo.py
```

### Запуск подробного nеста 

с открытием браузера:
```
pytest --headed ./test/test_saucedemo_separate.py
```
с просмотром промежуточных результатов:
```
pytest -v ./test/test_saucedemo_separate.py
```

## Технологии

* python
* playwright
* pytest
