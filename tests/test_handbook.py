import pytest

from phonebook import handbook, Handbook


def test_add_row(db, test_new_contact, test_contacts):
    hb = Handbook(db.file)
    hb.open()
    hb.add_row(test_new_contact)
    test_contacts.append(test_new_contact)

    assert hb.contacts == test_contacts


@pytest.mark.parametrize(
    "search_string",[
        'Иван Иванов',
        "Павел Станкевич",
        "Нина Егоровна"
    ]
)
def test_find_rows(db, search_string):
    hb = Handbook(db.file)
    hb.open()

    assert hb.find_rows(search_string)[0]["name"] == search_string


def test_update_row(db):
    hb = Handbook(db.file)
    hb.open()

    name = "Павел Станкевич"
    new_info = {
                "name": "Павел Станкевич",
                "phone": "+7 123 456-78-90",
                "email": "pavel.stankevich@example.com",
                "address": "NEW_ADDRESS"
            }

    hb.update_row(name, new_info)

    assert hb.find_rows(name)[0]["phone"] == "+7 123 456-78-90"
    assert hb.find_rows(name)[0]["address"] == "NEW_ADDRESS"


def test_delete_row(db):
    hb = Handbook(db.file)
    hb.open()

    name = "Павел Станкевич"
    hb.delete_row(name)
    assert hb.find_rows(name) == []
