<h1>Программирование и алгоритмизация</h1>
<h2>Лабораторная работа №5</h2>

**Задание 1**
```
import json
import csv
from pathlib import Path

def json_to_csv(json_path: str, csv_path: str) -> None:
    """
    Преобразует JSON-файл в CSV.
    Поддерживает список словарей [{...}, {...}], заполняет отсутствующие поля пустыми строками.
    Кодировка UTF-8.
    Порядок колонок — как в первом объекте, дополнительные — в алфавитном порядке.
    """
    json_file = Path(json_path)
    csv_file = Path(csv_path)

    if not json_file.is_file():
        raise FileNotFoundError(f"JSON файл не найден: {json_path}")

    with json_file.open("r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка чтения JSON: {e}")

    if not data or not isinstance(data, list):
        raise ValueError("Пустой JSON или неподдерживаемая структура: ожидается список словарей.")
    if not all(isinstance(item, dict) for item in data):
        raise ValueError("Все элементы JSON должны быть словарями.")

    first_keys = list(data[0].keys())
    all_keys = set(first_keys)
    for item in data[1:]:
        all_keys.update(item.keys())
    additional_keys = sorted(all_keys - set(first_keys))
    fieldnames = first_keys + additional_keys

    with csv_file.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            row = {key: item.get(key, "") for key in fieldnames}
            writer.writerow(row)
json_to_csv(f"src/lab05/samples/example1.json", f"src/lab05/out/example1_json.csv")

def csv_to_json(csv_path: str, json_path: str) -> None:
    """
    Преобразует CSV в JSON (список словарей).
    Заголовок обязателен, значения сохраняются как строки.
    json.dump(..., ensure_ascii=False, indent=2)
    """
    csv_file = Path(csv_path)
    json_file = Path(json_path)

    if not csv_file.is_file():
        raise FileNotFoundError(f"CSV файл не найден: {csv_path}")

    with csv_file.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("CSV файл не содержит заголовка.")
        data = list(reader)

    if not data:
        raise ValueError("CSV файл пуст.")

    with json_file.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

csv_to_json(f"src/lab05/samples/example2.csv", f"src/lab05/out/example2_csv.json")

```
![alt text](images/lab05/img5.1.png)  

![alt text](images/lab05/img.5.1.2.png)

![alt text](images/lab05/img.5.2.png)

![alt text](images/lab05/img.5.2.2.png)



**Задание 2**

```
from openpyxl import Workbook
import csv
from pathlib import Path

def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:
    """
    Конвертирует CSV в XLSX.
    Использует openpyxl.
    Первая строка CSV — заголовок.
    Лист называется "Sheet1".
    Колонки — автоширина по длине текста (не менее 8 символов).
    """
    csv_file = Path(csv_path)
    xlsx_file = Path(xlsx_path)

    if not csv_file.is_file():
        raise FileNotFoundError(f"CSV файл не найден: {csv_path}")

    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"

    with csv_file.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        raise ValueError("CSV файл пустой")

    for row in rows:
        ws.append(row)

    for col_idx, col_cells in enumerate(ws.columns, start=1):
        max_length = max(len(str(cell.value)) if cell.value is not None else 0 for cell in col_cells)
        adjusted_width = max(max_length, 8)
        col_letter = ws.cell(row=1, column=col_idx).column_letter
        ws.column_dimensions[col_letter].width = adjusted_width

    wb.save(xlsx_file)
csv_to_xlsx('src/lab05/samples/example2.csv', 'src/lab05/out/example3_csv.xlsx')

```
![alt text](images/lab05/img.5.2.png)

![alt text](images/lab05/img.5.3.png)




<h2>Лабораторная работа №4</h2>


**Задание №1**

```
from pathlib import Path
import csv

def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    path = Path(path)
    with open(path, 'r', encoding=encoding) as file:
        return file.read()

def write_csv(rows: list[tuple | list], path: str | Path, header: tuple[str, ...] | None = None) -> None:
    path = Path(path)
    ensure_parent_dir(path)
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
```
![alt text](images/lab04/img.4.1.png)
![alt text](images/lab04/img.4.1csv.png)

**Задание №2**
```
import sys
import argparse
from pathlib import Path

from io_txt_csv import read_text, write_csv
from lib.text import normalize, tokenize, count_freq, top_n

def generate_report(input_path: str, output_path: str, encoding: str = "utf-8") -> None:
    try:
        text = read_text(input_path, encoding)
    except FileNotFoundError:
        print(f"Ошибка: файл '{input_path}' не найден")
        sys.exit(1)
    except UnicodeDecodeError as e:
        print(f"Ошибка кодировки: {e}")
        print("Попробуйте указать другую кодировку с помощью --encoding")
        sys.exit(1)
    
    normalized_text = normalize(text, casefold=True, yo2e=True)
    tokens = tokenize(normalized_text)
    frequencies = count_freq(tokens)
    
    sorted_words = sorted(frequencies.items(), key=lambda x: (-x[1], x[0]))
    
    header = ("word", "count")
    write_csv(sorted_words, output_path, header)
    total_words = len(tokens)
    unique_words = len(frequencies)
    print(f"Всего слов: {total_words}")
    print(f"Уникальных слов: {unique_words}")
    
    if unique_words > 0:
        top_5_words = top_n(frequencies, 5)  
        print("Топ-5:")
        for i, (word, count) in enumerate(top_5_words, 1):
            print(f"  {i}. '{word}' - {count}")
    else:
        print("Топ-5: нет данных")
    
    print(f"Отчет сохранен в: {output_path}")

def main():
    
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
```
![alt text](images/lab04/img.4.2.png)
![alt text](images/lab04/img.4.2.csv.png)


