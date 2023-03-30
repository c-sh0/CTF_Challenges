#!/usr/bin/env python3
#
# https://hack.ainfosec.com/retired-challenges/
# Solution for: 300pts: [Super ROT]
# - c-sh0
#
import sys
import string
import re
import json
import requests
from urllib.parse import urlparse

# Grab these values from the browser/DevTools
#
get_url             = 'https://hack.ainfosec.com/challenge/get-challenge/super_rot/'
post_url            = 'https://hack.ainfosec.com/challenge/submit-answer/'
session_cookie      = {"Cookie": "csrftoken=; sessionid="}
csrfmiddlewaretoken = ''

#
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

def startChallenge():
    print(f"[*]: Connecting to: {get_url}")
    session = requests.Session()
    session.headers.update(session_cookie)

    try:
        #r = session.get(get_url, headers=session.headers, verify=False)
        r = session.get(get_url, headers=session.headers)
        if r.status_code != 200:
           print(f"[X]: Connection failed, got {r.status_code} response!")
           return sys.exit(-1)

    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    encoded_str = r.json()['hc_challenge']['encrypted_message']

    return encoded_str

def postAnswer(answer_str):
    #answer_url = post_url + 'csrfmiddlewaretoken=' + csrfmiddlewaretoken + '&challenge_id=super_rot&answer=' + answer_str
    post_data = 'csrfmiddlewaretoken=' + csrfmiddlewaretoken + '&challenge_id=super_rot&answer=' + answer_str

    print(f"[*]: Submitting answer to : {post_url}")

    session = requests.Session()
    session.headers.update(session_cookie)

    ctype_header = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    session.headers.update(ctype_header)

    try:
        #r = session.get(post_url, headers=session.headers, verify=False)
        r = session.post(post_url, data=post_data, headers=session.headers)
        if r.status_code != 200:
           print(f"[X]: Failed, got {r.status_code} response!")
           return sys.exit(-1)

    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    next_str = r.json()['hc_challenge']['encrypted_message']

    return next_str

def main():
     # store decoded string in an array (max 100 words)
     str_found = [None] * 100

     # List of words
     # http://www.gwicks.net/dictionaries.htm
     word_list = './english3.txt'

     # English word list
     with open(word_list) as word_file:
          english_words = set(word.strip().lower() for word in word_file)

     # Start the challange, Fisrt encoded string
     str = startChallenge()

     # Need to solve a total of 50 in under 180 seconds
     for solve_x in range(1, 50):
         #print(f"{solve_x}: {str}")

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
         print(f"{solve_x} {str_found[idx]}")
         str = postAnswer(str_found[idx])
         print("")

if __name__ == "__main__":
        main()

