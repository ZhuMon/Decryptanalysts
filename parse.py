from mono import *

# num = input("1~6")
num = 3
# 1: poly
# 2: mono
# 3: column
with open(f"project/ciphertext{num}.txt", "r") as f:
    lines = f.readlines()

parsed_lines = []
for line in lines:
    parsed_line = line[1:-2]
    parsed_lines.append(parsed_line)
    


c = caesar(parsed_lines)
if c == True:
    print("caesar")

p = playfair(parsed_lines)
if p:
    print("playfair")