<h2>Лабораторная работа №3</h2>

**Задание №1**

```
import re

def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    if casefold:
        text = text.casefold()
    if yo2e:
        text = text.replace('ё', 'е').replace('Ё', 'Е')
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def tokenize(text: str) -> list[str]:
    return re.findall(r'\w+(?:-\w+)*', text)

def count_freq(tokens: list[str]) -> dict[str, int]:
    freq = {}
    for token in tokens:
        freq[token] = freq.get(token, 0) + 1 
    return freq


def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    sorted_freq = sorted(freq.items(), key=lambda item: (-item[1], item[0]))
    return sorted_freq[:n]
print(normalize("ПрИвЕт\nМир\t"))
print(normalize("ёжик, Ёлка"))
print(normalize("  двойные   пробелы  "))
print(tokenize("привет мир"))
print(tokenize("hello,world!!!"))
print(tokenize("2025 год"))
print(tokenize("emoji 😀 не слово"))
print(count_freq(["a","b","a","c","b","a"]))
print(top_n(count_freq(["a","b","a","c","b","a"])))
print(top_n(count_freq(["bb","aa","bb","aa","cc"]), n=2))
```
![alt text](images/lab03/img.3.1.png)
**Задание №2**

```
import sys
from text import *

def text_in():
    text = sys.stdin.readline().strip()
    words = sorted(tokenize(normalize(text)), key=len, reverse=True)
    print(words)
    print(f"Всего слов: {len(tokenize(normalize(text)))}")
    print(f"Уникальных слов: {len(set(tokenize(normalize(text))))}")
    print("Топ-5:")
    print_word_frequency_table(text)
def print_word_frequency_table(text):
    freqs = count_freq(tokenize(normalize(text)))
    print('слово'.ljust(12), '|', 'частота')
    print('-' * 22)
    for word, count in sorted(freqs.items(), key=lambda x: x[1], reverse=True):
         print(word.ljust(12), '|', count)


text_in()
```
![alt text](images/lab03/img.3.2.png)


<h2>Лабораторная работа №2</h2>

**Задание №1**

```
#n=int(input('dlina:'))
#nums=[]
#i=0
#while i<n:
   # nums.append(input())
   # i+=1
def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    if not nums:
        raise ValueError("Список пуст")
    return(min(nums), max(nums))


def unique_sorted(nums: list[float | int]) -> list[float | int]:
    return sorted(set(nums))


def flatten(mat: list[list | tuple]) -> list:
    result = []
    for row in mat:
        if not isinstance(row, (list, tuple)):
            raise TypeError("Элемент не является списком или кортежем")
        result.extend(row)
    return result
#print(min_max(nums))
print(min_max([3, -1, 5, 5, 0]))
print(min_max([42]))
print(min_max([-5, -2, -9]))
print(min_max([1.5, 2, 2.0, -3.1]))
#print(unique_sorted(nums))
print(unique_sorted([3, 1, 2, 1, 3]))
print(unique_sorted([]))
print(unique_sorted([-1, -1, 0, 2, 2]))
print(unique_sorted([1.0, 1, 2.5, 2.5, 0]))
print(flatten([[1, 2], [3, 4]]))
print(flatten(([1, 2], (3, 4, 5))))
print(flatten([[1], [], [2, 3]]))

#print(flatten([[1, 2], "ab"]))
#print(min_max([]))
```
![alt text](images/lab02/img.2.1.png)

При введении:

print(flatten([[1, 2], "ab"]))

print(min_max([]))

Вывод

![alt text](images/lab02/img.2.1.1error.png)
![alt text](images/lab02/img.2.1.2error.png)

**Задание №2**

