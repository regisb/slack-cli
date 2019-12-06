import unittest

from slackcli import utils

class UtilsTests(unittest.TestCase):
    def test_format_outgoing_message(self):
        self.assertEqual("Hey <@U024BE7LH>, did you see my file?", utils.format_outgoing_message("Hello @loremipsum, did you see my file?"))
