import  argparse
from text import *

def cat(text, n):
    f = open(text, "r").readlines()
    if not n:
        for i in f:
            print(i.replace("\n", ""))
    else:
        f = enumerate(f)
        for i in f:
            print(i[0],i[1].replace("\n", ""))


def stats(txt,n):
    f = open(txt, "r").read()
    txt = top_n(count_freq(tokenize(normalize(f))),n)
    for a in txt:
        print(a[1],a[0])



# def main():
parser = argparse.ArgumentParser("CLI‑утилиты лабораторной №6")
subparsers = parser.add_subparsers(dest="command")

# подкоманда cat
cat_parser = subparsers.add_parser("cat",help = "Вывести содержимое файла")
cat_parser.add_argument("--input",required = True)
cat_parser.add_argument("-n", action="store_true",help = "Нумировать строки")

# подкоманда stats
stats_parser = subparsers.add_parser("stats",help = "Частоты слез")
stats_parser.add_argument("--input",required = True)
stats_parser.add_argument("--top",type = int, default = 5)

args = parser.parse_args()
# print("DEBUG:", args)

if args.command == "cat":
    cat(args.input,args.n)

if args.command == "stats":
    stats(args.input,args.top)