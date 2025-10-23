#!/usr/bin/python3
from __future__ import annotations
from functools import total_ordering
from typing import List, Optional
from math import ceil
import copy
import json


def get_first_line_from_file(filepath: str) -> str:
    ret: str = ''
    with open(filepath) as input_file_content:
        ret = input_file_content.readline()
    return ret


@total_ordering  # auto implement bigger than etc etc given less than.
class FrequencyCountNode:
    count: int
    character: Optional[str]
    leftChild: Optional[FrequencyCountNode] = None
    rightChild: Optional[FrequencyCountNode] = None

    def __init__(self, character=None) -> None:
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
    new_node.count = new_node.leftChild.count + new_node.rightChild.count
    new_level.pop()
    new_level.pop()
    new_level.append(new_node)
    return sorted(new_level, reverse=True)


def construct_huffman_tree(sorted_frequencies: List[FrequencyCountNode]) -> FrequencyCountNode:
    new_level = construct_new_level_in_huffman_tree(sorted_frequencies)
    while len(new_level) > 1:
        new_level = construct_new_level_in_huffman_tree(new_level)
    return new_level[0]


def get_character_encodings_through_tree(huffman_root_node: FrequencyCountNode) -> tuple(dict[str, str], dict[str, str]):
    char_to_code = {}
    code_to_char = {}

    def dfs(current_prefix: str, current_node: FrequencyCountNode):
        if current_node is None:
            return
        # having a character means you are a leaf node.
        if current_node.character:
            
            code_to_char[current_prefix] = current_node.character
            char_to_code[current_node.character] = current_prefix
        else:
            dfs(current_prefix + '1', current_node.leftChild)
            dfs(current_prefix + '0', current_node.rightChild)
    dfs('', huffman_root_node)
    return char_to_code, code_to_char


def get_huffman_character_encoding(string_to_get_encoding_from: str):
    sorted_frequencies = construct_sorted_frequencies(string_to_get_encoding_from)
    root_huffman_node = construct_huffman_tree(sorted_frequencies)
    charToCode, codeToChar = get_character_encodings_through_tree(root_huffman_node)
    return charToCode, codeToChar


def encode_string(string_to_encode: str, character_mapping: dict[str, str]) -> str:
    ret = ''
    for character in string_to_encode:
        ret += character_mapping[character]
    return ret


def decode_string(string_to_decode: str, character_mapping: dict[str, str]) -> str:
    ret = ''
    current_chunk = ''
    for character in string_to_decode:
        current_chunk += character
        if character_mapping.get(current_chunk):
            ret += character_mapping.get(current_chunk)
            current_chunk = ''
    return ret


if __name__ == '__main__':
    input_path = "input.txt"
    bin_path = "output.bin"
    dictionary_path = "overhead.json"
    decompressed_path = "decompressed.txt"


    # 1. Read text
    input_string = get_first_line_from_file(input_path)

    # 2. Build Huffman dictionary
    charToCode, codeToChar = get_huffman_character_encoding(input_string)
    
    # 3. Encode
    encoded_string = encode_string(input_string, charToCode)

    number_of_bits = len(encoded_string)
    

    # 4. Pad bits to byte length
    padding = (8 - (len(encoded_string) % 8)) % 8 # number of extra bits added the begining
    padded_bitstring = encoded_string + ("0" * padding)
    number_of_bytes = len(padded_bitstring) // 8
    bytes_data = int(padded_bitstring, 2).to_bytes(number_of_bytes, byteorder='big')
    # convert string form of 0's and 1's to binary bytes
    binary_encoded_message = int(encoded_string, 2).to_bytes(number_of_bytes, byteorder='big')



    # 5. Write compressed binary bytes to the .bin file
    with open(bin_path, 'wb') as f:
        f.write(bytes([padding])) # 1 byte to rememeber padding count
        f.write(bytes_data)
    print(f"Compressed file written to {bin_path}")
    
    # 6. Save overhead dictionary (char→code)
    with open(dictionary_path, "w", encoding="utf-8") as f:
        json.dump(charToCode, f, ensure_ascii=False, indent=2)
    print(f"Huffman dictionary written to {dictionary_path}")
    
    
    # ========== Decompression test ==========


    # Load the Huffman dictionary from overhead.json
    with open("overhead.json", "r") as f:
        loaded_charToCode = json.load(f)

    # Load overhead dictionary
    with open(dictionary_path, "r", encoding="utf-8") as f:
        loaded_codeToChar = {v: k for k, v in loaded_charToCode.items()} #####  WHAT IS THAT
    
    

    # Read binary
    with open(bin_path, "rb") as f:
        padding = int.from_bytes(f.read(1), 'big') # read the 1 byte first
        data = f.read()
    bitstring = ''.join(format(byte, '08b') for byte in data)
    if padding:
        bitstring = bitstring[:-padding]


    # Decode
    decoded_text = decode_string(bitstring, loaded_codeToChar)
    print(f"Decompressed text: {decoded_text}")


    # Save decompressed output
    with open(decompressed_path, "w", encoding="utf-8") as f:
        f.write(decoded_text)

    
    # Verify
    assert input_string == decoded_text, " XXXXX     Decompressed text does not match original!"
    print("-------    Huffman compression & decompression successful.")

   

    """

print(character_encoding)
    print(f'size before encoding: {len(input_string) * 4}')
    print(f'size after encoding: {len(encoded_string)}')
    print(encoded_string)
    print(decoded_string)

     """
    
