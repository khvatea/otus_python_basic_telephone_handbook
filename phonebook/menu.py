from .handbook import Handbook
import sys


class Menu:

    def __init__(self, handbook: Handbook):
        self.handbook = handbook


    def show(self, point: int) -> dict:
        """
        Main menu of the handbook
        :param point: Menu item number
        :return:
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
        self.handbook.open()
        return 0


    def item_print_handbook(self):
        return 2


    def item_sorted_handbook(self, sorted_by_field: str):
        print(self.handbook.show_pretty_table(sorted_by_field, self.handbook.contacts))
        return 0


    def item_diff_handbook(self):
        contacts_diff = self.handbook.compare()

        if not contacts_diff:
            sys.stdout.writelines("\033[34mИзменений в справочнике нет.\033[0m\n")
        else:
            sys.stdout.writelines(contacts_diff)

        return 0


    def item_add_row(self):
        new_contact = {"name": "undefined", "phone": "undefined", "email": "undefined", "address": "undefined"}

        print("\nЗаполните поля нового контакта")
        for key, value in new_contact.items():
            new_contact[key] = input(f"{key}: ")
        self.handbook.add_row(new_contact)

        return 0


    def item_save_handbook(self):
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
        find_contacts = self.handbook.find_rows(input("\nКого найти?: "))
        print(self.handbook.show_pretty_table(contacts=find_contacts))

        return 0

    def item_update_row(self):
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
        self.item_save_handbook()
        self.handbook.close()
        exit(0)