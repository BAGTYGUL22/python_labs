a = input("a: ").replace(",", ".")
b = input("b: ").replace(",", ".")
a = float(a)
b = float(b)
_sum = a + b
_avg = _sum / 2
print(f"sum={_sum:.2f}; avg={_avg:.2f}")
