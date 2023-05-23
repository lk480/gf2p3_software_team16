import sys
import os
from names import Names


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
        try:
            file = open_file(path)
        except IOError:
            print("Cannot find file or read data")
            sys.exit()
        else:
            print("Contents read successfully")

        print("\nNow reading file...")

        while True:
            char = get_next_character(file)
            if not char:
                char = ""
                break
            print(char, end="")

        print("\nNow skipping spaces...")
        # Print out all the characters in the file, without spaces
        file.seek(0)
        while True:
            char = get_next_non_whitespace_character(file)
            if char == '':
                break
            elif char is None:
                char = ""
            print(char, end="")

        print("\nNow reading numbers...")
        # Print out all the numbers in the file
        file.seek(0)
        while True:
            char_list = get_next_number(file)
            next_num = char_list[0]
            if next_num is None:
                pass
            else:
                print(next_num)
            if char_list[1] == '':
                break

        print("\nNow reading names...")
        file.seek(0)
        while True:
            char_list = get_next_name(file)
            next_name = char_list[0]
            if next_name is None:
                pass
            else:
                print(next_name)
            if char_list[1] == '':
                break

        print("\n testing names class")
        # Print out only the good names in the file
        names = Names()
        names_ids = names.lookup(['happy', 'sad'])
        print(names_ids)


if __name__ == "__main__":
    main()
