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


if __name__ == "__main__":
    cyphertext = "mematrhtgpryetefeteoaat"
    print(len(cyphertext))
    print(rail_fence(cyphertext))
