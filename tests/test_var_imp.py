import unittest
from collections import deque
from xcodex.Util.var_imp import variables


class TestVariablesFunction(unittest.TestCase):
    def test_variables(self):
        # Call the function
        result = variables()

        # Check if the result is a tuple
        self.assertIsInstance(result, tuple)

        # Check if the length of the tuple is 12
        self.assertEqual(len(result), 12)

        # Check if the first 11 elements are deque instances
        for i in range(11):
            self.assertIsInstance(result[i], deque)

        # Check if the last element is a string
        self.assertIsInstance(result[11], str)


if __name__ == '__main__':
    unittest.main()