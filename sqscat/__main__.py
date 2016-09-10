import argparse
import sys

import boto3

def main():
    if len(sys.argv) == 1:
        sys.argv.append('-h')

    NO_MESSAGE_EXIT_CODE = 2

    arg_parser = argparse.ArgumentParser(description="%(prog)s is a command-line tool for sending and receiving messages on Amazon SQS queues. It sends messages read from standard input and writes received messages to standard output so that it can be used in UNIX pipe workflows.")
    arg_parser.add_argument('--send', '-s', action='store_true', help="Send a message to the queue from standard input. If this option isn't specified then the program reads a message from the queue and writes it to standard output.")
    arg_parser.add_argument('--wait', '-w', action='store_true', help="When receiving a message from the queue this option makes the program wait (forever) for a message to be available. If this option is not specified then the program exits with a return code of %d and an explanatory message on the standard error output if there is no message available." % NO_MESSAGE_EXIT_CODE)
    arg_parser.add_argument('queuename', help="The name of the SQS queue to use. It must exist already.")
    args = arg_parser.parse_args()

    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=args.queuename)

    if args.send:
        queue.send_message(MessageBody=sys.stdin.read())
    else:
        while True:
            messages = queue.receive_messages(MaxNumberOfMessages=1, WaitTimeSeconds=20 if args.wait else 1)
            if len(messages) == 0:
                if args.wait:
                    continue
                else:
                    print("No message available", file=sys.stderr)
                    sys.exit(NO_MESSAGE_EXIT_CODE)
            break
        message = messages[0]
        sys.stdout.write(message.body)
        sys.stdout.close()
        message.delete()
