import operator
import enchant
import numpy as np
import itertools

en_dict = enchant.Dict("en_US")
is_word_thr = 5 # len(char)/2 is correct


def freq(cypher_text):
    f = {}
    for line in cypher_text:
        for char in line:
            if char not in f.keys():
                f[char] = 1
            else:
                f[char] += 1

    return sorted(f.items(), key = lambda d:d[1])

def check_syntax(text):
    correct_count = 0

    for word_len in range(3, 10):
        for begin_char in range(2, len(text)-word_len):
            word = text[begin_char:begin_char+word_len]
            if en_dict.check(word) and len(word) > 1:
                correct_count += 1

    if correct_count > len(text)/is_word_thr:
        return True
    else:
        return False

def caesar(cypher_text):
    max_char = max(freq(cypher_text).items(), key=operator.itemgetter(1))[0]
    
#     if key == None:
#         key = (ord('e')-ord(max_char))%26

    line = cypher_text[0]
    for key in range(1,26):
        new_line = ""
        for char in line:
            new_line += chr((ord(char) + key - 97)%26 + 97)
                
        if check_syntax(new_line):
            return True

    return False

def playfair(cypher_text):
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

    for line in cypher_text:
        plaintext = decrypt(line, matrix)
        if check_syntax(plaintext):
            return True

    return False

def hill(cypher_text):
    pass

def brute_force(cypher_text):
    frequency = freq(cypher_text)
    print(frequency)
    e_map = max(freq(cypher_text), key= lambda d: d[1])[0]

    ## find the most word in 2 char
    ### concat to one string
    one_string = ""
    for line in cypher_text:
        one_string += line

    ### find
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
    print(tmp_two_char_freq)
    th_map = max(two_char_freq.items(), key=operator.itemgetter(1))[0]
    t_map = th_map[0]
    h_map = th_map[1]

    ## find a mapping
    frequency.reverse()
    a_map = ""
    for char in frequency:
        if char[0] in [e_map, t_map, h_map]:
            continue
        else:
            a_map = char[0]
            break
    
    print(a_map)
    ## mapping[cypher] = plaintext
    ## plaintext: a, cyphertext: a_map
    """
    mapping = {a_map:'a', e_map:'e', h_map:'h', t_map:'t',
            'd':'r', 'n':'n', 'g':'i', 'u':'s', 'j':'z',
            'b':'x', 'm':'q', 'x':'j', 'o':'k', 's':'y',
            't':'v', 'k':'w', 'r':'b', 'e':'o', 'v':'p',
            'y':'g', 'h':'f', 'w':'m', 'c':'u', 'i':'c',
            'z':'d', 'f':'l', 'd':'r', 'n':'n'}
    """
    mapping = {a_map:'a', e_map:'e', h_map:'h', t_map:'t'}
    remain_map_plaintext = "abcdefghijklmnopqrstuvwxyz".replace(a_map,'').replace(e_map, '').replace(h_map, '').replace(t_map, '')
    # remain_map_plaintext = "abcefhijklmopqrstvwxyz".replace(a_map,'').replace(e_map, '').replace(h_map, '').replace(t_map, '')
    remain_map_key = "bcdfgijklmnopqrsuvwxyz"
    # remain_map_key = "bcfgjklmopqsuvwxyz"

    ## generate mapping
    
    def decode(text, mapping):
        plaintext = ""
        for char in text:
            plaintext += mapping[char]

        return plaintext


    # print(cypher_text[2])
    # print(decode(cypher_text[2], mapping))

    for permutation in itertools.permutations(remain_map_key,len(remain_map_key)):
        ## compute mapping
        for cypher_char, plain_char in zip(remain_map_plaintext, permutation):
            mapping[cypher_char] = plain_char
        
        plaintext = decode(cypher_text[0], mapping)

        ### checking
        if check_syntax(plaintext):
            print(plaintext)
            print(mapping)

