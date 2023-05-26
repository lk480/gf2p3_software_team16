import sys
import os
from names import Names
from scanner import Scanner


def open_file(path):
    f = open(path, "r")
    return f


def get_next_character(input_file):
    char = input_file.read(1)
    return char


def get_next_non_whitespace_character(input_file):
    char = input_file.read(1)
    if not char.isspace():
        return char


def get_next_number(input_file):
    next_number = ''
    while True:
        next_char = get_next_character(input_file)
        if next_char.isdigit():
            next_number += next_char
        elif not next_char.isdigit():
            break
    if next_number == '':
        return [None, next_char]
    else:
        return [int(next_number), next_char]


def get_next_name(input_file):
    next_word = ''
    while True:
        next_char = get_next_character(input_file)
        if next_char.isalnum():
            next_word += next_char
        elif not next_char.isalnum():
            break
    if next_word == '':
        return [None, next_char]
    elif next_word.isdigit():
        return [None, next_char]
    else:
        return [next_word, next_char]


def main():
    # Check command line arguments
    arguments = sys.argv[1:]
    if len(arguments) != 1:
        print("Error! One command line argument is required.")
        sys.exit()

    else:

        print("\nNow opening file...")
        # Print the path provided and try to open the file for reading
        path = os.path.abspath(sys.argv[1])
        print(path)
        print("\nNow reading file...")
        names = Names()
        scanner = Scanner(path, names)
        while True:
            next_char = scanner.advance()
            if not next_char.isalnum():
                break


if __name__ == "__main__":
    main()
