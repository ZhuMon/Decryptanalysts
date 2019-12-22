import operator
import enchant
import numpy as np
import itertools
import sys
import time
import threading
from functools import partial

en_dict = enchant.Dict("en_US")
is_word_thr = 3 # len(char)/is_word_thr is correct


def freq(cipher_text):
    f = {}
    for line in cipher_text:
        for char in line:
            if char not in f.keys():
                f[char] = 1
            else:
                f[char] += 1

    return sorted(f.items(), key = lambda d:d[1])

def check_syntax_by_thread(text, word_len, correct_count):
    for begin_char in range(2, len(text)-word_len):
        word = text[begin_char:begin_char+word_len]
        if en_dict[word_len-3].check(word) and len(word) > 1:
            correct_count[word_len-3] += 1

def check_syntax(text, is_word_thr=3):
    correct_count = 0

    threads = []
    for word_len in range(3, 10):
        # t = threading.Thread(target = check_syntax_by_thread, args=(text, word_len,correct_count))
        # t.start()
        # threads.append(t)
        for begin_char in range(2, len(text)-word_len):
            word = text[begin_char:begin_char+word_len]
            if en_dict.check(word) and len(word) > 1:
                correct_count += 1
    
    #alive_array = [t.isAlive() for t in threads]
    #while True in alive_array:
    #    alive_array = [t.isAlive() for t in threads]

    if correct_count > len(text)/is_word_thr:
        return True
    else:
        return False

def caesar(cipher_text):
    max_char = max(freq(cipher_text).items(), key=operator.itemgetter(1))[0]
    
#     if key == None:
#         key = (ord('e')-ord(max_char))%26

    line = cipher_text[0]
    for key in range(1,26):
        new_line = ""
        for char in line:
            new_line += chr((ord(char) + key - 97)%26 + 97)
                
        if check_syntax(new_line):
            return True

    return False

def playfair(cipher_text):
    key = ""

    def gen_matrix(key):
        tmp = ""
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        m = []
        for k in key:
            if k not in tmp:
                if (k == "i" and "j" in tmp) or (k == "j" and "i" in tmp):
                    alphabet = alphabet.replace(k,'')
                    continue
                tmp += k
                alphabet = alphabet.replace(k, '')

        if 'i' in alphabet and 'j' in alphabet:
            alphabet = alphabet.replace('j', '')
        tmp += alphabet

        for row in range(0,5):
            m_tmp = []
            for col in range(0, 5):
                m_tmp.append(tmp[row*5+col])
            m.append(m_tmp)

        return m
    
    def lookup_matrix(text, m):
        """
        Args:
            text (str): ex: 'ab'
            m (list[list[char]]): 5x5

        Return:
            str: ex: 'cd'
        """
        
        a = text[0]
        b = text[1]
        row1 = col1 = row2 = col2 = -1
        for row in range(5):
            for col in range(5):
                if m[row][col] == a or (a in ['i','j'] and m[row][col] in ['i','j']):
                    row1, col1 = row, col
                if m[row][col] == b or (b in ['i','j'] and m[row][col] in ['i','j']):
                    row2, col2 = row, col
        
        if -1 in [row1, col1, row2, col2]:
            print("cannot find text in matrix")
            return
        elif row1 == row2:
            col1 -= 1
            col2 -= 1
        elif col1 == col2:
            row1 -= 1
            row2 -= 1
        else:
            tmp = col1
            col1 = col2
            col2 = tmp

        return m[row1][col1]+m[row2][col2]

    def decrypt(text, matrix):
        ## split text
        s_text = []
        for i in range(0, len(text), 2):
            s_text.append(text[i:i+2])

        plaintext = ""
        for s in s_text:
            plaintext += lookup_matrix(s, matrix)
        return plaintext

    key = "monarchy"
    matrix = gen_matrix(key)

    for line in cipher_text:
        plaintext = decrypt(line, matrix)
        if check_syntax(plaintext):
            return True

    return False

def hill(cipher_text):
    pass

