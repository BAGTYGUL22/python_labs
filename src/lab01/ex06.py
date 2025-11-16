N = int(input("in_1:"))
onsite = 0
remote = 0
for _ in range(N):
    count = "in_" + str(_ + 2) + ":"
    line = input(count).strip().split()
    surname, name, age, format_part = line
    if format_part == "True":
        onsite += 1
    else:
        remote += 1
print("out:", onsite, remote)
