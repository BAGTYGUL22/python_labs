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

    # Запись строк в XLSX
    for row in rows:
        ws.append(row)

    # Автоширина колонок (минимум 8)
    for col_idx, col_cells in enumerate(ws.columns, start=1):
        max_length = max(len(str(cell.value)) if cell.value is not None else 0 for cell in col_cells)
        adjusted_width = max(max_length, 8)
        col_letter = ws.cell(row=1, column=col_idx).column_letter
        ws.column_dimensions[col_letter].width = adjusted_width

    wb.save(xlsx_file)
csv_to_xlsx('src/lab05/samples/example2.csv', 'src/lab05/out/example3_csv.xlsx')