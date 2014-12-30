from copy import deepcopy

__author__ = 'scobb'
from pattern import PatternEntry
debug = False


def main():
    in_file = 'sample.in'
    f = open(in_file)
    pattern = f.readline().strip()
    phrase = f.readline().strip()
    if debug:
        print('pattern: %s' % pattern)
        print('phrase: %s' % phrase)
    f.close()

    val = find_pattern(pattern, phrase, {}, 0, 0, 0)
    if debug:
        print(str(val))


def find_pattern(pattern, phrase, dictionary, pattern_ind, phrase_ind, inner_pattern_ind):
    """

    :param pattern: total pattern we're trying to match
    :param phrase: phrase we're trying to fit to the pattern
    :param dictionary: current
    :param pattern_ind: index we're examining in the pattern
    :param phrase_ind: index we're examining in the pattern
    :param inner_pattern_ind: index we're comparing within an existing pattern
    :return: boolean - is there a valid assignment? DECISION version
    """
    dictionary = deepcopy(dictionary)
    if debug:
        print(str(dictionary))
    if phrase_ind == len(phrase):
        if pattern_ind == len(pattern) - 1 and inner_pattern_ind == len(dictionary[pattern[pattern_ind]]):
            if debug:
                print(str(dictionary))
                # print('pattern_ind: %d, len(pattern)-1: %d' % (pattern_ind, len(pattern)-1))
                # print('inner_pattern_ind: %d, len(...): %d' % (inner_pattern_ind, len(dictionary[pattern[pattern_ind]])))
            check = ''
            for letter in pattern:
                check += dictionary[letter].pattern
            if phrase == check:
                sent = ''
                for letter in pattern:
                    sent += dictionary[letter].pattern + ' '
                print(sent)
            return phrase == check
        else:
            return False
    if pattern_ind == len(pattern):
        return False

    # assume current letter starts new pattern member. finish this one and start a new one.
    if pattern[pattern_ind] not in dictionary:
        dictionary[pattern[pattern_ind]] = PatternEntry('')

    new = False
    current = False
    next = False

    # assume current letter is in current pattern member
    if dictionary[pattern[pattern_ind]].is_building():
        # recursive call--start a new pattern
        dictionary[pattern[pattern_ind]].finish_build()
        new = find_pattern(pattern, phrase, dictionary, pattern_ind + 1, phrase_ind, 0)
        dictionary[pattern[pattern_ind]].open_build()
        # extending an existing pattern
        dictionary[pattern[pattern_ind]].add_to_pattern(phrase[phrase_ind])
        current = find_pattern(pattern, phrase, dictionary, pattern_ind, phrase_ind + 1, inner_pattern_ind + 1)
    elif dictionary[pattern[pattern_ind]].compare(phrase[phrase_ind], inner_pattern_ind):
        # check for current pattern passed; go to next letter in phrase.
        current = find_pattern(pattern, phrase, dictionary, pattern_ind, phrase_ind + 1, inner_pattern_ind + 1)
        if debug:
            print('dict[...]: %s' % dictionary[pattern[pattern_ind]])
            print('inner_pattern_ind: %d, len(...): %d' % (inner_pattern_ind, len(dictionary[pattern[pattern_ind]])))
        if inner_pattern_ind == len(dictionary[pattern[pattern_ind]]) - 1:
            next = find_pattern(pattern, phrase, dictionary, pattern_ind + 1, phrase_ind + 1, 0)

    return new or next or current


if __name__ == '__main__':
    main()