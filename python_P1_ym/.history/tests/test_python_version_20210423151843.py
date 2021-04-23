
import sys
import unittest


class TestPythonVersion(unittest.TestCase):
    """Check that the Python version is >= 3.6."""

    def test_python_version_is_at_least_3_6(self):
        self.assertTrue(sys.version_info >= (3, 6),
                        msg="""Unsupported Python version.

    It looks like you're using a version of Python that's too old.
    This project requires Python 3.6+. You're currently using Python {}.{}.{}.

    Make sure that you have a compatible version of Python and that you're using
    `python3` at the command-line (or that your environment resolves `python` to
    some Python3.6+ version if you have a custom setup).

    Remember, you can always ask Python to display its version with:

        $ python3 -V
        Python 3.X.Y

    """.format(*sys.version_info[:3]))


if __name__ == '__main__':
    unittest.main()
