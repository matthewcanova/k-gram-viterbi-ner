import sys
import math


def load_file(file_name):
    with open(file_name) as f:
        data = f.read()
    return data


def parse_corpus(data):

    data = data.lower()
    data = data.splitlines()

    return data


def parse_probs(data, pos):

    trans = {}
    emit = {}

    data = data.splitlines()

    for line in data:
        line = line.split()
        x = line[0]
        y = line[1]
        prob = math.log2(float(line[2]))
        #prob = float(line[2])
        if x in pos and y in pos:
            if x in trans.keys():
                trans[x][y] = prob
            else:
                trans[x] = {y: prob}
        else:
            if x in emit.keys():
                emit[x][y] = prob
            else:
                emit[x] = {y: prob}

    return trans, emit


def get_prob(probs, key1, key2):
    try:
        return probs[key1][key2]
    except KeyError:
        return math.log2(0.0001)


def viterbi(obs, pos, trans, emit):
    obs = obs.split()

    score = [{}]
    back = [{}]

    for tag in pos:
        score[0][tag] = get_prob(emit, obs[0], tag) + get_prob(trans, tag, "phi")
        back[0][tag] = None

    for w in range(1, len(obs)):
        score.append({})
        back.append({})
        for tag in pos:
            vals = {}
            for k in pos:
                vals[k] = score[w-1][k] + get_prob(trans, tag, k)
            v = list(vals.values())
            k = list(vals.keys())
            max_val = max(v)
            max_pos = k[v.index(max_val)]
            score[w][tag] = get_prob(emit, obs[w], tag) + max_val
            back[w][tag] = max_pos
    return score, back


def identify_sequence(obs, score, back, pos):
    obs = obs.split()

    seq = [None] * len(obs)

    vals = {}
    for tag in pos:
        vals[tag] = score[len(obs)-1][tag]
    v = list(vals.values())
    k = list(vals.keys())
    max_pos = k[v.index(max(v))]

    seq[len(obs)-1] = max_pos

    for x in range(len(obs)-2, -1, -1):
        seq[x] = back[x+1][seq[x+1]]

    return seq


def run():
    prob_file = sys.argv[1]
    test_file = sys.argv[2]

    sentences = load_file(test_file)
    sentences = parse_corpus(sentences)

    pos = ["noun", "verb", "inf", "prep", "phi"]

    probabilities = load_file(prob_file)
    trans, emit = parse_probs(probabilities, pos)

    for sentence in sentences:
        print("PROCESSING SENTENCE: " + sentence + "\n")

        print("FINAL VITERBI NETWORK\n")

        score, back = viterbi(sentence, pos, trans, emit)

        pos_list = ["noun", "verb", "inf", "prep"]
        for i in range(len(sentence.split())):
            for p in pos_list:
                print("P(" + sentence.split()[i] + "=" + p + ") = {0:.4f}".format(score[i][p]))

        print("\nFINAL BACKPTR NETWORK\n")

        for i in range(1, len(sentence.split())):
            for p in pos_list:
                print("Backptr(" + sentence.split()[i] + "=" + p + ") = " + back[i][p])

        v = list(score[len(sentence.split())-1].values())
        max_value = max(v)

        print("\nBEST TAG SEQUENCE HAS LOG PROBABILITY = {0:.4f}".format(max_value))

        sequence = identify_sequence(sentence, score, back, pos)

        for i in range(len(sentence.split())-1, -1, -1):
            print(sentence.split()[i] + " -> " + sequence[i])

        print()


run()
