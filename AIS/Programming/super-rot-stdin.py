#!/usr/bin/env python3
#
# - c-sh0
#
import string
import re

# https://stackoverflow.com/questions/3269686/short-rot13-function-python
def rot(s, n=13):
    '''Encode string s with ROT-n, i.e., by shifting all letters n positions.
    When n is not supplied, ROT-13 encoding is assumed.
    '''
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    upper_start = ord(upper[0])
    lower_start = ord(lower[0])
    out = ''
    for letter in s:
        if letter in upper:
            out += chr(upper_start + (ord(letter) - upper_start + n) % 26)
        elif letter in lower:
            out += chr(lower_start + (ord(letter) - lower_start + n) % 26)
        else:
            out += letter
    return(out)

def main():
     # store decoded string in an array (max 100 words)
     str_found = [None] * 100

     # List of words
     # http://www.gwicks.net/dictionaries.htm
     word_list = './english3.txt'

     # English word list
     with open(word_list) as word_file:
          english_words = set(word.strip().lower() for word in word_file)

     while True:
         # Read input from stdin
         str = input("encoded> ")

         # index based on word count
         idx = 1

         # Decode string (all ROT(X) variants)
         for i in range(1, 26):
             decoded_str  = rot(str, -i)
             str_array    = decoded_str.split()
             #print(str_array)

             # Loop through each decoded word
             wrd_cnt = 0
             for word in str_array:
                 test_word = re.sub(r'[^\w\s]', '', word) # strip punctuation

                 # test the word against a dictionary of words, count words found
                 if(test_word.lower() in english_words):
                    wrd_cnt += 1

             # save to array (index based on word count)
             str_found[wrd_cnt] = decoded_str

             # Track the position/index of the most words found
             if(wrd_cnt > idx):
                idx = wrd_cnt

         # Most likely
         print(str_found[idx])
         print("")

if __name__ == "__main__":
        main()

