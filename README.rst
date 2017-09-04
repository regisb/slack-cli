=========
slack-cli
=========

Interact with `Slack <https://slack.com/>`_ from the command line: send
messages, upload files, send command output, pipe content, all from the confort
of your terminal.

This was initially a fork of `slacker-cli <https://github.com/juanpabloaj/slacker-cli/>`_
but the two projects have now considerably diverged.

Install
=======

::

    $ pip install slack-cli


You should obtain an API token from Slack. To obtain a token, go to the
`API token generator <https://api.slack.com/custom-integrations/legacy-tokens>`_.

Usage
=====

::

    $ slack-cli -h
    usage: slack-cli [-h] [-t TOKEN] [-d DST] [-f FILE] [--pre] [--run] [-s SRC]
                     [-l LAST]
                     [messages [messages ...]]

    Send, pipe, upload and receive Slack messages from the CLI

    optional arguments:
      -h, --help            show this help message and exit
      -t TOKEN, --token TOKEN
                            Slack token which will be saved to /home/regis/.config
                            /slack-cli/slack_token. This argument only needs to be
                            specified once.

    Send messages:
      -d DST, --dst DST     Send message to a Slack channel, group or username
      -f FILE, --file FILE  Upload file
      --pre                 Send as verbatim `message`
      --run                 Run the message as a shell command and send both the
                            message and the command output
      messages              Messages to send. Pass "-" to send content from stdin.

    Receive messages:
      -s SRC, --src SRC     Receive messages from a Slack channel, group or
                            username
      -l LAST, --last LAST  Print the last N messages

Note that the Slack token may optionally be stored in an environment variable (although it
is not recommended `for security reasons <https://unix.stackexchange.com/questions/369566/why-is-passing-the-secrets-via-environmental-variables-considered-extremely-ins>`_)::

    $ export SLACK_TOKEN="slack_token_string"

Send message
------------

The destination argument may be any user, group or channel::

    $ slack-cli -d general "Hello everyone!"
    $ slack-cli -d slackbot "Hello!"


Pipe content
------------

::

    $ cat /etc/hosts | slack-cli -d devteam -

Usually you will want to format piped content as verbatim content with triple
backticks ("\`\`\`"). This is achieved with the `--pre` option::

    $ tail -f /var/log/nginx/access.log | slack-cli -d devteam --pre -

Upload file
-----------

::

    $ slack-cli -f /etc/nginx/sites-available/default.conf -d alice

Run command and send output
---------------------------

This is really convenient for showing both the result of a command and the
command itself::

    $ slack-cli -d john --run "git log -1"

will send to user `john`::

    $ git log -1
    commit 013798f5c85043d31f0221a9a32b39298e97fb08
    Author: Régis Behmo <regis@behmo.com>
    Date:   Thu Jun 22 15:20:36 2017 +0200

        Replace all commands by a single command
        
        Our first 1.0 release!
    

Stream content from a channel
-----------------------------

For monitoring a Slack channel from the terminal::

    $ slack-cli -s general

Dump (backup) the content of a channel
--------------------------------------

::

    $ slack-cli -s general --last 10000 > general.log
    $ slack-cli -s myboss --last 10000 > covermyass.log

Changelog
=========

v1.0.3 (2017-09-04):

- Add "--last" flag to print an entire conversation

v1.0.2 (2017-08-31):

- Fix token verification issue for users that don't have a "general" channel

v1.0 (2017-07-06):

- Refactor command line by reducing all commands to a single "slack-cli" command.
- Interactive API token input.
- Automatic token creation check.
    
Development
===========

I am very much open to comments! Please don't be afraid to `raise issues
<https://github.com/regisb/slack-cli/issues>`_ or `open pull requests
<https://github.com/regisb/slack-cli/pulls>`_.

This work is licensed under the terms of the `MIT License
<https://tldrlegal.com/license/mit-license>`_

TODO
----

- Support for multiple Slack teams
