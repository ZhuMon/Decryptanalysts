from mono import *
from transposition import *

num = input("1~6")
# num = 1
# 1: poly 9600 has j
# 2: mono 9600 has j
# 3: column 9599 has j
with open(f"project/ciphertext{num}.txt", "r") as f:
    lines = f.readlines()

count = 0
parsed_lines = []
for line in lines:
    parsed_line = line[1:-2]
    parsed_lines.append(parsed_line)
    count += len(parsed_line)

print(count)

print(factor(count))
# c = caesar(parsed_lines)
# if c == True:
    # print("caesar")

# p = playfair(parsed_lines)
# if p:
#     print("playfair")

# b = brute_force(parsed_lines)
# b = advanced_brute_force(parsed_lines)

# t = rail_fence(parsed_lines)
# print(freq(parsed_lines))
# r = row_transposition(parsed_lines)

# m = map_known_mapping(parsed_lines)
# r = row_transposition(m)

# if r:
#     print("yes")

# print(r[0:100])
