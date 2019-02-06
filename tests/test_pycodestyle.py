
import unittest

# If this import fails, do `pip3 install [--user] pycodestyle`
import pycodestyle

# Please do not increase this number. Style warnings should DECREASE,
# not increase.
ALLOWED_ERRORS = 2101

# Allow longer lines. The default is 79, which allows the 80th
# character to be a line continuation symbol. Here, we increase the
# line length to (effectively) 120.
MAX_LINE_LENGTH = 119

# List of files and directories to exclude from style checks
EXCLUDE = ['build']


class TestStyle(unittest.TestCase):

    def test_style(self):
        """Run pycodestyle on the directory tree."""
        # If there are files that don't have the '.py' extension, add
        # them to dirs_and_files to include them in the style checks.
        dirs_and_files = ['.']
        # Allow 120 character lines. The default is 80, but that's a
        # pretty narrow window size these days.
        sg = pycodestyle.StyleGuide(quiet=True,
                                    max_line_length=MAX_LINE_LENGTH,
                                    exclude=EXCLUDE)
        report = sg.check_files(dirs_and_files)
        self.assertEqual(report.total_errors, ALLOWED_ERRORS)

    def test_clean(self):
        """Ensure that warning free files stay that way.
        """
        # List all clean directories and files
        # Keep these sorted
        dirs_and_files = [
            'setup.py',
            'tests/__init__.py',
            'tests/test_pycodestyle.py'
        ]
        sg = pycodestyle.StyleGuide(quiet=True,
                                    max_line_length=MAX_LINE_LENGTH,
                                    exclude=EXCLUDE)
        report = sg.check_files(dirs_and_files)
        self.assertEqual(report.total_errors, 0)


if __name__ == '__main__':
    unittest.main()
