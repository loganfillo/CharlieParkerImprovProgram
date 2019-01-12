from unittest import TestCase
from datastructures.base_structures import NoteTransitionDictionary
from datastructures.transitions import NoteTransition


class TestNoteTransitionDictionary(TestCase):

    def setUp(self):
        self.size = 10
        self.nd = NoteTransitionDictionary(self.size)

    def test_init_invalid_size(self):
        from exceptions.Exceptions import InvalidSizeException
        self.assertRaises(InvalidSizeException, NoteTransitionDictionary, 0)

    def test_init_no_filename(self):
        self.nd = None
        self.nd = NoteTransitionDictionary(self.size)
        empty_dict = {x: {y: 0 for y in range(self.size)} for x in range(self.size)}
        self.assertEqual(self.nd.get_dict(),  empty_dict)

    def test_init_with_filename(self):
        self.nd = None
        self.nd = NoteTransitionDictionary(self.size, filename="TestNoteTransitionDictionary.txt")
        self.assertEqual(self.nd.read("TestNoteTransitionDictionary.txt"), self.nd.get_dict())

    def test_add_note_transition(self):
        import random as rand
        transitions = []
        for x in range(self.size**2):
            start = rand.randint(0, self.size - 1)
            end = rand.randint(0, self.size - 1)
            transitions.append(NoteTransition(start, end))
        self.nd.add_note_transitions(transitions)
        for transition in transitions:
            amount = transitions.count(transition)
            start= transition.get_start()
            end = transition.get_end()
            self.assertEqual(self.nd.get_dict()[start][end], amount)

    def test_write_and_read(self):
        import pickle
        before = dict(self.nd.get_dict())
        with open("TestNoteTransitionDictionary.txt", "wb") as file_b:
            pickle.dump(self.nd.get_dict(), file_b)
        with open("TestNoteTransitionDictionary.txt", "rb") as file_a:
            after = pickle.load(file_a)
        self.assertEqual(before, after)
