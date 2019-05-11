import nltk
from nltk.corpus import cmudict
from nltk.util import ngrams
from nltk.tag import pos_tag
from collections import defaultdict
import random
import more_itertools



def generate_haiku(lists, pro_dict, cfd, rank, start=None):
    if not start:
        start = random_word(random.randrange(1, 6), lists)

    count = syllable_count(start, pro_dict)

    haiku = []
    prefix = list('0' * (rank - 1))
    haiku.append(start + ' ' + generate_line(prefix + [start], 5 - count, lists, pro_dict, cfd, rank))
    haiku.append(generate_line((prefix + haiku[-1].split())[-rank:], 7, lists, pro_dict, cfd, rank))
    haiku.append(generate_line((prefix + haiku[-1].split())[-rank:], 5, lists, pro_dict, cfd, rank))
    print('\n'.join(haiku))


def generate_line(start, length, lists, pro_dict, cfd, rank):
    line = start
    
    last = line[-(rank - 1):]
    while length > 0:
        options = (more_itertools.flatten([option]*cfd[' '.join(last)][option] for option in cfd[' '.join(last)]))
        
        options = [option for option in options if syllable_count(option, pro_dict) <= length and option != last]
        if length <= 2:
            options = [option for option in options if pos_tag(option)[0][1] not in ['IN', 'DT', 'TO']]

        if options:
            choice = random.choice(options)
        else:
            choice = random_word(random.randrange(1, length+1), lists)
            print('-' + choice + '-')
        length -= syllable_count(choice, pro_dict)
        line.append(choice)

        last = line[-(rank - 1):]

    return ' '.join(line[rank:])


def random_word(syl, lists):
    return random.choice(lists[syl - 1])


def syllable_count(word, pro_dict):
    return [sum(any(c.isdigit() for c in part) for part in pro) for pro in pro_dict[word]][0]


def my_ngrams(corp, rank, *args, **kwargs):
    prefix = list('0'* (rank - 1))
    corp = [[elem for elem in lst if elem != '/'] for lst in corp]
    corp = [prefix + lst for lst in corp]
    x = [[lst[i:i+rank] for i in range(len(lst)-rank)] for lst in corp]
    return list(more_itertools.flatten(x))
    


def setup(path, rank):
    pro_dict = cmudict.dict()
    pro_dict['0'] = [['a']]

    with open(path, 'rb') as haiku_file:
        corp = [line.decode('utf-8').split()  for line in haiku_file]

    corp = [[word.lower() for word in line] for line in corp]

    lists = [[word for word in more_itertools.flatten(corp) if word in pro_dict and syllable_count(word, pro_dict) == i] for i in range(1, 8)]
    
    corp_ngrams = [words for words in my_ngrams(corp, rank, pad_left=True) if all(w in pro_dict for w in words)]
    
    cfd = defaultdict(lambda: defaultdict(int))

    for *head, tail in corp_ngrams:
        cfd[' '.join(head)][tail] += 1

    return lists, pro_dict, cfd


if __name__ == "__main__":
    for _ in range(3):
        rank = 3
        lists, pro_dict, cfd = setup('haikus.txt', rank)
        generate_haiku(lists, pro_dict, cfd, rank)
        print("-------------")
