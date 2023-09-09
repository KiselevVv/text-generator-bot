import random
from collections import defaultdict
from typing import List, Tuple

from nltk.tokenize import WhitespaceTokenizer
from nltk.util import ngrams


class TextGenerator:
    """
    Генератор текста на основе троек слов из корпуса.
    attr:
        file: Путь к файлу с корпусом текста.
        cached_trigrams: Кешированные тройки слов из корпуса.
    """
    def __init__(self):
        self.file = 'corpus/corpus.txt'
        self.cached_trigrams = None

    def get_trigrams(self) -> List[Tuple[str, str, str]]:
        """Возвращает тройки слов из корпуса текста."""
        if self.cached_trigrams is not None:
            return self.cached_trigrams

        with open(f'{self.file}', 'r', encoding='UTF-8') as f:
            content = f.read()
            tokenized = WhitespaceTokenizer().tokenize(content)
            self.cached_trigrams = list(ngrams(tokenized, 3))
            return self.cached_trigrams

    def corpus_count(self, last_tokens: Tuple[str, str]) -> str:
        """
        Генерирует следующее слово на основе последних двух слов.
        :param last_tokens: Последние два слова.
        :return: Следующее слово.
        """
        trigrams = self.get_trigrams()
        corpus_cnt = defaultdict(lambda: defaultdict(int))
        for triple in trigrams:
            if triple[:2] == last_tokens:
                x = ' '.join(triple[:2])
                tail_cnt = corpus_cnt[x]
                tail_cnt[triple[2]] += 1

        keys = list(corpus_cnt[x].keys())
        weights = list(corpus_cnt[x].values())
        return random.choices(keys, weights=weights)

    def get_first_words(self) -> Tuple[str, str]:
        """
        Генерирует первые два слова в начале предложения.
        :return: Первые два слова.
        """
        random_triple = random.choice(self.get_trigrams())
        if random_triple[0].istitle() and random_triple[0][-1] not in ['.',
                                                                       '!',
                                                                       '?']:
            return random_triple[0], random_triple[1]
        return self.get_first_words()

    def generate(self) -> str:
        """
        Генерирует текст на основе корпуса текста.
        :return: Сгенерированное предложение.
        """
        result = []
        while True:
            if len(result) == 0:
                result.extend(self.get_first_words())
            last_tokens = (result[-2], result[-1])
            random_token = self.corpus_count(last_tokens)
            result.append(random_token[0])
            if random_token[0][-1] in ['.', '!', '?'] and len(result) > 7:
                break

        return ' '.join(result)
