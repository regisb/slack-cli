import hashlib
import os
import sys

# Code shamelessly stolen from different places
# https://github.com/sphinx-doc/sphinx/blob/master/sphinx/util/console.py
# https://github.com/django/django/blob/master/django/core/management/color.py
# https://askubuntu.com/questions/821157/print-a-256-color-test-pattern-in-the-terminal

class Colors:
    SLACK_PURPLE = 5
    LINK_BLUE = 27


def supports_color():
    """
    Returns True if the running system's terminal supports color, and False
    otherwise.
    """
    if 'SLACK_CLI_NO_COLOR' in os.environ:
        return False

    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or 'ANSICON' in os.environ)

    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    return supported_platform and is_a_tty

USE_COLORS = supports_color()
RESET_CODE = "\x1b[39;49;00m"

def color(fingerprint):
    if fingerprint == "general":
        return Colors.SLACK_PURPLE
    return int(hashlib.md5(fingerprint.encode()).hexdigest(), 16) % 256

def colorize(text, color_id, effect='normal'):
    if not USE_COLORS:
        return text
    effects = {
        'normal': '',
        'bold': '1;',
        'faint': '2;',
        'standout': '3;',
        'underline': '4;',
        'blink': '5;',
    }
    term_code = "\x1b[%s38;5;%dm" % (effects[effect], color_id)
    return term_code + text + RESET_CODE

def hyperlink(text):
    return colorize(text, Colors.LINK_BLUE, 'underline')
