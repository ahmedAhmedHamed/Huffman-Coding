#!/usr/bin/python3
from functools import total_ordering
from typing import List
def get_first_line_from_file(filepath: str) -> str:
    ret: str = ''
    with open('./input.txt') as input_file_content:
        ret = input_file_content.readline()
    return ret

@total_ordering  # auto implement bigger than etc etc given less than.
class FrequencyCount:
    count: int
    character: str
    def __init__(self, character) -> None:
        self.count = 1
        self.character = character
    
    def __eq__(self, other):
        return self.count == other.count
    
    def __lt__(self, other):
        return self.count < other.count
    
    def __str__(self):
        return f'({self.count}, {self.character})'
    
    def __repr__(self):
        return str(self)
    


def construct_sorted_frequencies(string_to_be_counted_from: str) -> List[FrequencyCount]:
    counts: List[FrequencyCount] = []
    # sort the input string so that I can just add all the characters that are alike at a time.
    # could also use a dict for this, but I prefer this way.
    for character in sorted(string_to_be_counted_from):
        if len(counts) != 0 and counts[-1].character == character:
            counts[-1].count += 1
        else:
            counts.append(FrequencyCount(character))
    return sorted(counts, reverse=True)


if __name__ == '__main__':
    input_string = get_first_line_from_file('./input.txt')
    sorted_frequencies = construct_sorted_frequencies(input_string)
    print(input_string)
    print(sorted_frequencies)

