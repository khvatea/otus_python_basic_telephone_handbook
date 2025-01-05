import pathlib


def test_open_database(db, test_contacts):
    db.open()
    assert pathlib.Path(db.file_buff).exists() == True
    assert test_contacts == db.contacts

def test_save_database(db, test_contacts):
    db.save()
    db.open()

    assert db.contacts == test_contacts

def test_close_database(db):
    db.close()
    assert pathlib.Path(db.file_buff).exists() == False
