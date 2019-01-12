import numpy as np


def execute(starting_note, amount):
    """
    constructs a markov model consisting of a state space of musical notes: {C,E,G,B},
    checks if it is a valid markov model, then uses it to generate a set of musical notes
    :param string starting_note: the starting note
    :param int amount: the amount of notes generated
    :return list[string] notes: the generated notes
    """

    states = {"C", "E", "G", "B"}

    trans_matrix = [
        ["CC", "CE", "CG", "CB"],
        ["EC", "EE", "EG", "EB"],
        ["GC", "GE", "GG", "GB"],
        ["BC", "BE", "BG", "BB"]
    ]

    prob_matrix = [
        [0.2, 0.5, 0.2, 0.1],
        [0.4, 0.1, 0.4, 0.1],
        [0.2, 0.3, 0.2, 0.3],
        [0.4, 0.2, 0.3, 0.1]
    ]

    if not check_if_valid(prob_matrix):
        print("Probability matrix does not have stochastic rows")
        return

    notes = generate_notes(starting_note, amount, trans_matrix, prob_matrix)
    return notes

def generate_notes(starting_note, amount, trans_matrix, prob_matrix):
    """
    uses the markov model to generate a set of musical notes based on a given
    starting note and an amount of notes
    :param string starting_note: the starting note
    :param int amount: the amount of notes generated
    :param list[list[string]] trans_matrix: the transition matrix
    :param list[list[int]] prob_matrix: the probability matrix associated with trans_matrix
    :return list[string] notes: set of generated music notes
    """
    notes = [starting_note]
    current_note = starting_note
    i = 1
    while i<amount:
        if current_note == "C":
            current_note = generate_next_note(0, trans_matrix, prob_matrix)
            notes.append(current_note)
        elif current_note == "E":
            current_note = generate_next_note(1, trans_matrix, prob_matrix)
            notes.append(current_note)
        elif current_note == "G":
            current_note = generate_next_note(2, trans_matrix, prob_matrix)
            notes.append(current_note)
        elif current_note == "B":
            current_note = generate_next_note(3, trans_matrix, prob_matrix)
            notes.append(current_note)
        i += 1
    return notes

def generate_next_note(index, trans_matrix, prob_matrix):
    """
    based on the current note, generates the next note by randomly choosing
    a transition using the trans_matrix and prob_matrix
    :param int index: the row of the matrix corresponding to the current note
    :param list[list[string]] trans_matrix: the transition matrix
    :param list[list[int]] prob_matrix: the probability matrix associated with trans_matrix
    :return string next_note: the next note
    """
    transition = np.random.choice(trans_matrix[index], replace= True, p = prob_matrix[index])
    next_note = transition[1]
    return next_note


def check_if_valid(prob_matrix):
    """
    returns true if the prob_matrix is a valid
    markov probability matrix
    :param list[list[int]] prob_matrix: the probability matrix to check
    :return: bool
    """
    if (
            sum(prob_matrix[0]) +
            sum(prob_matrix[1]) +
            sum(prob_matrix[2]) +
            sum(prob_matrix[3]) != 4.0
    ):
        return False
    else:
        return True


def count_chords():
    i = 0
    limit = 1000
    count = 0
    while i<limit:
        outcome = execute("C", 3)
        if outcome[0] == "C" and outcome[1] == "E" and outcome[2] == "G":
            count += 1
        i += 1
    print("The percentage is: " + str(count/limit * 100))
    return count/limit * 100


def average_chords():
    i = 0
    limit = 20
    outcomes = []
    while i < 20:
        outcomes.append(count_chords())
        i += 1
    print(str(sum(outcomes)/limit))

average_chords()





