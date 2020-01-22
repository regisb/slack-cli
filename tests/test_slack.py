import unittest

from slackcli import slack


class SlackTests(unittest.TestCase):
    def test_parse_status(self):
        self.assertEqual(
            {"status_emoji": ":office:", "status_text": "In office"},
            slack.parse_status_update("/status :office: In office"),
        )
        self.assertEqual(
            None, slack.parse_status_update("/status At home"),
        )
        self.assertEqual(
            None, slack.parse_status_update("/status :office:"),
        )
        self.assertEqual(
            None, slack.parse_status_update("/status"),
        )
