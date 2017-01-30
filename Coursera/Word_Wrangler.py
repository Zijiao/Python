"""
Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    answer_list = []
    for elem in list1:
        if elem not in answer_list:
            answer_list.append(elem)
    return answer_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    answer_list = []
    for elem in list1:
        if elem in list2:
            answer_list.append(elem)
    return answer_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """   
    answer_list = []
    index1 = 0
    index2 = 0
    list1_copy = list(list1)
    list2_copy = list(list2)
    while (len(list1_copy) != 0) and (len(list2_copy) != 0):
        if(list1[index1] <= list2[index2]):
            answer_list.append(list1[index1])
            list1_copy.remove(list1[index1])
            index1 += 1
        else:
            answer_list.append(list2[index2])
            list2_copy.remove(list2[index2])
            index2 += 1
    if list1_copy:
        for elem in list1_copy:
            answer_list.append(elem)
    else:
        for elem in list2_copy:
            answer_list.append(elem)
    return answer_list
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    else:
        list1_length = len(list1)
        return merge(merge_sort(list1[:list1_length/2]), merge_sort(list1[list1_length/2:]))
    
    
# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if word == '':
        return ['']
    elif len(word) == 1 :
        return [''] + list(word) 
    else:
        first = word[0]
        rest = word[1:]
        rest_strings = gen_all_strings(rest)
        inserted_strings = []
        for elem in rest_strings:
            for position in range(len(elem) + 1):
                inserted_strings.append(insert_char(position, first, elem))
        return list(rest_strings) + list(inserted_strings)

# My help function used in gen_all_strings()

def insert_char(position, char, string):
    """
    insert "char" into "string" at "position"
    """
    return string[:position] + char + string[position:]


# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    return []

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# run()

