from .handbook import Handbook
from prettytable import PrettyTable
import sys


class Menu:

    def __init__(self, handbook: Handbook):
        """
        Console menu for displaying and interacting with the telephone directory
        :param handbook: list of handbook entries
        """
        self.handbook = handbook


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
        :return: Return string representation of pretty table in current state
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


    def show(self, point: int) -> dict:
        """
        Main menu of the handbook
        :param point: Menu item number
        :return:    Menu points in dictionary format with the value of a tuple of two elements.
                    The first element is the name of the menu item, the second is the name of the called function.
        """
        start_points = {1: ("Открыть справочник",    "item_open_handbook()"),
                        2: ("Выйти",                 "item_close_handbook()")}

        full_points = {1: ("Показать все контакты",  "item_print_handbook()"),
                       2: ("Показать изменения",     "item_diff_handbook()"),
                       3: ("Создать контакт",        "item_add_row()"),
                       4: ("Найти контакт",          "item_find_rows()"),
                       5: ("Обновить контакт",       "item_update_row()"),
                       6: ("Удалить контакт",        "item_delete_row()"),
                       7: ("Сохранить справочник",   "item_save_handbook()"),
                       8: ("Выйти",                  "item_close_handbook()")}

        filter_by_field_points = {1: ("Сортировать по имени",     "item_sorted_handbook('name')"),
                                  2: ("Сортировать по адресу",    "item_sorted_handbook('address')"),
                                  3: ("Сортировать по телефон",   "item_sorted_handbook('phone')")}

        if point == 2:
            return filter_by_field_points
        else:
            if not self.handbook.contacts:
                return start_points
            else:
                return full_points


    def item_open_handbook(self):
        """
        Menu item selected: "Открыть справочник"
        :return: Menu section number to go to
        """
        self.handbook.open()
        return 0


    def item_print_handbook(self):
        """
        Menu item selected: "Показать все контакты"
        :return: Menu section number to go to
        """
        return 2


    def item_sorted_handbook(self, sorted_by_field: str):
        """
        Menu item selected: "Сортировать по имени (адресу, телефону)"
        :return: Menu section number to go to
        """
        print(self.show_pretty_table(sorted_by_field, self.handbook.contacts))
        return 0


    def item_diff_handbook(self):
        """
        Menu item selected: "Показать изменения"
        :return: Menu section number to go to
        """
        contacts_diff = self.handbook.compare()

        if not contacts_diff:
            sys.stdout.writelines("\033[34mИзменений в справочнике нет.\033[0m\n")
        else:
            sys.stdout.writelines(contacts_diff)

        return 0


    def item_add_row(self):
        """
        Menu item selected: "Создать контакт"
        :return: Menu section number to go to
        """
        new_contact = {"name": "undefined", "phone": "undefined", "email": "undefined", "address": "undefined"}

        print("\nЗаполните поля нового контакта")
        for key, value in new_contact.items():
            new_contact[key] = input(f"{key}: ")
        self.handbook.add_row(new_contact)

        return 0


    def item_save_handbook(self):
        """
        Menu item selected: "Сохранить справочник"
        :return: Menu section number to go to
        """
        contacts_diff = self.handbook.compare()

        if not contacts_diff:
            sys.stdout.writelines("\033[34mИзменений в справочнике нет.\033[0m\n")
        else:
            print("\nОбнаружены следующие изменения:")
            sys.stdout.writelines(contacts_diff)
            if input("Сохранить изменения? (y/N)") == "y":
                self.handbook.save()

        return 0


    def item_find_rows(self):
        """
        Menu item selected: "Найти контакт"
        :return: Menu section number to go to
        """
        find_contacts = self.handbook.find_rows(input("\nКого найти?: "))
        print(self.show_pretty_table(contacts=find_contacts))

        return 0

    def item_update_row(self):
        """
        Menu item selected: "Обновить контакт"
        :return: Menu section number to go to
        """
        contact = input("\nВведите полное имя контакта: ")
        find_contacts = self.handbook.find_rows(contact)

        if find_contacts:
            update_contact = find_contacts[0]
            print(f"\nОбновите поля контакта {update_contact['name']}")
            for key, value in update_contact.items():
                item = input(f"{key} (сейчас ==> {value}): ")
                if item != "":
                    update_contact[key] = item
            print(self.handbook.update_row(contact, update_contact))
        else:
            sys.stdout.writelines("\033[34mЗапрошенный контакт не найден.\033[0m\n")

        return 0


    def item_delete_row(self):
        """
        Menu item selected: "Удалить контакт"
        :return: Menu section number to go to
        """
        contact = input("\nВведите полное имя контакта для удаления: ")

        register = self.handbook.delete_row(contact)
        if register:
            print(f"Запись {register} успешно удалена.")
        else:
            print("""
                        Контакт не удален, т.к. не был найден.
                        Убедитесь в правильности и полноте указанного имени.
                        Воспользуйтесь поиском по контактам.
                        """)
        return 0


    def item_close_handbook(self):
        """
        Menu item selected: "Выйти"
        :return: Menu section number to go to
        """
        if self.handbook.contacts:
            self.item_save_handbook()
        self.handbook.close()
        print("Выход...")
        exit(0)
