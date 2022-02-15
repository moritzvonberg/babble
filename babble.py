import re
from collections import Counter
from typing import Counter


#TODO read hand and only suggest words containing letters in hand
wordlist = None

with open('source.txt') as infile:
    wordlist = [x.rstrip('\n') for x in infile]

wordlist = sorted(wordlist, key=lambda word: len(word))

length_sets = dict()

for i in range(2,12):
    length_sets[i] = set((word for word in wordlist if len(word) == i))

wordset = set(wordlist)


def is_anagram(tiles: str, word: str) -> bool:
    return sorted(tiles) == sorted(word)
    

def simple_search(search_str:str, hand_tiles: str=None, count=50) -> list[str]:
    if hand_tiles:
        pattern = string_input_generate_regex(search_str, hand_pattern=str(set(hand_tiles)))
    else:
        pattern = string_input_generate_regex(search_str)
    # search_segments = re.split('\[[a-z]\]', search_str)
    match_gen = (word for word in wordlist if pattern.search(word))
    results = []
    try:
        while(len(results) < count):
            #TODO: check if played characters exceed hand count and continue if so
            word = next(match_gen)
            
            results.append(word)
    except StopIteration:
        return results
    return results


def tuple_input_generate_regex(search_positions:list[tuple[str, int]], hand_pattern: str='[a-z]') -> re.Pattern:
    """Generates a regex matching words corresponding to input pattern.
    input pattern is a list tuples with set characters and their position
    relative to the first set character"""
    #TODO deal with adjacent characters restricting selecter letters outside of word range
    #TODO replace wildcard select of all letter with set of letters in hand
    #TODO add optional limits of amount of characters to left or right of first last char in pattern for game board edges

    regex_pattern_parts = []
    last_pos = 0
    for chars, pos in search_positions:
        if pos - last_pos > 1:
            letters_between = pos - last_pos - 1
            to_add = hand_pattern
            
            if letters_between > 1:
                to_add += f"{{{letters_between}}}"
            
            regex_pattern_parts.append(to_add)
        if len(chars) == 1:
            regex_pattern_parts.append(chars)
        else:
            regex_pattern_parts.append(f"[{chars}]")
        last_pos = pos
    
    return re.compile(''.join(regex_pattern_parts))


def string_input_generate_regex(pattern: str, hand_pattern='[a-z]') -> re.Pattern:
    result = []
    segments = re.split('(\[[^\]]+])', pattern)
    for segment in segments:
        if segment.startswith('['):
            result.append(segment)
        else:
            for char in segment:
                if char.isnumeric():
                    result.append(hand_pattern + f'{{{char}}}')
                elif char.isalpha():
                    result.append(char.lower())
                else:
                    result.append(hand_pattern)
    return re.compile(''.join(result))

def convert_string_pattern_to_tuple(pattern: str) -> list[tuple[str, int]]:
    """utility function to create patterns for simple test cases"""
    result = []
    for pos, char in enumerate(pattern):
        if char.isalpha():
            result.append((char.lower(), pos))
    return result

# print(simple_search('e[la]'))
# print(simple_search('x.[la][el]a[yxt]e'))

# def search_intersect_simple(start_letter: str, end_letter: str, letters_between: int) -> str:
#     """Search for a string in wordlist joining the two letters with the specified
#     offset of letters in between.
    
#     Example: list_intersect_simple('n', 'r', 2) represents searching for words matching N _ _ R  

#     """
#     if letters_between < 0:
#         raise ValueError("offset must be greater than 0")
    
#     result = None
#     for word_length in range(letters_between + 2,12):
        
#         for scan_offset in range(word_length - (letters_between + 1)):
#             for word in length_sets[word_length]:
#                 if word[scan_offset] == start_letter and word[scan_offset + letters_between + 1] == end_letter:
#                     return word
    
#     return ''