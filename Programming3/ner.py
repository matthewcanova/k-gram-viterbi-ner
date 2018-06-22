

# the words and pos tags in this file will define the lexicon
train_file = "train.txt"

# the words and pos tags in this file will be tagged based on the existing lexicon and pos tags
test_file = "test.txt"

# check against to see if something is a location
loc_file = "locs.txt"

# all the ftypes that could be requested
ftypes = "WORD POSCON POS WORDCON ABBR CAP LOCATION"

ftypes = ftypes.split()
ft = set()
for typ in ftypes:
    ft.add(typ)

locations = set()
with open(loc_file) as file:
    for line in file:
        locations.add(line.strip())


def read_file(file):
    data = []
    with open(file) as train:
        text = train.readlines()
        for line in text:
            line = line.split()
            data.append(line)
    return data


def is_abbreviation(word):
    return word[len(word)-1] == '.' and word.replace(".", "").isalpha() and len(word) < 5


def process_train_readable(data, ftypes):
    index = 0
    lexicon = set()
    pos_lexicon = set()
    with open("train.txt.readable", 'w') as file:
        while index < len(data):
            sentence = []
            while len(data[index]) is not 0:
                sentence.append(data[index])
                lexicon.add(data[index][2])
                pos_lexicon.add(data[index][1])
                index += 1
            results = process_train_sentence(sentence, ftypes)
            file.write(results)
            while index < len(data) and len(data[index]) is 0:
                index += 1

    return lexicon, pos_lexicon


def process_train_sentence(sentence, ftypes):
    string = ""
    for index in range(len(sentence)):

        if "WORD" in ftypes:
            string += "WORD: " + sentence[index][2] + '\n'

        string += "WORDCON: "
        if "WORDCON" in ftypes:
            if index is 0:
                string += "PHI "
            else:
                string += sentence[index-1][2] + ' '
            if index is len(sentence)-1:
                string += "OMEGA\n"
            else:
                string += sentence[index+1][2] + '\n'
        else:
            string += 'n/a' + '\n'

        string += "POS: "
        if "POS" in ftypes:
            string += sentence[index][1] + '\n'
        else:
            string += 'n/a' + '\n'

        string += "POSCON: "
        if "POSCON" in ftypes:
            if index is 0:
                string += "PHIPOS "
            else:
                string += sentence[index-1][1] + ' '
            if index is len(sentence)-1:
                string += "OMEGAPOS\n"
            else:
                string += sentence[index+1][1] + '\n'
        else:
            string += 'n/a' + '\n'

        string += "ABBR: "
        if "ABBR" in ftypes:
            if is_abbreviation(sentence[index][2]):
                string += "yes\n"
            else:
                string += "no\n"
        else:
            string += 'n/a' + '\n'

        string += "CAP: "
        if "CAP" in ftypes:
            if sentence[index][2][0].isupper():
                string += "yes\n"
            else:
                string += "no\n"
        else:
            string += 'n/a' + '\n'

        string += "LOCATION: "
        if "LOCATION" in ftypes:
            if sentence[index][2] in locations:
                string += "yes\n"
            else:
                string += "no\n"
        else:
            string += 'n/a' + '\n'

        string += '\n'

    return string


def process_test_readable(data, ftypes, lexicon, pos_lexicon):
    index = 0
    with open("test.txt.readable", 'w') as file:
        while index < len(data):
            sentence = []
            while index < len(data) and len(data[index]) is not 0:
                sentence.append(data[index])
                index += 1
            results = process_test_sentence(sentence, ftypes, lexicon, pos_lexicon)
            file.write(results)
            while index < len(data) and len(data[index]) is 0:
                index += 1


