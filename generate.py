import random

from nltk.tokenize import WhitespaceTokenizer
from nltk.util import ngrams

file = 'corpus.txt'


def open_file():
    with open(f'{file}', 'r', encoding='UTF-8') as f:
        content = f.read()
        tokenized = WhitespaceTokenizer().tokenize(content)
        trigrams = list(ngrams(tokenized, 3))
        return trigrams


def corpus_count(last_tokens, trigrams):
    corpus_cnt = {}
    for triple in trigrams:
        if triple[:2] == last_tokens:
            x = ' '.join(triple[:2])
            if x not in corpus_cnt:
                corpus_cnt[x] = {}
            tail_cnt = corpus_cnt[x]
            tail_cnt[triple[2]] = tail_cnt.get(triple[2], 0) + 1

    keys = list(corpus_cnt[x].keys())
    weights = list(corpus_cnt[x].values())
    return random.choices(keys, weights=weights)


def get_first_words():
    random_triple = random.choice(open_file())
    if random_triple[0].istitle() and random_triple[0][-1] not in ['.', '!',
                                                                   '?']:
        return random_triple[0], random_triple[1]
    return get_first_words()


def generate():
    result = []
    while True:
        if len(result) == 0:
            result.extend(get_first_words())
        last_tokens = (result[-2], result[-1]) if len(result) >= 2 else (
            result[-1],)
        random_token = corpus_count(last_tokens, open_file())
        result.append(random_token[0])
        if random_token[0][-1] in ['.', '!', '?'] and len(result) > 5:
            break

    return ' '.join(result)
