import unittest
from unittest.mock import patch

from src.user_interface import print_menu


class TestUserInterface(unittest.TestCase):
    def test_print_menu(self):
        """Тест вывода меню"""
        try:
            print_menu()
        except Exception as e:
            self.fail(f"print_menu() вызвал ошибку: {e}")

    @patch("builtins.input", side_effect=["0"])
    @patch("src.user_interface.APIAdapter")
    def test_user_interaction_exit(self, mock_api, mock_input):
        """Тест выхода из программы"""
        from src.user_interface import user_interaction

        try:
            user_interaction()
        except Exception as e:
            self.fail(f"user_interaction() вызвал ошибку: {e}")

    # Пропускаем этот тест — он требует ручного ввода
    @unittest.skip("Требуется ручное тестирование")
    def test_user_interaction_get_aeroplanes(self):
        pass
