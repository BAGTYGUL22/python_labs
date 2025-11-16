import pytest
from src.lab03.text import *

class TestText:

    @pytest.mark.parametrize("input_text, expected", [
        # Базовые случаи
        ("Hello world", "hello world"),
        (" PYTHON  Programming  ", "python programming"),
        ("Test123", "test123"),
        # Граничные случаи
        ("", ""),
        ("  ", ""),  # пробелы
        ("Hello!!??", "hello!!??"),  # спецсимволы сохраняются
        # Unicode
        ("Привет Мир", "привет мир"),
        ("café", "café"),
    ])
    def test_normalize(self, input_text, expected):
        assert normalize(input_text) == expected

    @pytest.mark.parametrize("input_text, expected", [
        ("Hello world", ["hello", "world"]),
        ("", []),
        ("hello, world!", ["hello,", "world!"]),
        ("Привет мир", ["привет", "мир"])
    ])
    def test_tokenize(self, input_text, expected):
        assert tokenize(input_text) == expected

    @pytest.mark.parametrize("tokens, expected", [
        (["hello", "world", "hello"], {"hello": 2, "world": 1}),
        ([], {}),
        (["a", "b", "a", "c", "c"], {"a": 2, "b": 1, "c": 2})
    ])
    def test_count_freq(self, tokens, expected):
        assert count_freq(tokens) == expected

    @pytest.mark.parametrize("freq, n, expected", [
        ({"hello": 2, "world": 1}, 1, [("hello", 2)]),
        ({"a": 2, "b": 2, "c": 1}, 2, [("a", 2), ("b", 2)]),  # одна частота, алфавитная сортировка
        ({"x": 3, "y": 3, "z": 3}, 3, [("x", 3), ("y", 3), ("z", 3)]),  # одинаковые частоты -- по алфавиту
        ({}, 1, [])
    ])
    def test_top_n(self, freq, n, expected):
        assert top_n(freq, n) == expected
