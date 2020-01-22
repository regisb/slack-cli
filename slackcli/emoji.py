# -*- coding: utf-8 -*-
import json
import os


USE_EMOJIS = "SLACK_CLI_NO_EMOJI" not in os.environ


class Emojis:
    ALL = {}
    JSON_PATH = os.path.join(os.path.dirname(__file__), "emoji.json")
    URL = "https://raw.githubusercontent.com/iamcal/emoji-data/master/emoji.json"

    @classmethod
    def get(cls, name, default=None):
        """
        Get the unicode associated to an emoji name.
        """
        if not cls.ALL:
            with open(cls.JSON_PATH) as f:
                cls.ALL = json.load(f)
        return cls.ALL.get(name, default)

    @classmethod
    def download(cls):
        """
        Download list of emojis with short names from iamcal/emoji-data github
        repository. This is the most comprehensive emoji list I've found. In
        particular, it includes slack-specific aliases, such as 'medal' or
        ':medical_symbol:'.

        The following code works only in python 3. Users should not have to run it.
        I only use this when I need to update the emoji list in the slack-cli
        repository.
        """
        import urllib.request

        emojis = json.loads(urllib.request.urlopen(cls.URL).read())
        emoji_names = {}
        for emoji in emojis:
            utf8 = unified_to_unicode(emoji["unified"])
            for name in emoji["short_names"]:
                emoji_names[name] = utf8

        with open(cls.JSON_PATH, "w") as f:
            json.dump(emoji_names, f, sort_keys=True, indent=2)


def emojize(text):
    """
    Replace the :short_codes: with their corresponding unicode values. Avoid
    replacing short codes inside verbatim tick (`) marks.
    """
    if not USE_EMOJIS:
        return text

    pos = 0
    result = ""
    verbatim = False
    verbatim_block = False
    while pos < len(text):
        chunk = text[pos]
        if text[pos] == "`":
            if text[pos + 1 : pos + 3] == "``":
                verbatim_block = not verbatim_block
            if not verbatim_block:
                verbatim = not verbatim
        if text[pos] == ":" and not verbatim and not verbatim_block:
            end_pos = text.find(":", pos + 1)
            if end_pos > pos + 1:
                emoji = Emojis.get(text[pos + 1 : end_pos])
                if emoji:
                    chunk = emoji
                    pos = end_pos
        result += chunk
        pos += 1
    return result


def unified_to_unicode(unified):
    """
    Convert unified codes to unicode, such as "0023-FE0F-20E3" to #️⃣.
    """
    binary = b""
    for part in unified.split("-"):
        if len(part) == 4:
            prefix = b"\u"
        elif len(part) == 5:
            prefix = b"\U000"
        else:
            raise ValueError("ERROR:" + unified)
        binary += prefix + part.encode()
    return binary.decode("unicode_escape")
