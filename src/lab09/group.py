import csv
from pathlib import Path
from typing import List, Dict, Any
from src.lab08.models import Student


class Group:
    FIELDS = ["fio", "birthdate", "group", "gpa"]

    def __init__(self, storage_path: str):
        self.path = Path(storage_path)
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        """Создаёт CSV-файл с заголовком, если он не существует."""
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.FIELDS)
                writer.writeheader()

    def _read_all(self) -> List[Dict[str, str]]:
        """Читает все строки из CSV (включая заголовок, но пропускает его)."""
        if not self.path.exists() or self.path.stat().st_size == 0:
            return []

        with open(self.path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if set(reader.fieldnames) != set(self.FIELDS):
                raise ValueError(
                    f"Некорректные заголовки в CSV. Ожидались: {self.FIELDS}"
                )
            return [row for row in reader]

    def _write_all(self, rows: List[Dict[str, Any]]):
        """Записывает все строки в CSV (с заголовком)."""
        with open(self.path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDS)
            writer.writeheader()
            writer.writerows(rows)

    def list(self) -> List[Student]:
        """Возвращает всех студентов."""
        rows = self._read_all()
        students = []
        for row in rows:
            try:
                row["gpa"] = float(row["gpa"])
                student = Student(**row)
                students.append(student)
            except (ValueError, TypeError) as e:
                raise ValueError(f"Некорректные данные в строке: {row}") from e
        return students

    def add(self, student: Student):
        """Добавляет нового студента."""
        rows = self._read_all()
        new_row = student.to_dict()
        rows.append(new_row)
        self._write_all(rows)

    def find(self, substr: str) -> List[Student]:
        """Поиск по подстроке в ФИО (регистронезависимо)."""
        all_students = self.list()
        substr = substr.lower()
        return [s for s in all_students if substr in s.fio.lower()]

    def remove(self, fio: str):
        """Удаляет записи с точным совпадением по ФИО."""
        rows = self._read_all()
        filtered = [row for row in rows if row["fio"] != fio]
        if len(filtered) == len(rows):
            raise ValueError(f"Студент с ФИО '{fio}' не найден.")
        self._write_all(filtered)

    def update(self, fio: str, **fields):
        """Обновляет поля у студента с точным совпадением по ФИО."""
        if not fields:
            return

        rows = self._read_all()
        found = False
        for row in rows:
            if row["fio"] == fio:
                for key, value in fields.items():
                    if key not in self.FIELDS:
                        raise ValueError(f"Поле '{key}' не поддерживается.")
                    row[key] = value
                found = True

        if not found:
            raise ValueError(f"Студент с ФИО '{fio}' не найден.")

        for row in rows:
            try:
                Student(
                    fio=row["fio"],
                    birthdate=row["birthdate"],
                    group=row["group"],
                    gpa=float(row["gpa"]),
                )
            except Exception as e:
                raise ValueError(f"Обновление привело к некорректным данным: {e}")

        self._write_all(rows)

    def stats(self) -> Dict[str, Any]:
        """Возвращает статистику по студентам."""
        students = self.list()
        if not students:
            return {
                "count": 0,
                "min_gpa": 0,
                "max_gpa": 0,
                "avg_gpa": 0,
                "groups": {},
                "top_5_students": [],
            }

        gpas = [s.gpa for s in students]
        group_counts = {}
        for s in students:
            group_counts[s.group] = group_counts.get(s.group, 0) + 1

        top_5 = sorted(students, key=lambda x: x.gpa, reverse=True)[:5]
        top_5_serialized = [{"fio": s.fio, "gpa": s.gpa} for s in top_5]

        return {
            "count": len(students),
            "min_gpa": min(gpas),
            "max_gpa": max(gpas),
            "avg_gpa": round(sum(gpas) / len(gpas), 2),
            "groups": group_counts,
            "top_5_students": top_5_serialized,
        }


if __name__ == "__main__":
    import sys
    import os

    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
    from src.lab08.models import Student

    db = Group("data/lab09/students.csv")

    print("1. Исходный список студентов:")
    for s in db.list():
        print(f"   {s}")

    print("\n2. Добавляем: Мередова Огулабат Курбанмамедовна")
    db.add(
        Student(
            fio="Мередова Огулабат Курбанмамедовна",
            birthdate="2006-02-09",
            group="БМБ2404",
            gpa=5.0,
        )
    )

    print("\n3. Список после добавления:")
    for s in db.list():
        print(f"   {s}")

    print("\n4. Поиск по 'Мередова':")
    for s in db.find("Мередова"):
        print(f"   {s}")

    print("\n5. Статистика:")
    st = db.stats()
    print(f"   Всего: {st['count']}")
    print(f"   Средний GPA: {st['avg_gpa']}")
    print("   Группы:")
    for grp, cnt in st["groups"].items():
        print(f"     {grp}: {cnt}")
