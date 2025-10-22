from pathlib import Path
import csv


def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    """
    Открыть файл на чтение в указанной кодировке и вернуть содержимое как одну строку.
    
    Args:
        path: Путь к файлу для чтения (строка или Path объект)
        encoding: Кодировка файла. По умолчанию "utf-8".
                  Пользователь может выбрать другую кодировку, например:
                  - encoding="cp1251" для Windows-1251
                  - encoding="koi8-r" для KOI8-R
                  - encoding="iso-8859-1" для Latin-1
                  - encoding="cp866" для DOS/IBM866
    
    Returns:
        str: Содержимое файла как одна строка
        
    Raises:
        FileNotFoundError: Если файл не найден
        UnicodeDecodeError: Если указанная кодировка не подходит для чтения файла
    """
    path = Path(path)
    
    with open(path, 'r', encoding=encoding) as file:
        return file.read()


def write_csv(rows: list[tuple | list], path: str | Path, header: tuple[str, ...] | None = None) -> None:
    """
    Создать/перезаписать CSV файл с разделителем ','.
    
    Args:
        rows: Список строк данных (каждая строка - tuple или list)
        path: Путь для сохранения CSV файла
        header: Опциональный заголовок для первой строки CSV
        
    Raises:
        ValueError: Если строки в rows имеют разную длину
    """
    path = Path(path)
    
    # Создаем родительские директории если их нет
    ensure_parent_dir(path)
    
    # Проверяем одинаковую длину всех строк
    if rows:
        first_row_length = len(rows[0])
        for i, row in enumerate(rows):
            if len(row) != first_row_length:
                raise ValueError(f"Строка {i} имеет длину {len(row)}, ожидается {first_row_length}")
    
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        if header is not None:
            writer.writerow(header)
        
        writer.writerows(rows)


def ensure_parent_dir(path: str | Path) -> None:
    """
    Создать родительские директории, если их нет.
    
    Args:
        path: Путь к файлу или директории
    """
    path = Path(path)
    parent_dir = path.parent
    parent_dir.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    # Мини-тесты
    from io_txt_csv import read_text, write_csv
    
    # Тест записи CSV
    write_csv([("word", "count"), ("test", 3)], "data/check.csv")
    
    # Тест чтения текста (если файл существует)
    try:
        txt = read_text("test_input.txt")  # должен вернуть строку
        print("Файл успешно прочитан")
    except FileNotFoundError:
        print("Файл test_input.txt не найден")
    except UnicodeDecodeError:
        print("Ошибка кодировки при чтении файла")