```
def check_rectangular(mat):
    if not mat:
        return True
    length = len(mat[0])
    for row in mat:
        if len(row) != length:
            return False
    return True


def transpose(mat):
    if not check_rectangular(mat):
        raise ValueError("Рваная матрица")
    if not mat:
        return []
    return [list(row) for row in zip(*mat)]


def row_sums(mat):
    if not check_rectangular(mat):
        raise ValueError("Рваная матрица")
    return [sum(row) for row in mat]


def col_sums(mat):
    if not check_rectangular(mat):
        raise ValueError("Рваная матрица")
    if not mat:
        return []
    return [sum(col) for col in zip(*mat)]
print(transpose([[1, 2, 3]]))
print(transpose([[1], [2], [3]]))
print(transpose([[1, 2], [3, 4]]))
print(transpose([]))
#print(transpose([[1, 2], [3]]))

print(row_sums([[1, 2, 3], [4, 5, 6]]))
print(row_sums([[-1, 1], [10, -10]] ))
print(row_sums([[0, 0], [0, 0]]))
#print(row_sums([[1, 2], [3]]))

print(col_sums([[1, 2, 3], [4, 5, 6]]))
print(col_sums([[-1, 1], [10, -10]] ))
print(col_sums([[0, 0], [0, 0]]))
#print(col_sums([[1, 2], [3]]))
```
![alt text](images/lab02/img.2.2.png)


При введении:

print(transpose([[1, 2], [3]]))

print(row_sums([[1, 2], [3]]))

print(col_sums([[1, 2], [3]]))

Вывод:
![alt text](images/lab02/img.2.2.1error.png)
![alt text](images/lab02/img.2.2.2error.png)
![alt text](images/lab02/img.2.2.3error.png)


**Задание №3**
```
from typing import Tuple

StudentRecord = Tuple[str, str, float]

def format_record(rec: StudentRecord) -> str:
    fio, group, gpa = rec
    fio_parts = [part.strip() for part in fio.split()]
    formatted_surname = fio_parts[0].capitalize()
    initials = ''.join([f'{name[0].upper()}.' for name in fio_parts[1:]])
    formatted_gpa = f'{gpa:.2f}'
    formatted_record = f"{formatted_surname} {initials}, гр. {group}, GPA {formatted_gpa}"
    return formatted_record

print(format_record(("Иванов Иван Иванович", "BIVT-25", 4.605)))
print(format_record(("Петров Пётр", "IKBO-12", 5.0)))
print(format_record(("Петров Пётр Петрович", "IKBO-12", 5.0)))
print(format_record(("  сидорова  анна   сергеевна ", "ABB-01", 3.999)))
#print(format_record(("  сидорова  анна   сергеевна ", 3.999)))
```
![alt text](images/lab02/img.2.3.png)

При введении:

print(format_record(("  сидорова  анна   сергеевна ", 3.999)))

Вывод:
![alt text](images/lab02/img.2.3.error.png)



<h2>Лабораторная работа №1</h2>

**Задание №1**

```
name=input("Имя: ")
age=int(input('Возрвст: '))
print(f'Привет {name}! Через год тебе будет {age+1}!')
```
![alt text](images/lab01/img01.png)

**Задание №2**

```
a = input("a: ").replace(',', '.')
b = input("b: ").replace(',', '.')
a = float(a)
b = float(b)
_sum = a + b
_avg = _sum / 2
print(f"sum={_sum:.2f}; avg={_avg:.2f}")
```
![alt text](images/lab01/img02.png)

**Задание №3**
```
price=float(input())
discount=float(input())
vat=float(input())
base=price*(1-discount/100)
vat_amount=base*(vat/100)
total=base+vat_amount
print(f'База после скидки:{base:.2f}₽')
print(f'НДС:{vat_amount:.2f}₽')
print(f'Итого к оплате:{total:.2f}₽')
```
![alt text](images/lab01/img03.png)

**Задание №4**
```
m=int(input('минуты:'))
hours=m//60
minutes=m%60
print(f'{hours}:{minutes:02d}')
```
![alt text](images/lab01/img04.png)

**Задание №5**
```
a, b, c = input().split()
print(f"ФИО: {a} {b} {c}")
print(f"Инициалы: {a[0]}{b[0]}{c[0]}.")
print(f"Длина (символов): {len(a) + len(b) + len(c) + 2}")
```
![alt text](images/lab01/img05.png)

**Задание №6**
```
N=int(input('in_1:'))
onsite=0
remote=0
for _ in range(N):
    count="in_"+str(_+2)+':'
    line=input(count).strip().split()
    surname,name,age,format_part=line
    if format_part=="True":
        onsite+=1
    else:
        remote+=1
print('out:',onsite, remote)
```
![alt text](images/lab01/img06.png)

**Задание №7**
```
encoded= input('in:')
first_char_pos = 0
for i, char in enumerate(encoded):
    if 'A' <= char <= 'Z':
        first_char_pos = i
        first_char = char
        break
digit_position = 0
for i, char in enumerate(encoded):
    if char.isdigit():
        digit_position = i
        break
second_char = encoded[digit_position + 1]
step = digit_position + 1 - first_char_pos
result = first_char + second_char 
current_position = digit_position + 1 + step
while current_position < len(encoded) and encoded[current_position] != '.':
    result += encoded[current_position]
    current_position += step
result += "." 
print('out:',result)

```
![alt text](images/lab01/img07.png)