#!/usr/bin/python3

input_string: str = ''
with open('./input.txt') as input_file_content:
    input_string = input_file_content.readline()
print(input_string)

