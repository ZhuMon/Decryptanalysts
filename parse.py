
# num = input("1~6")
num = 1
with open(f"project/ciphertext{num}.txt", "r") as f:
    lines = f.readlines()

parsed_lines = []
for line in lines:
    parsed_line = line[1:-2]
    parsed_lines.append(parsed_line)


print(parsed_lines[0])
