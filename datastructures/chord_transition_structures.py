import pickle
from datastructures.base_structures import NoteTransitionDictionary, ProbabilityMatrix
from datastructures.transitions import Chord, ChordTransition
from exceptions.Exceptions import InvalidTransitionsSizeException


def make_chord_transitions():
    """
    constructs a list of ChordTransitions which contain every
    combination of tuples of Chords
    :return list[ChordTransition] transitions:
    """
    transitions = []
    for from_chord in Chord:
        for to_chord in Chord:
            transition = ChordTransition(from_chord, to_chord)
            transitions.append(transition)
    return transitions


CHORD_TRANSITIONS = make_chord_transitions()


class ChordTransitionDictionary:
    """a chord transition dictionary where the keys (k) are ChordTransitions and
    the associated values are NoteTransitionDictionaries which correspond to
    transitions between notes over the ChordTransition k

    Attributes:
        __dict -- the chord transition dictionary
    """
    def __init__(self, filename=None, size=None):
        """
        constructs an empty chord transition dictionary if filename
        is not specified, otherwise constructs a chord transition dictionary
        from the specified file, with given size of note dictionaries if specified
        :param  string filename: the file to be read from
        :param int size: the size of the note dictionaries
        """
        self.__dict = None
        self.__size = size

        if filename is not None:
            self.__dict = self.read(filename)
        else:
            self.__dict = self.__create_empty_dict()

    def __repr__(self):
        s = ""
        for key in self.__dict:
            s += key.__repr__() + "\n" + self.__dict[key].__repr__() + "\n"
        return s

    def __iter__(self):
        return self.__dict.__iter__()

    def get_dict(self):
        return self.__dict

    def get_note_dict_from_chord(self, chord_transition):
        """
        returns the note transition dictionary associated with the given chord transition
        :param ChordTransition chord_transition: the chord transition
        :return NoteTransitionDictionary dict: the corresponding note transition dictionary
        """
        return self.__dict[chord_transition]

    def add_note_transitions(self, note_transitions, chord_transitions):
        """
        if note_transitions and chord_transitions are not the same size, throws a
        InvalidTransitionsSizeException, else populates self's dict by inserting
        the NoteTransition at index (i) of note_transitions into the NoteTransitionDictionary
        associated with the ChordTransition at index (i)
        :param list[NoteTransition] note_transitions: the list of note transitions
        :param list[ChordTransition] chord_transitions: the list of chord transitions
        :return None:
        """
        if len(note_transitions) != len(chord_transitions):
            raise InvalidTransitionsSizeException()

        for i in range(len(note_transitions)):
            nd = self.__dict[chord_transitions[i]]
            nd.add_note_transitions([note_transitions[i]])

    def read(self, filename):
        """
        reads the file with given filename and stores it into a
        dictionary then returns it
        :param string filename: the file to be read from
        :return dict{ChordTransition: NoteTransitionDictionary:
        """
        with open(filename, "rb") as file:
            self.__dict = pickle.load(file)
        return self.__dict

    def write(self, filename):
        """
        writes self's dict into a file with given filename
        :param string filename: the file to be written to
        :return:
        """
        with open(filename, "wb") as file:
            pickle.dump(self.__dict, file)

    def __create_empty_dict(self):
        d = dict()
        for transition in make_chord_transitions():
            if self.__size is None:
                d.update({transition: NoteTransitionDictionary()})
            else:
                d.update({transition: NoteTransitionDictionary(self.__size)})
        return d


class ChordTransitionMatrixDictionary:
    """a chord transition dictionary where the keys (k) are ChordTransitions and
    the associated values are ProbabilityMatrices which correspond to transitions
    between notes over the ChordTransition k

    Attributes:
        __dict -- the chord transition matrix dictionary
    """
    def __init__(self, filename=None, size=None):
        """
        constructs an empty chord transition matrix dictionary if filename
        is not specified, otherwise constructs a chord transition matrix
        dictionary from the file with given filename, and with probability
        matrices of given size
        :param string filename: the file to be read from
        :param int size: the size of the probability matrices (only for testing purposes)
        """
        self.__dict = None
        self.__size = size

        if filename is not None:
            self.__dict = self.read(filename)
        else:
            self.__dict = self.__create_empty_dict()

    def __repr__(self):
        s = ""
        for key in self.__dict:
            s += key.__repr__() + "\n" + self.__dict[key].__repr__() + "\n"
        return s

    def __iter__(self):
        return self.__dict.__iter__()

    def get_dict(self):
        return self.__dict

    def get_prob_matrix_from_chord(self, chord_transition):
        """
        returns the probability matrix associated with the given chord transition
        :param ChordTransition chord_transition: the chord transition
        :return ProbabilityMatrix:
        """
        return self.__dict[chord_transition]

    def update(self, chord_transition_dictionary):
        """
        update's all the matrices in self's dict using the
        appropriate NoteTransitionDictionary from the given
        chord transition dictionary
        :param chord_transition_dictionary: the chord transition dictionary
        :return None:
        """
        for chord_transition in chord_transition_dictionary:
            pm = self.__dict[chord_transition]
            pm.update(chord_transition_dictionary.get_note_dict_from_chord(chord_transition))

    def read(self, filename):
        """
        reads the file with given filename and stores it into a
        dictionary then returns it
        :param string filename: the file to be read from
        :return dict{ChordTransition: ProbabilityMatrix}
        """
        with open(filename, "rb") as file:
            self.__dict = pickle.load(file)
        return self.__dict

    def write(self, filename):
        """
        writes self's dict into a file with given filename
        :param string filename: the file to write to
        :return None:
        """
        with open(filename, "wb") as file:
            pickle.dump(self.__dict, file)

    def __create_empty_dict(self):
        d = dict()
        for transition in make_chord_transitions():
            if self.__size is None:
                d.update({transition: ProbabilityMatrix()})
            else:
                d.update({transition: ProbabilityMatrix(self.__size)})
        return d
