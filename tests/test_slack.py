import unittest

from slackcli import slack


class SlackTests(unittest.TestCase):
    def test_parse_full_status(self):
        self.assertEqual(
            {"status_emoji": ":office:", "status_text": "In office"},
            slack.parse_status_update("/status :office: In office"),
        )

    def test_parse_no_emoji_status(self):
        self.assertEqual(
            {"status_emoji": ":speech_balloon:", "status_text": "At home"},
            slack.parse_status_update("/status At home"),
        )

    def test_parse_no_text_status(self):
        self.assertEqual(
            {"status_emoji": ":office:", "status_text": None},
            slack.parse_status_update("/status :office:"),
        )

    def test_parse_empty_status(self):
        self.assertEqual(
            None, slack.parse_status_update("/status"),
        )

    def test_parse_clear_status(self):
        self.assertEqual(
            {"status_emoji": None, "status_text": ""},
            slack.parse_status_update("/status clear"),
        )
