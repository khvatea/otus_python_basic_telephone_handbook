import json
from phonebook import Database
import pathlib
from prepare import Prepare


class TestDatabase:
    db = Database(Prepare().test_db)

    def test_open_database(self):
        self.db.open()
        assert pathlib.Path(self.db.file_buff).exists() == True
        assert Prepare().test_contacts == self.db.contacts

    def test_save_database(self):
        self.db.save()
        self.db.open()

        assert self.db.contacts == Prepare().test_contacts

    def test_close_database(self):
        self.db.close()
        assert pathlib.Path(self.db.file_buff).exists() == False
