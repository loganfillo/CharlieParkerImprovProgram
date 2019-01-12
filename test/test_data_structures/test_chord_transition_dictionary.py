from unittest import TestCase
from datastructures.chord_transition_structures import ChordTransitionDictionary, make_chord_transitions


class TestChordTransitionDictionary(TestCase):

    def setUp(self):
        self.size = 12
        self.td = ChordTransitionDictionary(size=self.size)

    def test_init_no_filename(self):
        self.td = None
        self.td = ChordTransitionDictionary(size=self.size)
        chords = make_chord_transitions()
        empty_dict = {x: {y: 0 for y in range(self.size)} for x in range(self.size)}
        chord_dict = []
        for chord in chords:
            chord_dict[chord] = empty_dict
        self.assertTrue(chord_dict, self.td.get_dict())

    def test_init_with_filename(self):
        self.td = None
        self.td = ChordTransitionDictionary(size=self.size, filename="TestChordTransitionDictionary.txt")
        self.assertEqual(self.td.read("TestChordTransitionDictionary.txt"), self.td.get_dict())

    def test_get_note_dict_from_chord(self):
        transitions = []
        for i in range(self.size):
            from datastructures.transitions import NoteTransition
            transitions.append(NoteTransition(i, i))
        chord_transitions = []
        for i in range(self.size):
            from datastructures.transitions import ChordTransition
            from datastructures.transitions import Chord
            chord_transitions.append(ChordTransition(Chord.Maj, Chord.Min))
        d = self.td.get_note_dict_from_chord(ChordTransition(Chord.Maj, Chord.Min))
        for i in range(self.size):
            for j in range(self.size):
                if i ==j:
                    self.assertTrue(d[i][j] == 1)

    def test_add_note_transitions(self):
        transitions = []
        for i in range(self.size):
            from datastructures.transitions import NoteTransition
            transitions.append(NoteTransition(i, i))
        chord_transitions = []
        for i in range(self.size):
            from datastructures.transitions import ChordTransition
            from datastructures.transitions import Chord
            chord_transitions.append(ChordTransition(Chord.Maj, Chord.Min))
        self.td.add_note_transitions(transitions, chord_transitions)
        d = self.td.get_note_dict_from_chord(ChordTransition(Chord.Maj, Chord.Min))
        for i in range(self.size):
            self.assertTrue(self.td[i][i] == 1)


    def test_read_and_write(self):
        import pickle
        before = self.td.get_dict()
        with open("TestChordTransitionDictionary.txt", "wb") as file_b:
            pickle.dump(self.td.get_dict(), file_b)
        with open("TestChordTransitionDictionary.txt", "rb") as file_a:
            after = pickle.load(file_a)
        self.assertEqual(before, after)