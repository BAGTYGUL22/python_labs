#!/usr/bin/env python3
"""
Скрипт для анализа текста и генерации отчета в CSV.
"""

import sys
import argparse
from pathlib import Path

# Добавляем путь к lib в sys.path для импорта модулей
lib_path = Path(__file__).parent.parent.parent / 'lib'
sys.path.insert(0, str(lib_path))

# Импортируем модули из предыдущих лабораторных
from io_txt_csv import read_text, write_csv
from lib.text import normalize, tokenize, count_freq, top_n


def generate_report(input_path: str, output_path: str, encoding: str = "utf-8") -> None:
    """
    Генерирует отчет по текстовому файлу.
    
    Args:
        input_path: Путь к входному файлу
        output_path: Путь для сохранения CSV отчета
        encoding: Кодировка входного файла
    """
    # Чтение входного файла
    try:
        text = read_text(input_path, encoding)
    except FileNotFoundError:
        print(f"Ошибка: файл '{input_path}' не найден")
        sys.exit(1)
    except UnicodeDecodeError as e:
        print(f"Ошибка кодировки: {e}")
        print("Попробуйте указать другую кодировку с помощью --encoding")
        sys.exit(1)
    
    # Нормализация и токенизация с использованием функций из lib/text.py
    normalized_text = normalize(text, casefold=True, yo2e=True)
    tokens = tokenize(normalized_text)
    
    # Подсчет частот
    frequencies = count_freq(tokens)
    
    # Сортировка: по убыванию частоты, при равенстве - по возрастанию слова
    sorted_words = sorted(frequencies.items(), 
                         key=lambda x: (-x[1], x[0]))
    
    # Запись CSV
    header = ("word", "count")
    write_csv(sorted_words, output_path, header)
    
    # Вывод резюме в консоль
    total_words = len(tokens)
    unique_words = len(frequencies)
    
    print(f"Всего слов: {total_words}")
    print(f"Уникальных слов: {unique_words}")
    
    if unique_words > 0:
        top_5_words = top_n(frequencies, 5)  # Используем функцию из lib/text.py
        print("Топ-5:")
        for i, (word, count) in enumerate(top_5_words, 1):
            print(f"  {i}. '{word}' - {count}")
    else:
        print("Топ-5: нет данных")
    
    print(f"Отчет сохранен в: {output_path}")


def main():
    """Основная функция скрипта."""
    parser = argparse.ArgumentParser(
        description="Генератор отчета по частотности слов в тексте"
    )
    parser.add_argument(
        "--in", 
        dest="input_file",
        default="test_input.txt",
        help="Входной текстовый файл (по умолчанию: test_input.txt)"
    )
    parser.add_argument(
        "--out",
        dest="output_file", 
        default="data/report.csv",
        help="Выходной CSV файл (по умолчанию: data/report.csv)"
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="Кодировка входного файла (по умолчанию: utf-8)"
    )
    
    args = parser.parse_args()
    
    generate_report(args.input_file, args.output_file, args.encoding)


if __name__ == "__main__":
    main()