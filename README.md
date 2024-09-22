# petstore_test


1. установка репозитория
git clone https://github.com/AlexeyLenskiy/petstore_test.git

2. создание venv
из корня репозитория выполнить:
python3 -m venv venv

3. активация venv
Linux: source venv/bin/activate
Windows: .\venv\Scripts\activate

4. установка зависимостей из requrements.txt
pip install -r requrments.txt

5. Запуск тестов
Все тесты:
pytest 
Отдельный сьют:
pytests <путь до директории сьюта> (напр: pytest tests/test_pet.py)
Отдельный тест:
pytests <путь до директории сьюта> -k <имя теста> (напр: pytest tests/test_pet.py -k test_create_pet_valid_data)

Для для более читабельного результата можно добавить -sv в команду запуска тестов (напр: pytest tests/test_pet.py -sv)