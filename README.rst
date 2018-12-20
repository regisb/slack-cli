=========
slack-cli
=========

Effectively interact with `Slack <https://slack.com/>`_ from the command line: send
messages, upload files, send command output, pipe content... all from the confort
of your terminal.

Member of dozens of Slack teams? No worries, `slack-cli` supports switching
easily from one team to another.

Quickstart
==========

::

    $ pip install slack-cli
    $ slack-cli -d general "Hello everyone!"


You will be asked to provide a Slack API token. It's easy, just get one from the
`API token generator <https://api.slack.com/custom-integrations/legacy-tokens>`_.

Usage
=====

::

    $ slack-cli -h
    usage: slack-cli [-h] [-t TOKEN] [-T TEAM] [-d DST] [-f FILE] [--pre] [--run]
                     [-u USER] [-s SRC] [-l LAST]
                     [messages [messages ...]]

    Send, pipe, upload and receive Slack messages from the CLI

    optional arguments:
      -h, --help            show this help message and exit
      -t TOKEN, --token TOKEN
                            Explicitely specify Slack API token which will be
                            saved to /home/user/.config/slack-cli/slack_token.
      -T TEAM, --team TEAM  Team domain to interact with. This is the name that
                            appears in the Slack url: https://xxx.slack.com. Use
                            this option to interact with different teams. If
                            unspecified, default to the team that was last used.

    Send messages:
      -d DST, --dst DST     Send message to a Slack channel, group or username
      -f FILE, --file FILE  Upload file
      --pre                 Send as verbatim `message`
      --run                 Run the message as a shell command and send both the
                            message and the command output
      -u USER, --user USER  Send message not as the current user, but as a bot
                            with the specified user name
      messages              Messages to send (messages can also be sent from
                            standard input)

    Receive messages:
      -s SRC, --src SRC     Receive messages from a Slack channel, group or
                            username. This option can be specified multiple times.
                            When streaming, use 'all' to stream from all sources.
      -l LAST, --last LAST  Print the last N messages. If this option is not
                            specified, messages will be streamed from the
                            requested sources.

Sending messages
----------------

The destination argument may be any user, group or channel::

    $ slack-cli -d general "Hello everyone!"
    $ slack-cli -d slackbot "Hello!"

Send message with a different username::

    $ slack-cli -d general -u terminator "I'll be back"

Pipe content from stdin
~~~~~~~~~~~~~~~~~~~~~~~

::

    $ cat /etc/hosts | slack-cli -d devteam

Usually you will want to format piped content as verbatim content with triple
backticks ("\`\`\`"). This is achieved with the `--pre` option::

    $ tail -f /var/log/nginx/access.log | slack-cli -d devteam --pre

Upload file
~~~~~~~~~~~

::

    $ slack-cli -f /etc/nginx/sites-available/default.conf -d alice

Run command and send output
~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
    
Receiving messages
------------------

Stream to stdout
~~~~~~~~~~~~~~~~

Stream the content of a channel::

    $ slack-cli -s general

Monitor all conversations::

    $ slack-cli -s all

Dump (backup) the content of a channel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    $ slack-cli -s general --last 10000 > general.log
    $ slack-cli -s myboss --last 10000 > covermyass.log

Authentication
--------------

Switch to a different team
~~~~~~~~~~~~~~~~~~~~~~~~~~

Switch to a different team anytime with the `-T` flag::

    $ slack-cli -T family -d general "I'll be home in an hour"

The new team will become the new default team.

Token management
~~~~~~~~~~~~~~~~

Note that the Slack token may optionally be stored in an environment variable (although it
is not recommended `for security reasons <https://unix.stackexchange.com/questions/369566/why-is-passing-the-secrets-via-environmental-variables-considered-extremely-ins>`_)::

    $ export SLACK_TOKEN="slack_token_string"

Bonus stuff ᕕ(⌐■_■)ᕗ ♪♬
-----------------------

Autocomplete
~~~~~~~~~~~~

Channel, group and user names can be autocompleted from the command line for `bash` users. Add the following line to `~/.bashrc`::

    eval "$(register-python-argcomplete slack-cli)"

Then, try autocompletion with::

    $ slack -s gene<tab>

or::
    
    $ slack -d <tab><tab>

Unfortunately, I did not manage to get autocompletion to work with `zsh` ¯\_( ͡° ͜ʖ ͡°)_/¯ Please let me know if you have more success.

Changelog
=========

v2.1.2 (2018-12-21)

- CLI bash autocompletion
- Fix default token saving on team change

v2.1.1 (2018-12-20)

- Correctly print user and channel names

v2.1.0 (2018-12-07)

- Faster search/stream
- Stream from all channels (`-s all`)
- Send messages as a different user (`-u terminator`)

v2.0.2 (2017-09-13)

- Better error management

v2.0.1 (2017-09-09)

- Simplify reading from stdin

v2.0.0 (2017-09-09)

- Add support for multiple teams
- Fix streaming issues
- Improve printed message format
- Simplify sending messages from stdin

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

Note that this project was initially a fork of `slacker-cli <https://github.com/juanpabloaj/slacker-cli/>`_
but the two projects have now considerably diverged.
