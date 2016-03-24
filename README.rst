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

Post to channel from stdin::

    date | slack-send -c slack_channel -t slack_token

In the following examples we assume the ``SLACK_TOKEN`` environment variable is
properly defined.

Post to channel::

    slack-send -c slack_channel -m "Hello world"

Send message to user::

    date | slack-send -u user_name

Upload file to channel::

    slack-send -c slack_channel -f image.png

Upload file to group::

    slack-send -g slack_group -f image.png

Send non-formatted message to channel::

    cat main.py | slack-send -c general --pre

Stream content in real time
---------------------------

The ``slack-stream`` command was written to emulate the behaviour of ``tail
-f``::

    slack-stream general username groupname