def map_known_mapping(cipher_text):
    plain_key = "abcdefghijklmnopqrstuvwxyz"
    cipher_key = "ahovcjqxelszgnubipwdkryfmt"
    # cipher_key = "arizqhypgxofwnevmdulctkbsj"

    ## mapping[cipher] = plaintext
    ## generate mapping
    mapping = {}
    for cipher_char, plain_char in zip(cipher_key, plain_key):
        mapping[cipher_char] = plain_char
    
    
    def decode(text, mapping):
        plaintext = ""
        for char in text:
            plaintext += mapping[char]

        return plaintext

    plaintexts = []
    for ci in cipher_text:
        plaintext = decode(ci, mapping)
        plaintexts.append(plaintext.replace('\n',''))
    
    
    return plaintexts



def advanced_brute_force(cipher_text):
    frequency = freq(cipher_text)
    e_map = max(freq(cipher_text), key= lambda d: d[1])[0]

    ## concat to one string
    one_string = ""
    for line in cipher_text:
        one_string += line

    ## find the most word in 2 char
    two_char_freq = {}
    for i in range(1,len(one_string)-1):
        two_char = one_string[i:i+2]
        if two_char not in two_char_freq.keys():
            two_char_freq[two_char] = 1
        else:
            two_char_freq[two_char] += 1

    tmp_two_char_freq = dict(two_char_freq)
    for key,value in two_char_freq.items():
        if value < 100:
            tmp_two_char_freq.pop(key)

    tmp_two_char_freq = sorted(tmp_two_char_freq.items(), key = lambda d:d[1])
    th_map = max(two_char_freq.items(), key=operator.itemgetter(1))[0]
    t_map = th_map[0]
    h_map = th_map[1]

    ## find 'a' mapping
    frequency.reverse()
    a_map = ""
    for char in frequency:
        if char[0] in [e_map, t_map, h_map]:
            continue
        else:
            a_map = char[0]
            break

    ## find first group and second group
    i = 0
    first_group_map = ""
    second_group_map = ""
    for f in frequency:
        if f[0] in [a_map, e_map, t_map, h_map]:
            continue
        else:
            if i < 7:
                first_group_map += f[0]
            else:
                second_group_map += f[0]
            i += 1

    ## mapping[cipher] = plaintext
    ## plaintext: a, ciphertext: a_map
    #  O, I, N, S, R, D, L : first group
    #  C, U, M, W, F, G, Y, P, B, V, K, J, X, Q, Z: second group

    mapping = {a_map:'a', e_map:'e', h_map:'h', t_map:'t'}

    ## generate mapping
    
    def decode(text, mapping):
        plaintext = ""
        for char in text:
            plaintext += mapping[char]

        return plaintext

    remain_map_key = first_group_map + second_group_map
    second_group_plaintext = tuple("cumwfgypbvkjxqz")
    
    tmp_mapping = {}
    for f_p in itertools.permutations("oinsrdl",7):
        ## compute mapping
        for cipher_char, plain_char in zip(remain_map_key, f_p+second_group_plaintext):
            tmp_mapping[cipher_char] = plain_char

        
        plaintext = decode(cipher_text[0], dict(mapping, **tmp_mapping))

        
        if check_syntax(plaintext, 3):
            print(str(f_p))
            print(plaintext)
        

    """
        for s_p in itertools.permutations("cumwfgypbvkjxqz",15):
            ## compute mapping
            for cipher_char, plain_char in zip(remain_map_key, f_p+s_p):
                mapping[cipher_char] = plain_char
        
            plaintext = decode(cipher_text[0], mapping)

            ### checking
            if check_syntax(plaintext):
                print(plaintext)
                print(mapping)

            print(len(cipher_text[0]))
            print([char for char in cipher_text[0] if char in second_group_map])
            sys.exit(1)
    """

if __name__ == "__main__":
    cipher = "creditriskevaluationisgettingimportantsincetheglob"
    print(len(cipher))
    if check_syntax(cipher,3):
        print("yes")
