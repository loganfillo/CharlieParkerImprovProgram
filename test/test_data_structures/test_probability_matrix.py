from unittest import TestCase
from datastructures.base_structures import ProbabilityMatrix
from datastructures.transitions import NoteTransition


class TestProbabilityMatrix(TestCase):

    def setUp(self):
        self.size = 12
        self.pm = ProbabilityMatrix(self.size)
        import random as rand
        for x in range(self.size**2):
            i = rand.randint(0,self.size-1)
            j = rand.randint(0,self.size-1)
            self.pm.get_matrix()[i][j] = rand.randint(0,10)
            x -= 1

    def test_init_invalid_size(self):
        from exceptions.Exceptions import InvalidSizeException
        self.assertRaises(InvalidSizeException, ProbabilityMatrix, 0)

    def test_init_no_filename(self):
        self.pm = None
        self.pm = ProbabilityMatrix(self.size)
        zeros = [[0 for column in range(self.size)] for row in range(self.size)]
        self.assertEqual(zeros, self.pm.get_matrix())

    def test_init_with_filename(self):
        self.pm = None
        self.pm = ProbabilityMatrix(self.size, filename="TestProbabilityMatrix.txt")
        self.assertEqual(self.pm.read("TestProbabilityMatrix.txt"), self.pm.get_matrix())

    def test_transpose(self):
        t = self.pm.transpose()
        for x in range(self.size):
            for y in range(self.size):
                self.assertEqual(self.pm.get_matrix()[x][y], t[y][x])

    def test_power_invalid_times(self):
        from exceptions.Exceptions import InvalidPowerException
        self.assertRaises(InvalidPowerException, self.pm.power, 0)

    def test_power_one_time(self):
        self.assertEqual(self.pm.get_matrix(), self.pm.power(1))

    def test_power_two_times(self):
        t = self.pm.transpose()
        for x in range(self.size):
            for y in range(self.size):
                entry = sum([x*y for x,y in zip(self.pm.get_matrix()[x], t[y])])
                self.assertEqual(self.pm.power(2)[x][y], entry)

    def test_update_empty(self):
        from datastructures.base_structures import NoteTransitionDictionary
        empty = NoteTransitionDictionary(self.size)
        before = self.pm.get_matrix()[:]
        self.pm.update(empty)
        self.assertEqual(before, self.pm.get_matrix())

    def test_update_not_empty(self):
        from datastructures.base_structures import NoteTransitionDictionary
        import random as rand
        nd = NoteTransitionDictionary(self.size)
        transitions = []
        for x in range(self.size**2):
            start = rand.randint(0, self.size-1)
            end = rand.randint(0, self.size-1)
            transitions.append(NoteTransition(start,end))
        nd.add_note_transitions(transitions)
        self.pm.update(nd)
        for i in range(self.size):
            for j in range(self.size):
                total = sum(nd.get_dict()[i].values())
                if total > 0:
                    self.assertEqual(self.pm.get_matrix()[i][j], nd.get_dict()[i][j]/total)

    def test_write_and_read(self):
        import pickle
        before = self.pm.get_matrix()[:]
        with open("TestProbabilityMatrix.txt", "wb") as file_b:
            pickle.dump(self.pm.get_matrix(), file_b)
        with open("TestProbabilityMatrix.txt", "rb") as file_a:
            after = pickle.load(file_a)
        self.assertEqual(before, after)

