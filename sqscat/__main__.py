import argparse
import sys

import boto3

def main():
    if len(sys.argv) == 1:
        sys.argv.append('-h')

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--send', '-s', action='store_true')
    arg_parser.add_argument('--wait', '-w', action='store_true')
    arg_parser.add_argument('queuename')
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
                    sys.exit(2)
            break
        message = messages[0]
        sys.stdout.write(message.body)
        sys.stdout.close()
        message.delete()
