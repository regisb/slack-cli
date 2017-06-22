import subprocess
import sys

from . import stream
from . import utils


def main():
    sys.exit(run())

def run():
    parser = utils.get_parser("""Send, pipe, upload and receive Slack messages from the CLI""")
    parser.add_argument("-d", "--dst", action='append', help="Send message to a Slack channel, group or username")
    parser.add_argument("-s", "--src", action='append', help="Receive messages from a Slack channel, group or username")
    parser.add_argument("-f", "--file", help="Upload file")
    parser.add_argument("--pre", action="store_true", help="Send as verbatim `message`")
    parser.add_argument("--run", action="store_true",
                        help="Run the message as a shell command and send both the message and the command output")
    parser.add_argument("messages", nargs="*", help="Messages to send. Pass \"-\" to send content from stdin.")
    args, token = utils.parse_args(parser)

    # Debug command line arguments
    error_message = args_error_message(args)
    if error_message:
        sys.stderr.write(error_message)
        parser.print_help()
        return 1

    # Stream content
    if args.src:
        stream.receive(token, args.src)
        return 0

    # Send file
    if args.file:
        for dst in args.dst:
            upload_file(token, dst, args.file)
        return 0

    # Pipe content
    if args.messages == ["-"]:
        pipe(token, args.dst, pre=args.pre)
        return 0

    # Send messages
    for dst in args.dst:
        for message in args.messages:
            if args.run:
                run_command(token, dst, message)
            else:
                send_message(token, dst, message, pre=args.pre)
    return 0

def args_error_message(args):
    if args.dst and args.src:
        return "Incompatible arguments: --src and --dst\n"
    if not args.dst and not args.src:
        return "Invalid arguments: one of --src or --dst must be specified\n"
    if args.dst and not args.messages and not args.file:
        return "Invalid arguments: when using --dst, one of `messages` or --file must be specified\n"
    if args.src and args.file:
        return "Incompatible arguments: --src and --file\n"
    if args.file and args.messages:
        return "Incompatible arguments: `messages` and --file\n"

    return None

def pipe(token, destinations, pre=False):
    destination_ids = [utils.get_source_id(token, destination) for destination in destinations]
    chat = utils.ChatAsUser(token)
    for line in sys.stdin:
        line = line.strip()
        if line:
            for destination_id in destination_ids:
                chat.post_formatted_message(destination_id, line, pre=pre)

def run_command(token, destination, command):
    destination_id = utils.get_source_id(token, destination)
    command_result = subprocess.check_output(command, shell=True)
    message = "$ " + command + "\n" + command_result.decode("utf-8")
    utils.ChatAsUser(token).post_formatted_message(destination_id, message, pre=True)

def send_message(token, destination, message, pre=False):
    destination_id = utils.get_source_id(token, destination)
    utils.ChatAsUser(token).post_formatted_message(destination_id, message, pre=pre)

def upload_file(token, destination, path):
    destination_id = utils.get_source_id(token, destination)
    utils.upload_file(token, path, destination_id)
