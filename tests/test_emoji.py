import unittest

from slackcli import emoji


class EmojiTests(unittest.TestCase):
    def test_emojize(self):
        self.assertEqual(
            "Merry christmas 🎄!", emoji.emojize("Merry christmas :christmas_tree:!")
        )
        self.assertEqual(
            "Merry christmas :🎄!", emoji.emojize("Merry christmas ::christmas_tree:!")
        )
        self.assertEqual(
            "::🎄 tricky stuff!", emoji.emojize(":::christmas_tree: tricky stuff!")
        )

    def test_emojize_verbatim_text(self):
        self.assertEqual(
            "`Merry christmas :christmas_tree:!`",
            emoji.emojize("`Merry christmas :christmas_tree:!`"),
        )

    def test_emojize_verbatim_block(self):
        self.assertEqual(
            "```Merry christmas :christmas_tree:!```",
            emoji.emojize("```Merry christmas :christmas_tree:!```"),
        )
        self.assertEqual(
            "```Merry christmas ` :christmas_tree:!```",
            emoji.emojize("```Merry christmas ` :christmas_tree:!```"),
        )

    def test_unified_to_unicode(self):
        self.assertEqual("🍺", emoji.unified_to_unicode("1F37A"))
        self.assertEqual("#️⃣", emoji.unified_to_unicode("0023-FE0F-20E3"))
        self.assertEqual("🎖️", emoji.unified_to_unicode("1F396-FE0F"))
