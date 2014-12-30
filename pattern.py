__author__ = 'scobb'


class PatternEntry(object):

    def __init__(self, pattern):
        self.building = True
        self.pattern = pattern

    def __str__(self):
        return self.pattern

    def __repr__(self):
        return self.pattern

    def __eq__(self, other):
        return self.pattern == other.pattern

    def __len__(self):
        return len(self.pattern)

    def finish_build(self):
        self.building = False

    def open_build(self):
        self.building = True

    def is_building(self):
        return self.building

    def compare(self, letter, index):
        if index >= len(self.pattern):
            return False
        return self.pattern[index] == letter

    def add_to_pattern(self, letter):
        if not self.building:
            raise RuntimeError('Attempting to continue building phrase after build is finished.')
        self.pattern += letter