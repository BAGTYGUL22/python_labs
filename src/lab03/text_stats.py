import sys
from text import *

def text_info():
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


text_info()
