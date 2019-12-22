from mono import check_syntax

def rail_fence(cyphertext):
    one_string = ""
    for line in cyphertext:
        one_string += line

    mid_num = len(one_string)//2 if len(one_string) % 2 == 1 else len(one_string)//2 + 1
    forward_string = one_string[:len(one_string)//2+1]
    backward_string = one_string[len(one_string)//2+1:]

    plaintext = ""
    for f, b in zip(forward_string, backward_string):
        plaintext += f+b

    return plaintext

def factor(num):
    """ find factor of a num exclusive 1 and num
    """
    factor_list = []
    for i in range(2, num//2+1):
        if num % i == 0:
            factor_list.append(i)
    return factor_list

def row_transposition(cyphertext):
    ## one string
    one_string = ""
    for line in cyphertext:
        one_string += line 
    
    ## find factor
    num_char = len(one_string)
    factor_list = factor(num_char)
    ## decode
    plaintext_list = []
    for f in factor_list:
        """ f = 2, f_inv = 3
        ab cd ef -> a c e -> acebdf
                    b d f
        """
        # f_inv = len(one_string) // f   # f * f_inv = len(one_string)
        split_rect = [ one_string[index:index+f] for index in range(0, len(one_string), f)]
        ### concat
        plaintext = ""
        for i in range(f):
            for char_list in split_rect:
                if i < len(char_list):
                    plaintext += char_list[i]

        if check_syntax(plaintext[0:50], 3):
            print(f)
            return True

        # plaintext_list.append(plaintext)

    # return plaintext_list
    return False

def encode_row_tran(plaintext):
    ## one string
    one_string = ""
    for line in plaintext:
        one_string += line
    one_string = one_string.replace('\n','')

    f = 75
    split_rect = [ one_string[index:index+f] for index in range(0, len(one_string), f)]
    cyphertext = ""
    for i in range(f):
        for line in split_rect:
            cyphertext += line[i]
        if i == 0:
            print(cyphertext)
            print(len(cyphertext))

    # with open("cyphertext3.txt", "w") as f:
    #     f.write(cyphertext)

if __name__ == "__main__":
    # cyphertext = "mematrhtgpryetefeteoaat"
    # print(len(cyphertext))
    # print(rail_fence(cyphertext))
    # a = ['abcd','ef']
    # print(row_transposition(a))
    # with open("test.txt", "r") as f:
    #     line_list = f.readlines()
    # encode_row_tran(line_list)
    pass