def process_test_sentence(sentence, ftypes, lexicon, pos_lexicon):
    string = ""
    for index in range(len(sentence)):

        if "WORD" in ftypes:
            if sentence[index][2] in lexicon:
                string += "WORD: " + sentence[index][2] + '\n'
            else:
                string += "WORD: " + "UNK" + '\n'

        string += "WORDCON: "
        if "WORDCON" in ftypes:

            if index is 0:
                string += "PHI "
            else:
                if sentence[index-1][2] in lexicon:
                    string += sentence[index - 1][2] + ' '
                else:
                    string += "UNK" + ' '

            if index is len(sentence) - 1:
                string += "OMEGA\n"
            else:
                if sentence[index+1][2] in lexicon:
                    string += sentence[index + 1][2] + '\n'
                else:
                    string += "UNK" + '\n'
        else:
            string += 'n/a' + '\n'

        string += "POS: "
        if "POS" in ftypes:
            if sentence[index][1] in pos_lexicon:
                string += sentence[index][1] + '\n'
            else:
                string += "UNKPOS" + '\n'
        else:
            string += 'n/a' + '\n'

        string += "POCON: "
        if "POSCON" in ftypes:

            if index is 0:
                string += "PHIPOS "
            else:
                if sentence[index-1][1] in pos_lexicon:
                    string += sentence[index - 1][1] + ' '
                else:
                    string += "UNKPOS" + ' '

            if index is len(sentence) - 1:
                string += "OMEGAPOS\n"
            else:
                if sentence[index+1][1] in pos_lexicon:
                    string += sentence[index + 1][1] + '\n'
                else:
                    string += "UNKPOS" + '\n'
        else:
            string += 'n/a' + '\n'

        string += "ABBR: "
        if "ABBR" in ftypes:
            if is_abbreviation(sentence[index][2]):
                string += "yes\n"
            else:
                string += "no\n"
        else:
            string += 'n/a' + '\n'

        string += "CAP: "
        if "CAP" in ftypes:
            if sentence[index][2][0].isupper():
                string += "yes\n"
            else:
                string += "no\n"
        else:
            string += 'n/a' + '\n'

        string += "LOCATION: "
        if "LOCATION" in ftypes:
            if sentence[index][2] in locations:
                string += "yes\n"
            else:
                string += "no\n"
        else:
            string += 'n/a' + '\n'

        string += '\n'

    return string


def process_training_features(data, ft, lex, pos_lex, feature_set):
    index = 0
    with open("train.txt.vector", 'w') as file:
        while index < len(data):
            sentence = []
            while len(data[index]) is not 0:
                sentence.append(data[index])
                index += 1
            results = process_train_vector(sentence, ft, lex, pos_lex, feature_set)
            file.write(results)
            while index < len(data) and len(data[index]) is 0:
                index += 1


def process_train_vector(sentence, ft, lex, pos_lex, feature_set):
    string = ""
    label = {"O": "0", "B-PER": "1", "I-PER": "2", "B-LOC": "3", "I-LOC": "4", "B-ORG": "5", "I-ORG": "6"}

    for index in range(len(sentence)):

        string += label[sentence[index][0]] + ' '

        feature_list = []

        if "WORD" in ftypes:
            feature_list.append(feature_set[sentence[index][2] + '1'])

        if "WORDCON" in ftypes:
            if index is 0:
                feature_list.append(feature_set["PHI2"])
            else:
                feature_list.append(feature_set[sentence[index - 1][2] + '2'])

            if index is len(sentence) - 1:
                feature_list.append(feature_set["OMEGA3"])
            else:
                feature_list.append(feature_set[sentence[index + 1][2] + '3'])

        if "POS" in ftypes:
            feature_list.append(feature_set[sentence[index][1] + '4'])

        if "POSCON" in ftypes:
            if index is 0:
                feature_list.append(feature_set["PHIPOS5"])
            else:
                feature_list.append(feature_set[sentence[index - 1][1] + '5'])

            if index is len(sentence) - 1:
                feature_list.append(feature_set["OMEGAPOS6"])
            else:
                feature_list.append(feature_set[sentence[index + 1][1] + '6'])

        if "ABBR" in ftypes:
            if is_abbreviation(sentence[index][2]):
                feature_list.append(feature_set["ABBR"])

        if "CAP" in ftypes:
            if sentence[index][2][0].isupper():
                feature_list.append(feature_set["CAP"])

        if "LOCATION" in ftypes:
            if sentence[index][2] in locations:
                feature_list.append(feature_set["LOCATION"])

        feature_list.sort()

        for f in feature_list:
            string = string + str(f) + ':1 '

        string.strip()
        string += '\n'

    return string


