import sys
import math
import random


def load_file(file_name):
    with open(file_name) as f:
        data = f.read()
    return data


def parse_sentence(sentence, n):
    ngrams = []

    sentence = sentence.split()
    if n > 1:
        sentence = ["phi"] + sentence

    for x in range(n, len(sentence)+1):
        ngram = " ".join(sentence[x-n:x])
        ngrams.append(ngram)

    return ngrams


def parse_corpus(data, n):
    ngrams = {}
    total = 0

    data = data.lower()
    data = data.splitlines()

    for sentence in data:
        grams = parse_sentence(sentence, n)
        for gram in grams:
            total += 1
            if gram in ngrams:
                ngrams[gram] += 1
            else:
                ngrams[gram] = 1

    return ngrams, total


def prob_sentence_uni(sentence, model, total):
    p = 0
    sentence = sentence.split()
    for word in sentence:
        p += math.log2((model[word]) / total)
    return p


def prob_sentence_bi(sentence, u_model, b_model):
    total = 0

    sentence = sentence.split()
    sentence = ["phi"] + sentence
    for x in range(1, len(sentence)):
        bigram = sentence[x-1] + ' ' + sentence[x]
        if bigram in b_model:
            total += math.log2(b_model[bigram] / u_model[sentence[x-1]])
        else:
            return 0
    return total


def prob_sentence_bi_smooth(sentence, u_model, b_model):
    total = 0

    sentence = sentence.split()
    sentence = ["phi"] + sentence
    for x in range(1, len(sentence)):
        bigram = sentence[x-1] + ' ' + sentence[x]
        div = u_model[sentence[x-1]] + len(u_model.keys()) - 1
        if bigram in b_model:
            total += math.log2((b_model[bigram] + 1) / div)
        else:
            total += math.log2(1 / div)
    return total


def gen_sentence(seed, model):
    curr_seed = seed
    sentence = curr_seed

    while len(sentence.split()) < 10:
        candidates = {}
        for key, value in model.items():
            if key.split()[0] == curr_seed:
                candidates[key] = value

        if len(candidates.keys()) == 0:
            return sentence

        total = sum(candidates.values())
        rand = random.uniform(0, total)
        start = 0
        for key, value in candidates.items():
            start += value
            if start > rand:
                new_word = key.split()[1]
                sentence = sentence + ' ' + new_word
                curr_seed = new_word
                if curr_seed == '.' or curr_seed == '?' or curr_seed == '!':
                    return sentence
                break

    return sentence


def run():

    sentence = "This is a test sentence for me"

    for word in sentence:
        for char in word:
            print(char)

    # get file names from command line input
    train = sys.argv[1]
    mode = sys.argv[2]
    run = sys.argv[3]

    train_data = load_file(train)

    unigrams, unigrams_total = parse_corpus(train_data, 1)

    # count the number of sentences (and therefore the number of phi's and store separately
    # (not included in the unigrams_total)
    unigrams["phi"] = len(train_data.splitlines())

    bigrams, bigrams_total = parse_corpus(train_data, 2)

    if mode == "-test":

        test_data = load_file(run)

        test_data = test_data.splitlines()

        for sentence in test_data:
            print("S = " + sentence)

            sentence = sentence.lower()

            u = prob_sentence_uni(sentence, unigrams, unigrams_total)
            b = prob_sentence_bi(sentence, unigrams, bigrams)
            bs = prob_sentence_bi_smooth(sentence, unigrams, bigrams)

            print()
            print("Unsmoothed Unigrams, logprob(S) = {0:.4f}".format(u))
            if b == 0:
                print("Unsmoothed Bigrams, logprob(S) = undefined")
            else:
                print("Unsmoothed Bigrams, logprob(S) = {0:.4f}".format(b))
            print("Smoothed Bigrams, logprob(S) = {0:.4f}".format(bs))
            print()

    if mode == "-gen":

        seed_data = load_file(run)

        seed_data = seed_data.splitlines()

        for seed in seed_data:
            print("Seed = " + seed)

            seed = seed.lower()

            print()
            for x in range(1, 11):
                print("Sentence " + str(x) + ": " + gen_sentence(seed, bigrams))
            print()


run()
