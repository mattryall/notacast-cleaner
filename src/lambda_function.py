#!/usr/bin/env python3

import base64
import os
from urllib.error import HTTPError

import clean_notacast


def lambda_handler(event, context):
    token = None
    try:
        token = event['queryStringParameters']['auth']
    except (TypeError, KeyError):
        pass  # fall through to token check below

    if not token:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'text/plain'},
            'body': 'Error - required parameter "auth" was missing.\n\n'
                    'Please provide a Patreon auth token, e.g. '
                    '"https://api.mattryall.net/notacast/notacast-clean.rss?auth=...".\n\n'
        }

    try:
        buf = clean_notacast.clean_feed(token)
    except HTTPError as e:
        return {
            'statusCode': e.code,
            'headers': {'Content-Type': 'text/plain'},
            'body': f'Error retrieving feed: {type(e).__name__} {e.code} {e.reason}\n\n'
                    f'URL: {e.url}\n\n'
                    f'Please check your auth token is correct, and you have a valid '
                    f'NotACast subscription on Patreon.\n\n'
        }

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
