from unittest import TestCase
from datastructures.transitions import Transition, NoteTransition, ChordTransition, Chord


class TestTransition(TestCase):

    def test_equals_same_start(self):
        t1 = Transition(1,2)
        t2 = Transition(1,3)
        self.assertNotEqual(t1, t2)

    def test_equals_same_end(self):
        t1 = Transition(1, 3)
        t2 = Transition(2, 3)
        self.assertNotEqual(t1, t2)

    def test_equals_none_same(self):
        t1 = Transition(1, 2)
        t2 = Transition(0, 3)
        self.assertNotEqual(t1, t2)

    def test_equals_is_equal(self):
        t1 = Transition(1,2)
        t2 = Transition(1,2)
        self.assertEqual(t1,t2)


class TestNoteTransition(TestCase):

    def test_init_invalid_start(self):
        from exceptions.Exceptions import  InvalidNoteException
        self.assertRaises(InvalidNoteException, NoteTransition, -1, 0)

    def test_init_invalid_end(self):
        from exceptions.Exceptions import InvalidNoteException
        self.assertRaises(InvalidNoteException, NoteTransition, 0, 128)

    def test_init_invalid_start_and_end(self):
        from exceptions.Exceptions import InvalidNoteException
        self.assertRaises(InvalidNoteException, NoteTransition, -1, 128)

    def test_init_valid(self):
        t = NoteTransition(0, 127)
        self.assertEqual(0, t.get_start())
        self.assertEqual(127, t.get_end())


class TestChordTransition(TestCase):

    def test_init_invalid_start(self):
        from exceptions.Exceptions import  InvalidChordException
        self.assertRaises(InvalidChordException, ChordTransition, "not a chord", Chord.Min)

    def test_init_invalid_end(self):
        from exceptions.Exceptions import InvalidChordException
        self.assertRaises(InvalidChordException, ChordTransition, Chord.Maj, "not a chord")

    def test_init_invalid_start_and_end(self):
        from exceptions.Exceptions import InvalidChordException
        self.assertRaises(InvalidChordException, ChordTransition, "not a chord", "not a chord")

    def test_init_invalid_chord_int(self):
        from exceptions.Exceptions import InvalidChordException
        self.assertRaises(InvalidChordException, ChordTransition, 0, 127)

    def test_init_valid(self):
        t = ChordTransition(Chord.Maj, Chord.HalfDim)
        self.assertEqual(Chord.Maj, t.get_start())
        self.assertEqual(Chord.HalfDim, t.get_end())
