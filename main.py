from phonebook import Handbook
from phonebook import Menu


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
        menu_return_point = eval(f"menu.{menu_items[int(menu_user_choice)][1]}")


if __name__ == "__main__":
    main()