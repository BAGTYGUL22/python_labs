import sys
from text import *

def text_info():
    text = sys.stdin.readline().strip()
    words = sorted(tokenize(normalize(text)), key=len, reverse=True)
    print(words)
    print(f"Всего слов: {len(tokenize(normalize(text)))}")
    print(f"Уникальных слов: {len(set(tokenize(normalize(text))))}")
    print("Топ-5:")
    print("Слово" + " " * (len(max("Слово", max(words), key=len))-len(min("Слово", max(words), key=len))+1) + "|")
    for w in count_freq(tokenize(normalize(text))):
        print(f"{w}:{count_freq(tokenize(normalize(text))).get(w)}")

text_info()