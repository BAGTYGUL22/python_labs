# run_lab08.py
from src.lab08.serialize import students_from_json, students_to_json

# 1. Загружаем студентов из входного файла
students = students_from_json("data/lab08/students_input.json")

# 2. Выводим их в консоль (опционально)
for s in students:
    print(s)

# 3. Сохраняем обратно — это и будет students_output.json
students_to_json(students, "data/lab08/students_output.json")

print("\n✅ Файл students_output.json успешно создан!")
