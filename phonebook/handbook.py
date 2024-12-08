from .database import Database
from prettytable import PrettyTable


class Handbook(Database):

    @staticmethod
    def show_pretty_table(sort_by_field="name", contacts=[]) -> str:
        """
        Get all handbook entries sorted by the selected field (by default, sorting will be done by the 'name' field)
        The list should be presented as follows:
        [
            {
                "name": "Ivan Ivanov",
                "phone": "+7 111 111-11-11",
                "email": "ivan.ivanov@example.com",
                "address": "Moscow, st. Lenina, 1"
            }
        ]
        :param sort_by_field: Table sort field
        :param contacts: Contact list
        :return: Return string representation of table in current state
        """
        pretty_table = PrettyTable()

        # set table field names
        pretty_table.field_names = ["name", "phone", "email", "address"]
        pretty_table.align["name"] = "l"
        pretty_table.align["address"] = "l"

        # place all lines from the dictionary into a table
        for contact in contacts:
            pretty_table.add_row(list(contact.values()))

        return pretty_table.get_string(sortby=sort_by_field)


    def add_row(self, new_contact: dict):
        """
        Add an entry to the handbook
        :param new_contact: New contact in dict format
        :return:
        """
        expected_field_names = {"name", "phone", "email", "address"}

        if isinstance(new_contact, dict):
            missing_keys = expected_field_names - new_contact.keys()
            extra_keys = new_contact.keys() - expected_field_names

            if missing_keys:
                print(f"Ошибка при записи контакта. Отсутствуют ключи: {missing_keys}")
            elif extra_keys:
                print(f"Ошибка при записи контакта. Лишние ключи: {extra_keys}")
            else:
                self.contacts.append(new_contact)
        else:
            print(f"""
            В функции передан: {type(new_contact)}
            Требуется dict
            """)


    def find_rows(self, search_string: str, find_by_field="name") -> list:
        """
        Searching for contacts in the handbook
        :param search_string: Search string
        :param find_by_field: Field to search for
        :return: Search result
        """
        result = [contact for contact in self.contacts if search_string in contact[find_by_field]]
        return result


    def update_row(self, name: str, update_contact: dict) -> dict:
        """
        Update a handbook entry
        :param name: Name of the record that is being updated
        :param update_contact: Data according to handbook fields in dict format
        :return: Updated contact
        """
        for contact in self.contacts:
            if contact["name"] == name:
                contact.update(update_contact)
                return contact


    def delete_row(self, name: str):
        """
        Removing an entry from the handbook
        :param name: Name of the entry to be deleted
        :return: Remove contact in dict format
        """
        for contact in self.contacts:
            if contact["name"] == name:
                self.contacts.remove(contact)
                return contact
        return None