import sys
from resource import *
import time
import psutil


MISMATCH_DICT = {
    "A-A" : 0,
    "A-C" : 110,
    "A-G" : 48,
    "A-T" : 94,
        "C-A" : 110,
        "C-C" : 0,
        "C-G" : 118,
        "C-T" : 48,
            "G-A" : 48,
            "G-C" : 118,
            "G-G" : 0,
            "G-T" : 110,
                "T-A" : 94,
                "T-C" : 48,
                "T-G" : 110,
                "T-T" : 0,
}
MATCH_SCORE = 0
GAP_PENALTY = 30


'''
input_string_generator's job is to add the s substring to itself at index n and return that new string 
ex) ACTG 3  --> ACTGACTG
'''
def input_string_generator(s,n):
    return s[:n + 1] + s + s[n + 1:]


def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed

def time_wrapper(s1, s2):
    start_time = time.time()
    algorithm_info = find_sequence_alignment_nw_algo(s1, s2)
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000
    return algorithm_info + "\n" + str(time_taken)


'''
 Sequence Alignment Problem using Needleman-wunsch algorithm as basis
'''


def find_sequence_alignment_nw_algo(s1, s2):
    # s1 = "ACAC"
    # s2 = "TATTA"

    # List Comprehension to make matrix like so:
    #  0 -1 -2 -3
    # -1  0  0  0
    # -2  0  0  0
    # -3  0  0  0


    scoring_matrix = [
        [0 if x == 0 and y == 0 else x * GAP_PENALTY if y == 0 else y * GAP_PENALTY if x == 0 else 0 for x in
         range(len(s2) + 1)] for y in range(len(s1) + 1)]

    # Loop to populate our scoring matrix
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            # Match
            if s1[i - 1] == s2[j - 1]:
                scoring_matrix[i][j] = scoring_matrix[i - 1][j - 1]
            # Mismatch
            else:
                mismatch_id = s1[i - 1] + "-" + s2[j - 1]
                mismatch_score = MISMATCH_DICT[mismatch_id]
                # Recurrence given in class
                scoring_matrix[i][j] = min(scoring_matrix[i - 1][j - 1] + mismatch_score,
                                           scoring_matrix[i - 1][j] + GAP_PENALTY,
                                           scoring_matrix[i][j - 1] + GAP_PENALTY)


    max_alignment_score = scoring_matrix[len(s1)][len(s2)]

    p_i = len(s1)
    p_j = len(s2)
    new_s1 = []
    new_s2 = []

    while p_i > 0 or p_j > 0:
        mismatch_id = s1[p_i - 1] + "-" + s2[p_j - 1]
        mismatch_score = MISMATCH_DICT[mismatch_id]


        if (s1[p_i - 1] == s2[p_j - 1]) or ((scoring_matrix[p_i - 1][p_j -1] + mismatch_score) == scoring_matrix[p_i][p_j]):
            new_s1.append(s1[p_i-1])
            new_s2.append(s2[p_j-1])
            p_j -= 1
            p_i -= 1
        elif (scoring_matrix[p_i - 1][p_j] + GAP_PENALTY ==  scoring_matrix[p_i][p_j]):
            new_s1.append(s1[p_i-1])
            new_s2.append("_")
            p_i -= 1
        elif (scoring_matrix[p_i][p_j - 1] + GAP_PENALTY ==  scoring_matrix[p_i][p_j]):
            new_s1.append("_")
            new_s2.append(s2[p_j-1])
            p_j -= 1

    new_s1 = ''.join(new_s1)[::-1]
    new_s2 = ''.join(new_s2)[::-1]

    #print(new_s1)
    #print(new_s2)
    #print(max_alignment_score)

    return str(max_alignment_score) + "\n" + new_s1 + "\n" + new_s2


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

    algo_and_time_str = time_wrapper(s1,s2)
    memory_useage_str = process_memory()

    final_output_str = (algo_and_time_str + "\n" + str(memory_useage_str))
    print(final_output_str)
    with open(output_file_path, 'w') as f:
        f.writelines(final_output_str)
    #print(s1)
    #print(s2)
    #algorithm_info = find_sequence_alignment_nw_algo(s1,s2)
    #print(algorithm_info)

