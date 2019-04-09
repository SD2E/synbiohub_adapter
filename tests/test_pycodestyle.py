import unittest
import os

# If this import fails, do `pip3 install [--user] pycodestyle`
import pycodestyle

# Please do not increase this number. Style warnings should DECREASE,
# not increase.
ALLOWED_ERRORS = 366

# Allow longer lines. The default is 79, which allows the 80th
# character to be a line continuation symbol. Here, we increase the
# line length to (effectively) 120.
MAX_LINE_LENGTH = 119

# List of files and directories to exclude from style checks
EXCLUDE = ['build']

# Report custom failure messages instead of default assertion errors
unittest.TestCase.longMessage = False

# Verbose option will explicitly print all style failures
if 'VERBOSE' in os.environ.keys():
    QUIET = not os.environ['VERBOSE']
else:
    QUIET = True


class TestStyle(unittest.TestCase):

    def test_style(self):
        """Run pycodestyle on the directory tree."""
        # If there are files that don't have the '.py' extension, add
        # them to dirs_and_files to include them in the style checks.
        dirs_and_files = ['.']
        # Allow 120 character lines. The default is 80, but that's a
        # pretty narrow window size these days.
        sg = pycodestyle.StyleGuide(quiet=QUIET,
                                    max_line_length=MAX_LINE_LENGTH,
                                    exclude=EXCLUDE)
        report = sg.check_files(dirs_and_files)
        self.assertEqual(report.total_errors, ALLOWED_ERRORS,
                         msg='{0} style violations were found. Expected {1}'.format(report.total_errors,
                                                                                    ALLOWED_ERRORS))

    def test_clean(self):
        """Ensure that warning free files stay that way.
        """
        # List all clean directories and files
        # Keep these sorted
        dirs_and_files = [
            'setup.py',
            'synbiohub_adapter/__init__.py',
            'tests/__init__.py',
            'tests/test_pycodestyle.py'
        ]
        sg = pycodestyle.StyleGuide(quiet=QUIET,
                                    max_line_length=MAX_LINE_LENGTH,
                                    exclude=EXCLUDE)
        for f in dirs_and_files:
            report = sg.check_files([f])
            self.assertEqual(report.total_errors, 0,
                             msg='New style violation introduced in previously clean file {}'.format(f))

    def assert_clean_report(self, code, message):
        """Verify that no erros of the given pycodestyle code exist in the
        codebase.

        """
        dirs_and_files = ['.']
        sg = pycodestyle.StyleGuide(quiet=QUIET,
                                    max_line_length=MAX_LINE_LENGTH,
                                    exclude=EXCLUDE,
                                    select=[code])
        report = sg.check_files(dirs_and_files)
        self.assertEqual(report.total_errors, 0,
                         msg=message)

    def test_indentation(self):
        self.assert_clean_report('E1', "Indentation style errors ('E1xx') exist")

    def test_whitespace(self):
        self.assert_clean_report('E202', "whitespace before ')'")
        self.assert_clean_report('E203', "whitespace before ':'")
        self.assert_clean_report('E225', "missing whitespace around operator")
        self.assert_clean_report('E226', "missing whitespace around arithmetic operator")
        self.assert_clean_report('E251', "unexpected spaces around keyword / parameter equals")
        self.assert_clean_report('E261', "at least two spaces before inline comment")
        self.assert_clean_report('E271', "multiple spaces after keyword")

    def test_blank_line(self):
        self.assert_clean_report('E301', "expected 1 blank line, found 0")
        self.assert_clean_report('E303', "too many blank lines (2)")
        self.assert_clean_report('E305', "expected 2 blank lines after class or function definition, found 1")

    def test_import(self):
        self.assert_clean_report('E4', "Import style errors ('E4*') exist")

    def test_statement(self):
        self.assert_clean_report('E711', "comparison to None should be 'if cond is not None:'")
        self.assert_clean_report('E713', "test for membership should be 'not in'")

    def test_all_warnings(self):
        self.assert_clean_report('W', "Style warnings ('W*') exists")


if __name__ == '__main__':
    unittest.main()
