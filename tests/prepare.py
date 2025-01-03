import json
import pathlib


class Prepare:
    """
    Class for preparing equipment before testing. Defined as singleton
    """

    _instance = None
    test_db = "./tests/test_db.json"
    test_contacts = [{'name': 'Иван Иванов',
                           'phone': '+7 111 111-11-11',
                           'email': 'ivan.ivanov@example.com',
                           'address': 'Москва, ул. Ленина, д. 1'}]

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
            with open(class_.test_db, "w", encoding='utf8') as stream:
                json.dump(class_.test_contacts, stream, ensure_ascii=False, indent=4)
        return class_._instance

    def purge_database(self):
        if pathlib.Path(self.test_db).exists():
            pathlib.Path(self.test_db).unlink()