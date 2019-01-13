from unittest import TestCase
from datastructures.chord_transition_structures import ChordTransitionMatrixDictionary, \
                                                       ChordTransitionDictionary,\
                                                       make_chord_transitions


class TestChordTransitionMatrixDictionary(TestCase):

    def setUp(self):
        self.size = 2
        self.tmd = ChordTransitionMatrixDictionary(size=self.size)

    def test_init_no_filename(self):
        self.tmd = None
        self.tmd = ChordTransitionMatrixDictionary(size=self.size)
        chords = make_chord_transitions()
        chord_dict = {}
        for chord in chords:
            from datastructures.base_structures import ProbabilityMatrix
            chord_dict.update({chord : ProbabilityMatrix(self.size)})
        self.assertEqual(chord_dict, self.tmd.get_dict())

    def test_init_with_filename(self):
        self.tmd = None
        self.tmd = ChordTransitionMatrixDictionary(size=self.size, filename="TestChordTransitionMatrixDictionary.txt")
        self.assertEqual(self.tmd.read("TestChordTransitionMatrixDictionary.txt"), self.tmd.get_dict())

    def test_update_and_get_prob_matrix_from_chord(self):
        td = ChordTransitionDictionary()
        transitions = []
        for i in range(self.size):
            from datastructures.transitions import NoteTransition
            transitions.append(NoteTransition(i, i))
        chord_transitions = []
        for i in range(self.size):
            from datastructures.transitions import ChordTransition
            from datastructures.transitions import Chord
            chord_transitions.append(ChordTransition(Chord.Maj, Chord.Min))
        td.add_note_transitions(transitions, chord_transitions)
        for i in range(self.size):
            self.assertTrue(self.tmd.get_prob_matrix_from_chord(
                 ChordTransition(Chord.Maj, Chord.Min)).get_matrix()[i][i]==0)
        self.tmd.update(td)
        from datastructures.transitions import Chord
        m = self.tmd.get_prob_matrix_from_chord(ChordTransition(Chord.Maj, Chord.Min))
        for i in range(self.size):
            self.assertTrue(m.get_matrix()[i][i] == 1)

    def test_write_and_read(self):
        import pickle
        before = dict(self.tmd.get_dict())
        with open("TestChordTransitionMatrixDictionary.txt", "wb") as file_b:
            pickle.dump(self.tmd.get_dict(), file_b)
        with open("TestChordTransitionMatrixDictionary.txt", "rb") as file_a:
            after = pickle.load(file_a)
        self.assertEqual(before, after)

