from src.api_adapter import APIAdapter


def print_menu():
    """Вывод главного меню"""
    print("\n" + "=" * 50)
    print("ГЛАВНОЕ МЕНЮ")
    print("=" * 50)
    print("1. Получить самолёты по стране")
    print("2. Топ N по высоте")
    print("3. Топ N по скорости")
    print("4. Фильтр по стране регистрации")
    print("5. Фильтр по диапазону высот")
    print("6. Показать статистику")
    print("7. Сохранить данные")
    print("8. Загрузить данные")
    print("9. Переключить тестовый режим")
    print("0. Выход")
    print("-" * 50)


def user_interaction():
    """Функция для взаимодействия с пользователем"""
    api = APIAdapter(test_mode=False)

    print("\n" + "=" * 60)
    print("🛩ДОБРО ПОЖАЛОВАТЬ В СЕРВИС ОТСЛЕЖИВАНИЯ САМОЛЁТОВ")
    print("=" * 60)
    print(f"Режим работы: {'ТЕСТОВЫЙ' if api.test_mode else 'РЕАЛЬНЫЙ'}")

    while True:
        print_menu()
        choice = input("\nВаш выбор: ").strip()

        if choice == "0":
            print("\nДо свидания!")
            break

        elif choice == "1":
            country = input("Введите название страны (на английском): ").strip()
            if not country:
                print("Название страны не может быть пустым")
                continue

            try:
                api.get_aeroplanes(country)
                api.print_aeroplanes(title=f"Самолёты в {country}")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == "2":
            try:
                n = int(input("Введите количество самолётов для топа: "))
                if n <= 0:
                    print("Число должно быть положительным")
                    continue

                top = api.get_top_by_altitude(n)
                api.print_aeroplanes(top, title=f"Топ {n} самолётов по высоте")
            except ValueError:
                print("Ошибка: введите корректное число")

        elif choice == "3":
            try:
                n = int(input("Введите количество самолётов для топа: "))
                if n <= 0:
                    print("Число должно быть положительным")
                    continue

                top = api.get_top_by_speed(n)
                api.print_aeroplanes(top, title=f"Топ {n} самолётов по скорости")
            except ValueError:
                print("Ошибка: введите корректное число")

        elif choice == "4":
            country = input("Введите страну регистрации: ").strip()
            if not country:
                print("Название страны не может быть пустым")
                continue

            filtered = api.filter_by_country(country)
            api.print_aeroplanes(filtered, title=f"Самолёты из {country}")

        elif choice == "5":
            try:
                min_alt = float(input("Введите минимальную высоту (м): "))
                max_alt = float(input("Введите максимальную высоту (м): "))

                filtered = api.filter_by_altitude_range(min_alt, max_alt)
                api.print_aeroplanes(filtered, title=f"Самолёты на высоте {min_alt:.0f}-{max_alt:.0f} м")
            except ValueError:
                print("Ошибка: введите корректные числа")

        elif choice == "6":
            api.print_statistics()

        elif choice == "7":
            api.save_to_file()

        elif choice == "8":
            api.load_from_file()
            api.print_aeroplanes(title="Загруженные данные")

        elif choice == "9":
            api.test_mode = not api.test_mode
            print(f"Режим изменён на: {'ТЕСТОВЫЙ' if api.test_mode else 'РЕАЛЬНЫЙ'}")

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    user_interaction()
