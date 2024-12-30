from phonebook import Handbook
from phonebook import Menu
import sys


def main():
    handbook = Handbook("sources/handbook.json")
    menu = Menu(handbook)
    menu_return_point = 0

    while True:
        print("\n\n##############################")
        menu_items = menu.show(menu_return_point)

        # Show (sub)menu
        for key, value in menu_items.items():
            print(f"{key}. {value[0]}")

        # Select action and evaluate
        menu_user_choice = input("Введите номер действия: ")
        try:
            menu_return_point = eval(f"menu.{menu_items[int(menu_user_choice)][1]}")
        except KeyError:
            sys.stdout.writelines("\033[31mУказан неверный пункт меню.\033[0m\n")
        except ValueError:
            sys.stdout.writelines("\033[31mНа ввод должно поступить целочисленное значение.\033[0m\n")


if __name__ == "__main__":
    main()