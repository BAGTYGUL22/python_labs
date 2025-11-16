import pytest
import sys
import os

# Добавляем корневую папку в путь Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем из корневой папки
from lib.text import normalize, tokenize, count_freq, top_n


@pytest.mark.parametrize(
    "source, expected",
    [
        ("Hello world", ["Hello", "world"]),
        ("", []),
        ("hello, world!", ["hello", "world"]),
        ("Привет мир", ["Привет", "мир"]),
        ("до-свидания мир", ["до-свидания", "мир"]),
    ],
)
def test_tokenize_basic(source, expected):
    assert tokenize(source) == expected


@pytest.mark.parametrize(
    "tokens, expected",
    [
        (["hello", "world", "hello"], {"hello": 2, "world": 1}),
        ([], {}),
        (["a", "b", "a", "c", "c", "c"], {"a": 2, "b": 1, "c": 3}),
    ],
)
def test_count_freq_and_top_n(tokens, expected):
    assert count_freq(tokens) == expected


@pytest.mark.parametrize(
    "freq, n, expected",
    [
        ({"hello": 2, "world": 1}, 1, [("hello", 2)]),
        ({"a": 2, "b": 2, "c": 1}, 3, [("a", 2), ("b", 2), ("c", 1)]),
        ({"x": 3, "y": 3, "z": 3}, 3, [("x", 3), ("y", 3), ("z", 3)]),
        ({}, 1, []),
    ],
)
def test_top_n_tie_breaker(freq, n, expected):
    assert top_n(freq, n) == expected
