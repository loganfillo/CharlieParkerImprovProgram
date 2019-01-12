from enum import Enum, unique
from exceptions.Exceptions import InvalidNoteException, InvalidChordException


class Transition:
    """a tuple object containing a starting element and ending element which represents
    a transition from the start element to the end element.

    Attributes:
        __start -- starting element
        __end -- ending element
    """
    def __init__(self, start, end):
        """
        constructs a transition tuple from starting element to ending element
        :param start: the starting element
        :param end: the starting element
        """
        self.__start = start
        self.__end = end

    def __eq__(self, other):
        if isinstance(other, Transition):
            f = self.__start == other.get_start()
            s = self.__end == other.get_end()
            return f and s
        else:
            return False

    def __repr__(self):
        return str((self.__start, self.__end))

    def get_start(self):
        return self.__start

    def get_end(self):
        return self.__end


class NoteTransition(Transition):
    """a tuple object containing a starting note and ending note (both
    represented in the MIDI form i.e, as ints on the range [0,127]) which
    represents a transition between notes. Made for use in a NoteTransitionMatrix

    Attributes:
          see Transition
    """

    def __init__(self, start, end):
        """
        if start or end are not valid MIDI notes, raises InvalidNoteException,
        otherwise constructs a transition tuple from the starting note to the
        end note
        :param int start: the starting note
        :param int end: the ending note
        """
        if not self.__valid_notes(start, end):
            raise InvalidNoteException

        super(NoteTransition, self).__init__(start, end)

    def __valid_notes(self, start, end):
        if start > 127 or start < 0:
            return False
        elif end > 127 or start < 0:
            return False
        else:
            return True


class ChordTransition(Transition):
    #TODO make this hashable, ie override hash and equal
    """a tuple object containing a starting chord and ending chord which represents
    a transition between chords. Made for use in ChordTransition structures

    Attributes:
        see Transition
    """
    def __init__(self, start, end):
        """
        if start or end are not valid chord names, rasies InvalidChordException,
        otherwise constructs a transition tuple from the starting chord to the
        end chord
        :param Chord string start: the starting chord
        :param Chord string end: the ending chord
        """
        if not self.__valid_chord(start, end):
            raise InvalidChordException

        super().__init__(start, end)

    def __repr__(self):
        return (self.get_start().name, self.get_end().name)

    def __valid_chord(self, start, end):
        return isinstance(start, Chord) and isinstance(end, Chord)


@unique
class Chord(Enum):
    """
    represents an enumeration of the different chord types

    Values:
        Maj
        Min
        Dom
        HalfDim
        Dim
    """
    Maj = 1
    Min = 2
    Dom = 3
    HalfDIm = 4
    Dim = 5
