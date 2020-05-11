# Changelog

## v2.2.7 (2020-05-11)

- Support `/status clear` and extended status updates.
- Make it possible to run slack-cli without a writable configuration directory

## v2.2.6 (2020-01-22)

- Support status updates

## v2.2.4 (2019-02-17)

- Fix crash on receiving private group message

## v2.2.3 (2019-01-16)

- Properly identify bots
- Properly print bot messages

## v2.2.1 (2018-12-22)

- Colorized output
- Emojis!

## v2.1.2 (2018-12-21)

- CLI bash autocompletion
- Fix default token saving on team change

## v2.1.1 (2018-12-20)

- Correctly print user and channel names

## v2.1.0 (2018-12-07)

- Faster search/stream
- Stream from all channels (``-s all``)
- Send messages as a different user (``-u terminator``)

## v2.0.2 (2017-09-13)

- Better error management

## v2.0.1 (2017-09-09)

- Simplify reading from stdin

## v2.0.0 (2017-09-09)

- Add support for multiple teams
- Fix streaming issues
- Improve printed message format
- Simplify sending messages from stdin

## v1.0.3 (2017-09-04):

- Add "--last" flag to print an entire conversation

## v1.0.2 (2017-08-31):

- Fix token verification issue for users that don't have a "general" channel

## v1.0 (2017-07-06):

- Refactor command line by reducing all commands to a single "slack-cli" command.
- Interactive API token input.
- Automatic token creation check.
    
