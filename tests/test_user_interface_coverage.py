import unittest
from unittest.mock import patch

from src.user_interface import print_menu


class TestUserInterfaceCoverage(unittest.TestCase):
    def test_print_menu_output(self):
        """Тест вывода меню (проверяем, что функция не падает)"""
        try:
            print_menu()
        except Exception as e:
            self.fail(f"print_menu() вызвал ошибку: {e}")

    @patch("src.user_interface.APIAdapter")
    @patch("builtins.input", side_effect=["1", "Germany", "0"])
    def test_user_interaction_germany(self, mock_input, mock_api):
        """Тест получения самолётов для Германии"""
        from src.user_interface import user_interaction

        try:
            user_interaction()
        except Exception as e:
            self.fail(f"user_interaction() вызвал ошибку: {e}")

    @patch("src.user_interface.APIAdapter")
    @patch("builtins.input", side_effect=["2", "5", "0"])
    def test_user_interaction_top_altitude(self, mock_input, mock_api):
        """Тест топа по высоте"""
        from src.user_interface import user_interaction

        try:
            user_interaction()
        except Exception as e:
            self.fail(f"user_interaction() вызвал ошибку: {e}")

    @patch("src.user_interface.APIAdapter")
    @patch("builtins.input", side_effect=["3", "3", "0"])
    def test_user_interaction_top_speed(self, mock_input, mock_api):
        """Тест топа по скорости"""
        from src.user_interface import user_interaction

        try:
            user_interaction()
        except Exception as e:
            self.fail(f"user_interaction() вызвал ошибку: {e}")

    @patch("src.user_interface.APIAdapter")
    @patch("builtins.input", side_effect=["4", "USA", "0"])
    def test_user_interaction_filter_country(self, mock_input, mock_api):
        """Тест фильтрации по стране"""
        from src.user_interface import user_interaction

        try:
            user_interaction()
        except Exception as e:
            self.fail(f"user_interaction() вызвал ошибку: {e}")

    @patch("src.user_interface.APIAdapter")
    @patch("builtins.input", side_effect=["6", "0"])
    def test_user_interaction_statistics(self, mock_input, mock_api):
        """Тест вывода статистики"""
        from src.user_interface import user_interaction

        try:
            user_interaction()
        except Exception as e:
            self.fail(f"user_interaction() вызвал ошибку: {e}")

    @patch("src.user_interface.APIAdapter")
    @patch("builtins.input", side_effect=["7", "0"])
    def test_user_interaction_save(self, mock_input, mock_api):
        """Тест сохранения данных"""
        from src.user_interface import user_interaction

        try:
            user_interaction()
        except Exception as e:
            self.fail(f"user_interaction() вызвал ошибку: {e}")
