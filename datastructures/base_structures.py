import pickle
from exceptions.Exceptions import InvalidPowerException, InvalidSizeException
from datastructures.transitions import NoteTransition


DEFAULT_SIZE = 128


class NoteTransitionMatrix:
    """ a transition matrix where each entry i,j contains Transition(i-1, j-1) which
     represents a transition from  the MIDI note i-1 to  the MIDI note j-1. This
     data structure is useful when generating a list of MIDI notes based on the
     associated probability matrix, as well as easily analysing the transitions

     Attributes:
         __size -- size of the n x n matrix
         __matrix -- the note transition matrix
    """

    def __init__(self, size=DEFAULT_SIZE):
        """
        if size is note greater than 0, raises InvalidSizeException, else
        constructs a note transition matrix based on given size
        :param int size: the size of the matrix
        """
        if not size > 0:
            raise InvalidSizeException

        self.__size = size
        self.__matrix = self.__create_transition_matrix()

    def __repr__(self):
        string = "\n"
        for row in self.__matrix:
            string += str(row) + "\n"
        return string

    def __iter__(self):
        return self.__matrix.__iter__()

    def get_size(self):
        return self.__size

    def get_matrix(self):
        return self.__matrix

    def __create_transition_matrix(self):
        return [[NoteTransition(row, column) for column in range(self.__size)] for row in range(self.__size)]


class NoteTransitionDictionary:
    """a note transition dictionary where the keys (i) represent MIDI notes that span the range
    [0,size). Each associated value is another dictionary where again the keys (j) represent
    MIDI notes and span the range [0, size). Their associated values are ints which represent
    the number of transitions from the MIDI note i to the MIDI note j

    Attributes:
         __size -- the number of keys in the dictionary
         __dict -- the note transition dictionary
    """

    def __init__(self, size=DEFAULT_SIZE, filename=None):
        """
        if size is note greater than 0, raises InvalidSizeException, else
        constructs an empty note transition dictionary if filename is not specified,
        otherwise constructs a note transition dictionary from specified file
        :param int size: the size of the dictionary
        :param string filename: the file to be read from
        """
        if not size > 0:
            raise InvalidSizeException

        self.__size = size
        self.__dict = None

        if filename is not None:
            self.read(filename)
        else:
            self.__create_empty_dict()

    def __eq__(self, other):
        return isinstance(other, NoteTransitionDictionary) and other.get_dict() == self.__dict

    def __iter__(self):
        return self.__dict.__iter__()

    def __repr__(self):
        string = "{\n"
        for key in self.__dict:
            string += str(key)+": "+str(self.__dict[key]) + "\n"
        return string + "}"

    def get_size(self):
        return self.__size

    def get_dict(self):
        return self.__dict

    def add_note_transitions(self, transitions):
        """
        increments the part of the dictionary by one associated with every
        NoteTransition in transitions
        :param list[NoteTransition] transitions: the list of NoteTransitions
        :return None:
        """
        for transition in transitions:
            start = transition.get_start()
            end = transition.get_end()
            self.__dict[start][end] += 1

    def write(self, filename):
        """
        writes self's dictionary into a file with given filename
        :param string filename: the file to be saved into
        :return None:
        """
        with open(filename, "wb") as file:
            pickle.dump(self.__dict, file)

    def read(self, filename):
        """
        reads the given file with filename and stores it into a
        dictionary then returns it
        :param string filename: name of file to be read
        :return dict{int: dict|{int: int}:
        """
        with open(filename, "rb") as file:
            self.__dict = pickle.load(file)
        return self.__dict

    def __create_empty_dict(self):
        self.__dict = {x: {y: 0 for y in range(self.__size)} for x in range(self.__size)}


class ProbabilityMatrix:
    """ a probability (or stochastic) matrix associated to a transition matrix
    in a markov chain model. Each entry i,j in the matrix is the probability
    of going from i to j

    Attributes:
         __size -- size of the n x n matrix
         __matrix -- the probability matrix
    """

    def __init__(self, size=DEFAULT_SIZE, filename=None):
        """
        constructs an empty probability matrix if filename is not specified,
        otherwise constructs a probability matrix from the given file
        :param int size: size of the matrix
        :param string filename: the name of the files to be read from
        """
        if not size > 0:
            raise InvalidSizeException()

        self.__size = size
        self.__matrix = None

        if filename is not None:
            self.read(filename)
        else:
            self.__create_zero_matrix()

    def __eq__(self, other):
        return isinstance(other, ProbabilityMatrix) and other.get_matrix() == self.__matrix

    def __iter__(self):
        return self.__matrix.__iter__()

    def __repr__(self):
        string = "[\n"
        for row in self.__matrix:
            string += str(row) + "\n"
        return string + "]"

    def get_matrix(self):
        return self.__matrix

    def get_size(self):
        return self.__size

    def transpose(self):
        """
        returns self's transposed matrix
        :return list[list[int]]:
        """
        return [[row[i] for row in self.__matrix] for i in range(self.__size)]

    def power(self, times):
        """
        if times is not greater than 0, raises InvalidPowerException, else
        returns a copy of self's matrix raised to the power given by times
        :param int times: the power to which the matrix is raised
        :return list[list[int]]:
        """
        if not times > 0:
            raise InvalidPowerException

        current_matrix = self.__matrix[:]
        while times - 1 > 0:
            current_matrix = self.__make_new_matrix(current_matrix)
            times -= 1

        return current_matrix

    def update(self, note_trans_dict):
        """
        updates self's matrix entries based on the given dictionary
        :param NoteTransitionDictionary note_trans_dict: the dictionary to use in the update
        :return None:
        """
        dict = note_trans_dict.get_dict()
        for row in range(self.__size):
            sub_dict = dict[row]
            self.__update_entries(row, sub_dict)

    def write(self, filename):
        """
        writes self's matrix into a file with given filename
        :param string filename: the file to be saved into
        :return None:
        """
        with open(filename, "wb") as file:
            pickle.dump(self.__matrix, file)

    def read(self, filename):
        """
        reads the file and sets its contents to be self's matrix and returns it
        :param string filename: the file to be read from
        :return list[list[int]]: self's matrix
        """
        with open(filename, "rb") as file:
            self.__matrix = pickle.load(file)
        return self.__matrix

    def __create_zero_matrix(self):
        self.__matrix = [[0 for column in range(self.__size)] for row in range(self.__size)]

    def __make_new_matrix(self, matrix):
        return [self.__make_new_row(matrix[row]) for row in range(self.__size)]

    def __make_new_row(self, row_m):
        transpose = self.transpose()
        return [self.__make_new_entry(row_m, transpose[column]) for column in range(self.__size)]

    def __make_new_entry(self, row_m, row_t):
        return sum([x*y for x,y in zip(row_m, row_t)])

    def __update_entries(self, row, sub_dict):
        current_row = self.__matrix[row]
        total = sum(sub_dict.values())
        if total > 0:
            for entry in range(self.__size):
                current_row[entry] = sub_dict[entry] / total

