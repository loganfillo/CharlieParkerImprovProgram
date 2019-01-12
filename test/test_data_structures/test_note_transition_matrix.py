from unittest import TestCase
from datastructures.base_structures import NoteTransitionMatrix


class TestNoteTransitionMatrix(TestCase):

    def test_init_invalid_size(self):
        from exceptions.Exceptions import InvalidSizeException
        self.assertRaises(InvalidSizeException, NoteTransitionMatrix, 0)

    def test_init_valid_size(self):
        size = 12
        tm = NoteTransitionMatrix(size)
        from datastructures.base_structures import NoteTransition
        for i in range(size):
            for j in range(size):
                self.assertEqual(NoteTransition(i, j), tm.get_matrix()[i][j])
