=========
slack-cli
=========

Interact with `Slack <https://slack.com/>`_ from the command line.

This was initially a fork of https://github.com/juanpabloaj/slacker-cli/ but
the two projects have now considerably diverged.

Install
=======

::

    pip install slack-cli

Note that ``slack-cli`` is compatible with Python 2.7+ and Python 3.4+.

You should obtain an API token from Slack. This token can passed as an option
to the CLI (see below). To obtain a token, go to the [API token generator](https://api.slack.com/custom-integrations/legacy-tokens).

Alternatively, the token can be defined in an environment variable (although it
is not recommended [for security reasons](https://unix.stackexchange.com/questions/369566/why-is-passing-the-secrets-via-environmental-variables-considered-extremely-ins)):

    export SLACK_TOKEN="slack_token_string"

After the first use, the token will be stored in a local configuration file.

Usage
=====

Send message to channel, group or user
--------------------------------------

Check that everything is working fine::

    slack-send -t yourtoken "Hello!" slackbot

Slackbot should answer something nice :) After this first command, the slack
token will be saved to a local configuration file and you no longer have to
pass the `-t` argument on the command line. (see `slack-pipe -h` for more info)

Post to ``@general`` from stdin::

    date | slack-pipe general

Post to channel::

    slack-send "Hello world" general

Send message to user::

    date | slack-pipe username

Upload file to channel ``@random``::

    slack-upload lolcat.png random

Send non-formatted message to channel::

    cat main.py | slack-pipe general

Send the result of a command to John::

    slack-run "git status" john 

Stream content in real time
---------------------------

The ``slack-stream`` command was written to emulate the behaviour of ``tail -f``::

    slack-stream general username groupname
