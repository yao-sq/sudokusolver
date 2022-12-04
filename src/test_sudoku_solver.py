from unittest import TestCase
import numpy as np
from sudoku_solver import sudoku_solver, vars_in_box


class Test(TestCase):
    def test_solver_veryeasy(self):
        self.check_solver_ondata("very_easy")

    def test_solver_easy(self):
        self.check_solver_ondata("easy")

    def test_solver_medium(self):
        self.check_solver_ondata("medium")

    def test_solver_hard(self):
        self.check_solver_ondata("hard")

    # extra puzzles

    def test_solver_extra_medium_1(self):
        sudoku = np.array([
            [0, 2, 0, 0, 0, 0, 7, 0, 1],
            [0, 7, 0, 0, 6, 0, 8, 0, 0],
            [8, 9, 0, 7, 0, 1, 0, 0, 0],
            [0, 5, 9, 1, 0, 0, 0, 0, 0],
            [6, 0, 0, 9, 0, 4, 0, 0, 8],
            [0, 0, 0, 0, 0, 2, 5, 9, 0],
            [0, 0, 0, 4, 0, 8, 0, 6, 2],
            [0, 0, 3, 0, 2, 0, 0, 1, 0],
            [9, 0, 2, 0, 0, 0, 0, 8, 0]
        ])
        expected = np.array([
            [5, 2, 6, 8, 4, 9, 7, 3, 1],
            [3, 7, 1, 2, 6, 5, 8, 4, 9],
            [8, 9, 4, 7, 3, 1, 2, 5, 6],
            [2, 5, 9, 1, 8, 3, 6, 7, 4],
            [6, 3, 7, 9, 5, 4, 1, 2, 8],
            [1, 4, 8, 6, 7, 2, 5, 9, 3],
            [7, 1, 5, 4, 9, 8, 3, 6, 2],
            [4, 8, 3, 5, 2, 6, 9, 1, 7],
            [9, 6, 2, 3, 1, 7, 4, 8, 5]
        ])
        self.check_solver(sudoku, expected)

    def test_solver_extra_medium_2(self):
        sudoku = np.array([
            [2, 0, 0, 0, 0, 8, 0, 4, 5],
            [9, 0, 8, 0, 0, 0, 0, 1, 0],
            [0, 0, 7, 1, 2, 4, 0, 8, 0],
            [5, 0, 0, 8, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 7, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 7],
            [0, 3, 0, 7, 6, 2, 5, 0, 0],
            [0, 9, 0, 0, 0, 0, 1, 0, 3],
            [4, 2, 0, 3, 0, 0, 0, 0, 8]
        ])
        expected = np.array([
            [2, 1, 3, 6, 9, 8, 7, 4, 5],
            [9, 4, 8, 5, 3, 7, 2, 1, 6],
            [6, 5, 7, 1, 2, 4, 3, 8, 9],
            [5, 7, 2, 8, 4, 6, 9, 3, 1],
            [1, 6, 4, 9, 7, 3, 8, 5, 2],
            [3, 8, 9, 2, 5, 1, 4, 6, 7],
            [8, 3, 1, 7, 6, 2, 5, 9, 4],
            [7, 9, 6, 4, 8, 5, 1, 2, 3],
            [4, 2, 5, 3, 1, 9, 6, 7, 8]
        ])
        self.check_solver(sudoku, expected)

    def test_solver_extra_hard_1(self):
        sudoku = np.array([
            [2, 0, 0, 0, 0, 0, 8, 4, 0],
            [9, 0, 0, 0, 3, 4, 0, 0, 0],
            [0, 0, 4, 6, 0, 0, 0, 1, 0],
            [0, 4, 0, 0, 0, 0, 6, 9, 1],
            [0, 0, 0, 8, 0, 3, 0, 0, 0],
            [7, 2, 6, 0, 0, 0, 0, 5, 0],
            [0, 8, 0, 0, 0, 7, 1, 0, 0],
            [0, 0, 0, 3, 8, 0, 0, 0, 2],
            [0, 7, 2, 0, 0, 0, 0, 0, 4]
        ])
        expected = np.array([
            [2, 6, 7, 1, 9, 5, 8, 4, 3],
            [9, 1, 8, 2, 3, 4, 5, 7, 6],
            [5, 3, 4, 6, 7, 8, 2, 1, 9],
            [8, 4, 3, 7, 5, 2, 6, 9, 1],
            [1, 9, 5, 8, 6, 3, 4, 2, 7],
            [7, 2, 6, 9, 4, 1, 3, 5, 8],
            [6, 8, 9, 4, 2, 7, 1, 3, 5],
            [4, 5, 1, 3, 8, 9, 7, 6, 2],
            [3, 7, 2, 5, 1, 6, 9, 8, 4]
        ])
        self.check_solver(sudoku, expected)

    def test_solver_extra_extreme_1(self):
        sudoku = np.array([
            [0, 9, 0, 0, 0, 0, 5, 0, 0],
            [7, 0, 0, 0, 0, 9, 1, 6, 0],
            [0, 0, 6, 0, 0, 8, 0, 3, 0],
            [0, 0, 0, 0, 0, 5, 6, 0, 3],
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [8, 0, 1, 3, 0, 0, 0, 0, 0],
            [0, 1, 0, 5, 0, 0, 9, 0, 0],
            [0, 7, 3, 9, 0, 0, 0, 0, 6],
            [0, 0, 4, 0, 0, 0, 0, 7, 0]
        ])
        expected = np.array([
            [3, 9, 2, 1, 6, 4, 5, 8, 7],
            [7, 8, 5, 2, 3, 9, 1, 6, 4],
            [1, 4, 6, 7, 5, 8, 2, 3, 9],
            [4, 2, 7, 8, 9, 5, 6, 1, 3],
            [5, 3, 9, 4, 1, 6, 7, 2, 8],
            [8, 6, 1, 3, 2, 7, 4, 9, 5],
            [6, 1, 8, 5, 7, 3, 9, 4, 2],
            [2, 7, 3, 9, 4, 1, 8, 5, 6],
            [9, 5, 4, 6, 8, 2, 3, 7, 1]
        ])
        self.check_solver(sudoku, expected)


    # helpers

    def check_solver_ondata(self, difficulty):
        sudoku = np.load("../sudoku_org/data/"+difficulty+"_puzzle.npy")[0]
        expected = np.load("../sudoku_org/data/"+difficulty+"_solution.npy")[0]
        self.check_solver(sudoku, expected)

    def check_solver(self, input, expected):
        print("Input:\n", input)
        print("Solution (expected):\n", expected)

        solution = sudoku_solver(input)
        print("Solution (actual):\n", solution)

        self.assertTrue(np.array_equal(solution, expected))

    # other tests

    def test_vars_in_box(self):
        self.assertEqual(sorted(["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]), sorted(list(vars_in_box("A1"))))
        self.assertEqual(sorted(["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]), sorted(list(vars_in_box("A2"))))
        self.assertEqual(sorted(["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]), sorted(list(vars_in_box("A3"))))
        self.assertEqual(sorted(["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]), sorted(list(vars_in_box("B1"))))
        self.assertEqual(sorted(["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]), sorted(list(vars_in_box("B2"))))
        self.assertEqual(sorted(["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]), sorted(list(vars_in_box("B3"))))
        self.assertEqual(sorted(["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]), sorted(list(vars_in_box("C1"))))
        self.assertEqual(sorted(["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]), sorted(list(vars_in_box("C2"))))
        self.assertEqual(sorted(["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]), sorted(list(vars_in_box("C3"))))

        # vertical
        self.assertEqual(sorted(["A4", "A5", "A6", "B4", "B5", "B6", "C4", "C5", "C6"]), sorted(list(vars_in_box("A4"))))
        self.assertEqual(sorted(["A4", "A5", "A6", "B4", "B5", "B6", "C4", "C5", "C6"]), sorted(list(vars_in_box("A5"))))
        self.assertEqual(sorted(["A4", "A5", "A6", "B4", "B5", "B6", "C4", "C5", "C6"]), sorted(list(vars_in_box("A6"))))

        self.assertEqual(sorted(["A7", "A8", "A9", "B7", "B8", "B9", "C7", "C8", "C9"]), sorted(list(vars_in_box("A7"))))
        self.assertEqual(sorted(["A7", "A8", "A9", "B7", "B8", "B9", "C7", "C8", "C9"]), sorted(list(vars_in_box("A8"))))
        self.assertEqual(sorted(["A7", "A8", "A9", "B7", "B8", "B9", "C7", "C8", "C9"]), sorted(list(vars_in_box("A9"))))

        # horizontal
        self.assertEqual(sorted(["D1", "D2", "D3", "E1", "E2", "E3", "F1", "F2", "F3"]), sorted(list(vars_in_box("D1"))))
        self.assertEqual(sorted(["D1", "D2", "D3", "E1", "E2", "E3", "F1", "F2", "F3"]), sorted(list(vars_in_box("E1"))))
        self.assertEqual(sorted(["D1", "D2", "D3", "E1", "E2", "E3", "F1", "F2", "F3"]), sorted(list(vars_in_box("F1"))))

        self.assertEqual(sorted(["G1", "G2", "G3", "H1", "H2", "H3", "I1", "I2", "I3"]), sorted(list(vars_in_box("G1"))))
        self.assertEqual(sorted(["G1", "G2", "G3", "H1", "H2", "H3", "I1", "I2", "I3"]), sorted(list(vars_in_box("H1"))))
        self.assertEqual(sorted(["G1", "G2", "G3", "H1", "H2", "H3", "I1", "I2", "I3"]), sorted(list(vars_in_box("I1"))))

        # diagonal
        self.assertEqual(sorted(["D4", "D5", "D6", "E4", "E5", "E6", "F4", "F5", "F6"]), sorted(list(vars_in_box("D4"))))
        self.assertEqual(sorted(["D4", "D5", "D6", "E4", "E5", "E6", "F4", "F5", "F6"]), sorted(list(vars_in_box("E5"))))
        self.assertEqual(sorted(["D4", "D5", "D6", "E4", "E5", "E6", "F4", "F5", "F6"]), sorted(list(vars_in_box("F6"))))

        self.assertEqual(sorted(["G7", "G8", "G9", "H7", "H8", "H9", "I7", "I8", "I9"]), sorted(list(vars_in_box("G7"))))
        self.assertEqual(sorted(["G7", "G8", "G9", "H7", "H8", "H9", "I7", "I8", "I9"]), sorted(list(vars_in_box("H8"))))
        self.assertEqual(sorted(["G7", "G8", "G9", "H7", "H8", "H9", "I7", "I8", "I9"]), sorted(list(vars_in_box("I9"))))
