from boardstate import *

# Define scoring patterns and values for White and Black pieces
WHITE_PATTERNS_6 = [
    ['empty', 'white', 'white', 'white', 'white', 'empty'],
    ['empty', 'white', 'white', 'white', 'empty', 'empty'],
    ['empty', 'empty', 'white', 'white', 'white', 'empty'],
    ['empty', 'white', 'white', 'empty', 'white', 'empty'],
    ['empty', 'white', 'empty', 'white', 'white', 'empty'],
    ['empty', 'empty', 'white', 'white', 'empty', 'empty'],
    ['empty', 'empty', 'white', 'empty', 'white', 'empty'],
    ['empty', 'white', 'empty', 'white', 'empty', 'empty'],
    ['empty', 'empty', 'white', 'empty', 'empty', 'empty'],
    ['empty', 'empty', 'empty', 'white', 'empty', 'empty']
]

WHITE_SCORES_6 = [50000, 5000, 5000, 500, 500, 100, 100, 100, 10, 10]

WHITE_PATTERNS_5 = [
    ['white', 'white', 'white', 'white', 'white'],
    ['white', 'white', 'white', 'white', 'empty'],
    ['empty', 'white', 'white', 'white', 'white'],
    ['white', 'white', 'empty', 'white', 'white'],
    ['white', 'empty', 'white', 'white', 'white'],
    ['white', 'white', 'white', 'empty', 'white']
]

WHITE_SCORES_5 = [1000000, 5000, 5000, 5000, 5000, 5000]

BLACK_PATTERNS_6 = [
    ['empty', 'black', 'black', 'black', 'black', 'empty'],
    ['empty', 'black', 'black', 'black', 'empty', 'empty'],
    ['empty', 'empty', 'black', 'black', 'black', 'empty'],
    ['empty', 'black', 'black', 'empty', 'black', 'empty'],
    ['empty', 'black', 'empty', 'black', 'black', 'empty'],
    ['empty', 'empty', 'black', 'black', 'empty', 'empty'],
    ['empty', 'empty', 'black', 'empty', 'black', 'empty'],
    ['empty', 'black', 'empty', 'black', 'empty', 'empty'],
    ['empty', 'empty', 'black', 'empty', 'empty', 'empty'],
    ['empty', 'empty', 'empty', 'black', 'empty', 'empty']
]

BLACK_SCORES_6 = [50000, 5000, 5000, 500, 500, 100, 100, 100, 10, 10]

BLACK_PATTERNS_5 = [
    ['black', 'black', 'black', 'black', 'black'],
    ['black', 'black', 'black', 'black', 'empty'],
    ['empty', 'black', 'black', 'black', 'black'],
    ['black', 'black', 'empty', 'black', 'black'],
    ['black', 'empty', 'black', 'black', 'black'],
    ['black', 'black', 'black', 'empty', 'black']
]

BLACK_SCORES_5 = [1000000, 5000, 5000, 5000, 5000, 5000]

def is_sublist(small, big):
    """
    Check if the list 'small' is contained in 'big'.
    """
    return any(big[i:i+len(small)] == small for i in range(len(big) - len(small) + 1))

def convert_to_str(vector):
    """
    Convert BoardState enums to string values ('white', 'black', 'empty').
    """
    converted = []
    for item in vector:
        if item == BoardState.BLACK:
            converted.append('black')
        elif item == BoardState.WHITE:
            converted.append('white')
        else:
            converted.append('empty')
    return converted

def calculate_score(vector):
    """
    Calculate and return score based on patterns in the input vector.
    """
    score_tally = {'white': 0, 'black': 0}
    vector_str = convert_to_str(vector)
    length = len(vector_str)

    # Evaluate 5-piece patterns
    if length == 5:
        for i, pattern in enumerate(WHITE_PATTERNS_5):
            if pattern == vector_str:
                score_tally['white'] += WHITE_SCORES_5[i]
            if BLACK_PATTERNS_5[i] == vector_str:
                score_tally['black'] += BLACK_SCORES_5[i]
        return score_tally

    # Evaluate partial 5-piece patterns in larger vectors
    for i in range(length - 4):
        segment_5 = vector_str[i:i+5]
        for j, pattern in enumerate(WHITE_PATTERNS_5):
            if pattern == segment_5:
                score_tally['white'] += WHITE_SCORES_5[j]
            if BLACK_PATTERNS_5[j] == segment_5:
                score_tally['black'] += BLACK_SCORES_5[j]

    # Evaluate 6-piece patterns
    for i in range(length - 5):
        segment_6 = vector_str[i:i+6]
        for j, pattern in enumerate(WHITE_PATTERNS_6):
            if pattern == segment_6:
                score_tally['white'] += WHITE_SCORES_6[j]
            if BLACK_PATTERNS_6[j] == segment_6:
                score_tally['black'] += BLACK_SCORES_6[j]

    return score_tally
