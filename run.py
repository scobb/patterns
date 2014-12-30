from copy import deepcopy

__author__ = 'scobb'
from pattern import PatternEntry


def main():
    in_file = 'sample.in'
    f = open(in_file)
    pattern = f.readline().strip()
    print('pattern: %s' % pattern)
    phrase = f.readline().strip()
    print('phrase: %s' % phrase)
    f.close()

    val = find_pattern(pattern, phrase, {}, 0, 0, 0)
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
    if phrase_ind == len(phrase):
        if pattern_ind == len(pattern) - 1 and inner_pattern_ind == len(dictionary[pattern[pattern_ind]]):

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

    building = dictionary[pattern[pattern_ind]].is_building()
    dictionary[pattern[pattern_ind]].finish_build()

    next = find_pattern(pattern, phrase, dictionary, pattern_ind + 1, phrase_ind, 0)

    if building:
        dictionary[pattern[pattern_ind]].open_build()

    # assume current letter is in current pattern member
    if dictionary[pattern[pattern_ind]].is_building():
        # extending an existing pattern
        dictionary[pattern[pattern_ind]].add_to_pattern(phrase[phrase_ind])
    else:
        # checking against an existing pattern
        if not dictionary[pattern[pattern_ind]].compare(phrase[phrase_ind], inner_pattern_ind):
            return next
        inner_pattern_ind += 1

    # check go to next letter
    current = find_pattern(pattern, phrase, dictionary, pattern_ind, phrase_ind + 1, inner_pattern_ind)
    return next or current


if __name__ == '__main__':
    main()