import unittest
from unittest.mock import patch

from slackcli import messaging


class ParseStatusTests(unittest.TestCase):
    def test_parse_full_status(self):
        self.assertEqual(
            {"status_emoji": ":office:", "status_text": "In office"},
            messaging.parse_status_update("/status :office: In office"),
        )

    def test_parse_no_emoji_status(self):
        self.assertEqual(
            {"status_emoji": ":speech_balloon:", "status_text": "At home"},
            messaging.parse_status_update("/status At home"),
        )

    def test_parse_no_text_status(self):
        self.assertEqual(
            {"status_emoji": ":office:", "status_text": None},
            messaging.parse_status_update("/status :office:"),
        )

    def test_parse_empty_status(self):
        self.assertEqual(
            None, messaging.parse_status_update("/status"),
        )

    def test_parse_clear_status(self):
        self.assertEqual(
            {"status_emoji": None, "status_text": ""},
            messaging.parse_status_update("/status clear"),
        )


class FormatMessageTests(unittest.TestCase):
    @patch.object(messaging.names, "get_user_id", return_value="U024BE7LH")
    def test_format_outgoing_message(self, mock_user_id):
        self.assertEqual(
            "Hello <@U024BE7LH>, did you see my file?",
            messaging.format_outgoing_message(
                "Hello @loremipsum, did you see my file?"
            ),
        )
        mock_user_id.assert_called_with("loremipsum")
