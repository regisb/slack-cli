import argparse
import subprocess
import sys

from . import errors
from . import slack
from . import stream
from . import token
from . import utils


def main():
    try:
        sys.exit(run())
    except errors.SourceDoesNotExistError as e:
        sys.stderr.write("Channel, group or user '{}' does not exist".format(e.args[0]))
        sys.exit(1)
    except errors.InvalidSlackToken as e:
        sys.stderr.write("Invalid Slack token: '{}'".format(e.args[0]))
        sys.exit(1)

def run():
    parser = argparse.ArgumentParser(description="""Send, pipe, upload and
                                     receive Slack messages from the CLI""")
    parser.add_argument("-t", "--token",
                        help="Explicitely specify Slack API token which will be saved to {}.".format(token.TOKEN_PATH))
    parser.add_argument("-T", "--team",
                        help="""Team domain to interact with. This is the name
                        that appears in the Slack url: https://xxx.slack.com.
                        Use this option to interact with different teams. If
                        unspecified, default to the team that was last
                        used.""")

    group_send = parser.add_argument_group("Send messages")
    group_send.add_argument("-d", "--dst", help="Send message to a Slack channel, group or username")
    group_send.add_argument("-f", "--file", help="Upload file")
    group_send.add_argument("--pre", action="store_true", help="Send as verbatim `message`")
    group_send.add_argument(
        "--run", action="store_true",
        help="""Run the message as a shell command and send both the message
        and the command output"""
    )
    group_send.add_argument(
        "-u", "--user",
        help="""Send message not as the current user, but as a bot with the
        specified user name"""
    )
    group_send.add_argument("messages", nargs="*",
                            help="""Messages to send (messages can also be sent
                            from standard input)""")

    group_receive = parser.add_argument_group("Receive messages")
    group_receive.add_argument("-s", "--src", action='append',
                               help="""Receive messages from a Slack channel,
                               group or username. This option can be specified
                               multiple times. When streaming, use 'all' to
                               stream from all sources.""")
    group_receive.add_argument("-l", "--last", type=int,
                               help="""Print the last N messages. If this option
                               is not specified, messages will be streamed from
                               the requested sources.""")

    args = parser.parse_args()
    slack.init(user_token=args.token, team=args.team)

    # Debug command line arguments
    error_message = args_error_message(args)
    if error_message:
        sys.stderr.write(error_message)
        parser.print_help()
        return 1

    # Stream content
    if args.src and args.last is None:
        stream.receive(args.src)
        return 0

    # Print last messages
    if args.src and args.last is not None:
        last_messages(args.src, args.last)
        return 0

    # Send file
    if args.file:
        upload_file(args.dst, args.file)
        return 0

    # Pipe content
    if not args.messages:
        pipe(args.dst, pre=args.pre, username=args.user)
        return 0

    # Send messages
    for message in args.messages:
        if args.run:
            run_command(args.dst, message, username=args.user)
        else:
            send_message(args.dst, message, pre=args.pre, username=args.user)
    return 0

# pylint: disable=too-many-return-statements
def args_error_message(args):
    if args.dst and args.src:
        return "Incompatible arguments: --src and --dst\n"
    if not args.dst and not args.src:
        return "Invalid arguments: one of --src or --dst must be specified\n"
    if args.dst and args.last:
        return "Incompatible arguments: --dst and --last\n"
    if args.src and args.file:
        return "Incompatible arguments: --src and --file\n"
    if args.file and args.messages:
        return "Incompatible arguments: `messages` and --file\n"

    return None

######### Receive

def last_messages(sources, count):
    for source in sources:
        utils.search_messages(source, count=count)

######### Send

def pipe(destination, pre=False, username=None):
    destination_id = utils.get_destination_id(destination)
    for line in sys.stdin:
        line = line.strip()
        if line:
            slack.post_message(destination_id, line, pre=pre, username=username)

def run_command(destination, command, username=None):
    destination_id = utils.get_destination_id(destination)
    command_result = subprocess.check_output(command, shell=True)
    message = "$ " + command + "\n" + command_result.decode("utf-8")
    slack.post_message(destination_id, message, pre=True, username=username)

def send_message(destination, message, pre=False, username=None):
    destination_id = utils.get_destination_id(destination)
    slack.post_message(destination_id, message, pre=pre, username=username)

def upload_file(destination, path):
    destination_id = utils.get_destination_id(destination)
    utils.upload_file(path, destination_id)
