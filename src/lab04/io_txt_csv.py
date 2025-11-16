from pathlib import Path
import csv


def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    path = Path(path)
    with open(path, "r", encoding=encoding) as file:
        return file.read()


def write_csv(
    rows: list[tuple | list], path: str | Path, header: tuple[str, ...] | None = None
) -> None:
    path = Path(path)
    ensure_parent_dir(path)
    if rows:
        first_row_length = len(rows[0])
        for i, row in enumerate(rows):
            if len(row) != first_row_length:
                raise ValueError(
                    f"Строка {i} имеет длину {len(row)}, ожидается {first_row_length}"
                )

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if header is not None:
            writer.writerow(header)
        writer.writerows(rows)


def ensure_parent_dir(path: str | Path) -> None:
    path = Path(path)
    parent_dir = path.parent
    parent_dir.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":

    from io_txt_csv import read_text, write_csv

    write_csv([("word", "count"), ("test", 3)], "data/check.csv")
    try:
        txt = read_text("test_input.txt")
        print("Файл успешно прочитан")
    except FileNotFoundError:
        print("Файл test_input.txt не найден")
    except UnicodeDecodeError:
        print("Ошибка кодировки при чтении файла")
