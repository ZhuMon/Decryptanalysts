import operator
import enchant
import numpy as np

en_dict = enchant.Dict("en_US")
is_word_thr = 2 # len(char)/2 is correct

def freq(cypher_text):
    f = {}
    for line in cypher_text:
        for char in line:
            if char not in f.keys():
                f[char] = 1
            else:
                f[char] += 1
    return f

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
        m = np.char.ndarray()
        for k in key:
            if k not in tmp:
                if (k == "i" and "j" in tmp) or (k == "j" and "i" in tmp):
                    alphabet = alphabet.replace(k,'')
                    continue
                tmp += k
                alphabet = alphabet.replace(k, '')

        tmp += alphabet
        for row in range(0,5):
            m_tmp = []
            for col in range(0, 5):
                m_tmp.append(tmp[row*5+col])
            m.append(m_tmp)

        return m
    
    def check_position(text, matrix):
        for i in range(5):
            if matrix[:][0]:


    def decrypt(text, matrix):
        ## split text
        s_text = []
        for i in range(len(text) // 2):
            s_text.append(text[0:2])

        for s in s_text:



    key = "abcaijk"
    matrix = gen_matrix(key)
    return False

def hill(cypher_text):
    pass
