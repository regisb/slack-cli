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
to the CLI (see below) or stored in an environment variable.

You may set ``SLACK_TOKEN`` in your ``~/.bashrc``::

    # ~/.bashrc
    export SLACK_TOKEN="slack_token_string"


Usage
=====

Send message to channel, group or user
--------------------------------------

Post to ``@general`` from stdin::

    date | slack-pipe -t slack_token general

In the following examples we assume the ``SLACK_TOKEN`` environment variable is
properly defined.

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

The ``slack-stream`` command was written to emulate the behaviour of ``tail
-f``::

    slack-stream general username groupname
