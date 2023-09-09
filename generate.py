import random
from collections import defaultdict

from nltk.tokenize import WhitespaceTokenizer
from nltk.util import ngrams


class TextGenerator:
    def __init__(self):
        self.file = 'corpus/corpus.txt'
        self.cached_trigrams = None

    def get_trigrams(self):
        if self.cached_trigrams is not None:
            return self.cached_trigrams

        with open(f'{self.file}', 'r', encoding='UTF-8') as f:
            content = f.read()
            tokenized = WhitespaceTokenizer().tokenize(content)
            self.cached_trigrams = list(ngrams(tokenized, 3))
            return self.cached_trigrams

    def corpus_count(self, last_tokens):
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

    def get_first_words(self):
        random_triple = random.choice(self.get_trigrams())
        if random_triple[0].istitle() and random_triple[0][-1] not in ['.',
                                                                       '!',
                                                                       '?']:
            return random_triple[0], random_triple[1]
        return self.get_first_words()

    def generate(self):
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
