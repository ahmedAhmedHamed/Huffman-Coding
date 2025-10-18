#!/usr/bin/python3
from __future__ import annotations
from functools import total_ordering
from typing import List, Optional
import copy


def get_first_line_from_file(filepath: str) -> str:
    ret: str = ''
    with open('./input.txt') as input_file_content:
        ret = input_file_content.readline()
    return ret


@total_ordering  # auto implement bigger than etc etc given less than.
class FrequencyCountNode:
    count: int
    character: Optional[str]
    leftChild: Optional[FrequencyCountNode]  = None
    rightChild: Optional[FrequencyCountNode]  = None
    def __init__(self, character = None) -> None:
        self.count = 1
        self.character = character
    
    def __eq__(self, other):
        return self.count == other.count
    
    def __lt__(self, other):
        return self.count < other.count
    
    def __str__(self):
        if self.character:
            return f'({self.count}, {self.character})'
        else:
            return f'{str(self.leftChild)}, {str(self.rightChild)}'
    

    def __repr__(self):
        return str(self)


def construct_sorted_frequencies(string_to_be_counted_from: str) -> List[FrequencyCountNode]:
    counts: List[FrequencyCountNode] = []
    # sort the input string so that I can just add all the characters that are alike at a time.
    # could also use a dict for this, but I prefer this way.
    for character in sorted(string_to_be_counted_from):
        if len(counts) != 0 and counts[-1].character == character:
            counts[-1].count += 1
        else:
            counts.append(FrequencyCountNode(character))
    return sorted(counts, reverse=True)


def construct_new_level_in_huffman_tree(current_level: List[FrequencyCountNode]) -> List[FrequencyCountNode]:
    
    new_level = copy.deepcopy(current_level)
    smallest_frequency = new_level[-1]
    second_smallest = new_level[-2]
    new_node = FrequencyCountNode()
    new_node.leftChild = smallest_frequency
    new_node.rightChild = second_smallest
    new_level.pop()
    new_level.pop()
    new_level.append(new_node)
    return sorted(new_level)


def construct_huffman_tree(sorted_frequencies: List[FrequencyCountNode]) -> FrequencyCountNode:
    new_level = construct_new_level_in_huffman_tree(sorted_frequencies)
    while len(new_level) > 1:
        new_level = construct_new_level_in_huffman_tree(new_level)
    return new_level[0]


if __name__ == '__main__':
    input_string = get_first_line_from_file('./input.txt')
    sorted_frequencies = construct_sorted_frequencies(input_string)
    root_huffman_node = construct_huffman_tree(sorted_frequencies)
    print(input_string)
    print(sorted_frequencies)
    print(root_huffman_node)

