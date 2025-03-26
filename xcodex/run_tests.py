import unittest
import os


def run_all_tests():
    # Get the absolute path of the 'tests' directory
    start_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "xcodex",'tests'))

    # Discover all test files in the 'tests' directory
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=start_dir, pattern='test_*.py')

    # Run the tests with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return the result
    return result


if __name__ == '__main__':
    run_all_tests()
