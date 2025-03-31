#!/usr/bin/python3
import argparse

__author__ = 'sco-sec'

# Argument parser setup
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=r'''\
  ____  _ _        _     
 |  _ \(_) |_ _ __(_)___ 
 | | | | | __| '__| / __|
 | |_| | | |_| |  | \__ \
 |____/|_|\__|_|  |_|___/

Distort - A wordlist distortion tool by sco-sec.
'''
)
parser.add_argument('word', metavar='word', nargs='?', help='word to distort')
parser.add_argument('-l', '--level', type=int, default=5, help='distortion level [0-9] (default 5)')
parser.add_argument('-i', '--input', help='input file')
parser.add_argument('-o', '--output', help='output file')
args = parser.parse_args()

# Validate level argument
args.level = max(0, min(args.level, 9))

# Helper function for leet transformations
def leet_transform(word, patterns):
    for pattern in patterns:
        yield ''.join(pattern.get(char, char) for char in word)

# Define transformation patterns for various levels
leet_patterns = [
    {},
    {'e': '3', 'a': '4', 'o': '0', 'i': '1', 'l': '1', 's': '$'},
    {'e': '3', 'a': '@', 'o': '0', 'i': '1', 'l': '1', 's': '$'},
    {'e': '3', 'a': '4', 'o': '0', 'i': '!', 'l': '1', 's': '$'},
    {'e': '3', 'a': '@', 'o': '0', 'i': '!', 'l': '1', 's': '$'},
    {'e': '3', 'a': '4', 'o': '0', 'i': '1', 'l': '1', 's': '5'},
    {'e': '3', 'a': '@', 'o': '0', 'i': '1', 'l': '1', 's': '5'},
    {'e': '3', 'a': '4', 'o': '0', 'i': '!', 'l': '1', 's': '5'},
    {'e': '3', 'a': '@', 'o': '0', 'i': '!', 'l': '1', 's': '5'},
]

# Generate capitalization variants
def capitalize_variants(word):
    return {word, word.upper(), word.capitalize(), word.lower()}

# Generate transformations based on level
def distort(word, level):
    transformations = set()
    for variant in capitalize_variants(word):
        transformations.add(variant)
        if level > 4:
            transformations |= set(leet_transform(variant, leet_patterns[:level - 4]))
    return transformations

# Apply transformations and append suffixes
def distort_with_suffixes(word, level):
    suffixes = []
    if level > 4:
        suffixes.extend(['1', '123', '!', '.', '2'])
    if level > 6:
        suffixes.extend(['?', '_', '69', '23', '25', '8', '10', '13', '3', '4', '6', '7'])
    if level > 7:
        suffixes.extend(['07', '09', '14', '15', '17', '18', '19', '77', '88', '99', '12345'])
    if level > 8:
        suffixes.extend(['00', '02', '06', '19', '20', '25', '007', '111', '777', '666', '2024'])

    distorted_words = distort(word, level)
    for suffix in suffixes:
        for variant in capitalize_variants(word):
            distorted_words |= distort(variant + suffix, level)
    return distorted_words

# Generate distorted words from input
def generate_wordlist(word_list, level):
    result = set()
    for word in word_list:
        word = word.strip().lower()
        result |= distort_with_suffixes(word, level)
    return result

# Main logic for handling input/output
def main():
    word_list = []
    if args.word:
        word_list.append(args.word)
    elif args.input:
        try:
            with open(args.input) as f:
                word_list = f.readlines()
        except IOError:
            print(f"Exiting\nCould not read file: {args.input}")
            return
    else:
        print("Nothing to do!!\nTry -h for help.\n")
        return

    wordlist = generate_wordlist(word_list, args.level)
    
    if args.output:
        try:
            with open(args.output, 'w') as f:
                f.write('\n'.join(wordlist) + '\n')
            print(f"Written to: {args.output}")
        except IOError:
            print(f"Exiting\nCould not write file: {args.output}")
    else:
        for word in wordlist:
            print(word)

if __name__ == "__main__":
    main()
