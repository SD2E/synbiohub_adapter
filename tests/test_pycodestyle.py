import unittest
import os

# If this import fails, do `pip3 install [--user] pycodestyle`
import pycodestyle

# Please do not increase this number. Style warnings should DECREASE,
# not increase.
ALLOWED_ERRORS = 187

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
            'synbiohub_adapter/cache_query.py',
            'synbiohub_adapter/upload_sbol/__init__.py',
            'tests/DataGenerator.py',
            'tests/SBHRun_Environment.py',
            'tests/__init__.py',
            'tests/test_authentication.py',
            'tests/test_fallback_cache.py',
            'tests/test_pycodestyle.py',
            'tests/test_sbh_submissions.py',
            'tests/test_sbolquery.py'
        ]
        sg = pycodestyle.StyleGuide(quiet=QUIET,
                                    max_line_length=MAX_LINE_LENGTH,
                                    exclude=EXCLUDE)
        for f in dirs_and_files:
            report = sg.check_files([f])
            self.assertEqual(report.total_errors, 0,
                             msg='New style violation introduced in previously clean file {}'.format(f))

    def assert_warning_count(self, code, count, message):
        sg = pycodestyle.StyleGuide(quiet=QUIET,
                                    max_line_length=MAX_LINE_LENGTH,
                                    exclude=EXCLUDE,
                                    select=[code])
        report = sg.check_files('.')
        message = 'Too many "{} {}" style errors. Expected {}, found {}'.format(code, message,
                                                                                count, report.total_errors)
        self.assertEqual(report.total_errors, count, msg=message)

    def test_allowed_errors(self):
        self.assert_warning_count('E501', 174, "line too long")
        self.assert_warning_count('E722', 13, "do not use bare 'except'")

    def test_disallowed_errors(self):
        """All errors other than E501 and E722 should not appear in the code."""
        sg = pycodestyle.StyleGuide(quiet=QUIET,
                                    max_line_length=MAX_LINE_LENGTH,
                                    exclude=EXCLUDE,
                                    ignore=['E501', 'E722'])
        report = sg.check_files('.')
        self.assertEqual(report.total_errors, 0)


if __name__ == '__main__':
    unittest.main()