def process_test_features(data, ftypes, lexicon, pos_lexicon, feature_set):
    index = 0
    with open("test.txt.vector", 'w') as file:
        while index < len(data):
            sentence = []
            while index < len(data) and len(data[index]) is not 0:
                sentence.append(data[index])
                index += 1
            results = process_test_vector(sentence, ftypes, lexicon, pos_lexicon, feature_set)
            file.write(results)
            while index < len(data) and len(data[index]) is 0:
                index += 1


def process_test_vector(sentence, ft, lex, pos_lex, feature_set):
    string = ""
    label = {"O": "0", "B-PER": "1", "I-PER": "2", "B-LOC": "3", "I-LOC": "4", "B-ORG": "5", "I-ORG": "6"}

    for index in range(len(sentence)):

        string += label[sentence[index][0]] + ' '

        feature_list = []

        if "WORD" in ftypes:
            if sentence[index][2] in lex:
                feature_list.append(feature_set[sentence[index][2] + '1'])
            else:
                feature_list.append(feature_set["UNK1"])

        if "WORDCON" in ftypes:
            if index is 0:
                feature_list.append(feature_set["PHI2"])
            else:
                if sentence[index - 1][2] in lex:
                    feature_list.append(feature_set[sentence[index - 1][2] + '2'])
                else:
                    feature_list.append(feature_set["UNK2"])

            if index is len(sentence) - 1:
                feature_list.append(feature_set["OMEGA3"])
            else:
                if sentence[index + 1][2] in lex:
                    feature_list.append(feature_set[sentence[index + 1][2] + '3'])
                else:
                    feature_list.append(feature_set["UNK3"])

        if "POS" in ftypes:
            if sentence[index][1] in pos_lex:
                feature_list.append(feature_set[sentence[index][1] + '4'])
            else:
                feature_list.append(feature_set["UNKPOS4"])

        if "POSCON" in ftypes:
            if index is 0:
                feature_list.append(feature_set["PHIPOS5"])
            else:
                if sentence[index - 1][1] in pos_lex:
                    feature_list.append(feature_set[sentence[index - 1][1] + '5'])
                else:
                    feature_list.append(feature_set["UNKPOS5"])

            if index is len(sentence) - 1:
                feature_list.append(feature_set["OMEGAPOS6"])
            else:
                if sentence[index + 1][1] in pos_lex:
                    feature_list.append(feature_set[sentence[index + 1][1] + '6'])
                else:
                    feature_list.append(feature_set["UNKPOS6"])

        if "ABBR" in ftypes:
            if is_abbreviation(sentence[index][2]):
                feature_list.append(feature_set["ABBR"])

        if "CAP" in ftypes:
            if sentence[index][2][0].isupper():
                feature_list.append(feature_set["CAP"])

        if "LOCATION" in ftypes:
            if sentence[index][2] in locations:
                feature_list.append(feature_set["LOCATION"])

        feature_list.sort()

        for f in feature_list:
            string = string + str(f) + ':1 '

        string.strip()
        string += '\n'

    return string

def run():

    train_data = read_file(train_file)
    test_data = read_file(test_file)


    lex, pos_lex = process_train_readable(train_data, ft)

    process_test_readable(test_data, ft, lex, pos_lex)

    lex.add("PHI")
    lex.add("OMEGA")
    lex.add("UNK")
    pos_lex.add("PHIPOS")
    pos_lex.add("OMEGAPOS")
    pos_lex.add("UNKPOS")

    feature_set = {}
    feature_index = 1

    if "ABBR" in ft:
        feature_set["ABBR"] = feature_index
        feature_index += 1
    if "CAP" in ft:
        feature_set["CAP"] = feature_index
        feature_index += 1
    if "LOCATION" in ft:
        feature_set["LOCATION"] = feature_index
        feature_index += 1

    for word in lex:
        feature_set[word + "1"] = feature_index
        feature_index += 1
        feature_set[word + "2"] = feature_index
        feature_index += 1
        feature_set[word + "3"] = feature_index
        feature_index += 1

    for pos in pos_lex:
        feature_set[pos + "4"] = feature_index
        feature_index += 1
        feature_set[pos + "5"] = feature_index
        feature_index += 1
        feature_set[pos + "6"] = feature_index
        feature_index += 1

    process_training_features(train_data, ft, lex, pos_lex, feature_set)
    process_test_features(test_data, ft, lex, pos_lex, feature_set)


run()
