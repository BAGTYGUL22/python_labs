fio = input("ФИО: ")
fio = fio.strip()
words = fio.split()
initials = "".join([word[0].upper() for word in words])

print("Инициалы:", initials + ".")
print("Длина (символов):", len(fio))