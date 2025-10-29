import argparse

parser = argparse.ArgumentParser(description="Пример CLI")
parser.add_argument("--name", required=True, help="Имя пользователя")
args = parser.parse_args()
print(f"Привет, {args.name}!")