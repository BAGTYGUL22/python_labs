import sys
from text import normalize,tokenize,count_freq,top_n
def main():
    text = sys.stdin.read().strip()
    normalized_text = normalize(text)
    tokens = tokenize(normalized_text)
    word_freq = count_freq(tokens)
    top5 = top_n(word_freq, 5)
    print(f"Всего слов: {len(tokens)}")
    print(f"Уникальных слов: {len(word_freq)}")
    print("Топ-5:")
    for word, count in top5:
        print(f"{word}:{count}")
 