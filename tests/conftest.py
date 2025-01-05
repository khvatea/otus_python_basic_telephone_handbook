import time

import pytest
import json
import pathlib
import shutil
from phonebook import Database


@pytest.fixture(scope="session")
def test_contacts():
    data = [{   'name': 'Иван Иванов',
                'phone': '+7 111 111-11-11',
                'email': 'ivan.ivanov@example.com',
                'address': 'Москва, ул. Ленина, д. 1'
            },
            {
                "name": "Павел Станкевич",
                "phone": "+7 200 111-11-00",
                "email": "pavel.stankevich@example.com",
                "address": "Горловка, ул. Надежды, д. 90"
            },
            {
                "name": "Нина Егоровна",
                "phone": "+7 201 111-11-01",
                "email": "nina.egorovna@example.com",
                "address": "Невельск, ул. Левобережная, д. 91"
            }]
    return data


@pytest.fixture(scope="session")
def test_new_contact():
    contact = { 'name':  'Петр Петров',
                'phone': '+7 222 222-22-22',
                'email': 'peter.petrov@example.com',
                'address': 'Владивосток, ул. К.Маркса, д. 11'}
    return contact

@pytest.fixture(scope="session")
def db(tmp_path_factory, test_contacts):
    """
    Создание тестовой БД. YIELD. Удаление тестовой БД

    Временная БД генерируется и доступна в границах одного тестового сеанса.
    Создается тестовая БД во временном каталоге, подготовкой которого занимаются фикстуры tmp_path (в пределах функции) и tmp_path_factory (в пределах сеанса).
    (https://docs.pytest.org/en/stable/how-to/tmp_path.html)
    """

    # Создание тестовой БД
    tmp_file_db = tmp_path_factory.mktemp("db") / "test_db.json"
    with open(tmp_file_db, "w", encoding='utf8') as stream:
        json.dump(test_contacts, stream, ensure_ascii=False, indent=4)

    database = Database(str(tmp_file_db))

    yield database

    # Удаляем временный каталог для тестов
    if pathlib.Path(str(tmp_path_factory.getbasetemp())).exists():
        shutil.rmtree(str(tmp_path_factory.getbasetemp()))

