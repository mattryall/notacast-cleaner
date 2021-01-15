#!/usr/bin/env python3

import base64
import os

import clean_notacast


def lambda_handler(event, context):
    token = None
    try:
        token = event['queryStringParameters']['auth']
    except (TypeError, KeyError):
        pass

    if not token:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'text/plain'},
            'body': 'Error - required parameter "auth" was missing.\n\n'
                    'Please provide a Patreon auth token, e.g. '
                    '"https://api.mattryall.net/notacast/notacast-clean.rss?auth=...".\n\n'
        }

    buf = clean_notacast.clean_feed(token)
    return {
        'statusCode': 200,
        'isBase64Encoded': True,
        'headers': {
            'Content-Type': 'application/rss+xml; charset=utf-8',
        },
        'body': base64.b64encode(buf.getvalue()).decode('utf-8'),
    }


# Can be run on the command line for testing - provide a PATREON_TOKEN env var
def main():
    event = {
        'queryStringParameters': {
            'auth': os.environ['PATREON_TOKEN'],
        }
    }
    result = lambda_handler(event, None)
    print(result)


if __name__ == '__main__':
    main()
