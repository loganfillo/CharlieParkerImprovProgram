import midi
import numpy.random as rand
import ProbabilityMatrix as pm





def write_note_dict(note_dict, filename):
    """
    writes the note_dict into a file with name filename
    :param dict{int : dict{int: int}} note_dict: the dictionary to be written
    :param string filename: name of file
    :return None:
    """
    with open(filename, 'w') as file:
        file.write(str(note_dict))

def read_note_dict(filename):
    """
    reads the given file with filename and stores it into a dictionary
    of dictionaries and returns it
    :param string filename: name of file to be read
    :return dict{int : dict{int: int}} note_dict: the dictionary to be read
    """
    with open(filename, 'r') as file:
        string = file.read()
        return eval(string)

class TransitionMatrix:

    def __init__(self, size):
        """
        constructs a transition matrix
        :param int size: size of the matrix
        """
        self.matrix = create_transition_matrix(size)

    def get_matrix(self):
        return self.matrix












def print_data_structures(size):

    transition_matrix = create_transition_matrix(size)
    probability_matrix = create_zero_matrix(size)
    note_dict = create_note_dict(size)

    for row in transition_matrix:
        #print(row)
        pass
    for row in probability_matrix:
        #print(row)
        pass
    for key in note_dict.keys():
        print(key, note_dict[key])

    write_note_dict(note_dict, "NoteDictionary")
    note_dict = read_note_dict("NoteDictionary")
    print("\n")

    add_note_transition(0, 2, note_dict)
    add_note_transition(0, 3, note_dict)
    add_note_transition(4, 5, note_dict)



    for key in note_dict.keys():
        print(key, note_dict[key])


new_message = midi.Message(midi.NoteOn(60,50),1)












