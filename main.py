import sys

# test

MISMATCH_DICT = {
    "A-A" : 0,
    "A-C" : 110,
"A-G" : 110,
"A-T" : 110,
"C-A" : 110,
"C-C" : 110,
"C-G" : 110,
"C-T" : 110,
"G-A" : 110,
"G-C" : 110,
"G-G" : 110,
"G-T" : 110,
"T-A" : 110,
"T-C" : 110,
"T-G" : 110,
"T-T" : 110,



}

'''
input_string_generator's job is to add the s substring to itself at index n and return that new string 
ex) ACTG 3  --> ACTGACTG
'''
def input_string_generator(s,n):
    return s[:n + 1] + s + s[n + 1:]


if __name__ == '__main__':
    input_file_path = str(sys.argv[1])
    output_file_path = str(sys.argv[2])

    with open(input_file_path) as f:
        input_lines = [line.strip() for line in f]

    s1 = input_lines[0]  # Guaranteed to always be first element in our file
    s2 = ""
    s1_copy_instructions = []
    s2_copy_instructions = []
    f_s1 = ""
    f_s2 = ""

    # Loops over our input file and parses info accordingly
    for i in range (1, len(input_lines)):
        if (input_lines[i].isdigit() and len(s2) == 0):
            s1_copy_instructions.append(int(input_lines[i]))
        elif (input_lines[i].isdigit() and len(s2) != 0):
            s2_copy_instructions.append(int(input_lines[i]))
        else:
            s2 = input_lines[i]

    s1_og_len = len(s1)
    s2_og_len = len(s2)

    # Generates our new string based on copying itself to index in copy instructions
    for j in s1_copy_instructions:
        s1 = input_string_generator(s1, j)

    for k in s2_copy_instructions:
        s2 = input_string_generator(s2, k)

    assert len(s1) == (2**len(s1_copy_instructions)) * s1_og_len , "Length of S1 is not correct. Oh no"
    assert (len(s2) == (2 ** len(s2_copy_instructions)) * s2_og_len),  "Length of S2 is not correct. Oh no"


