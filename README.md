Sendy.co API wrapper
==================

[![Build Status](https://travis-ci.org/volsor/sendy.svg?branch=master)](https://travis-ci.org/volsor/sendy)

Python wrapper for [sendy.co API](https://sendy.co/api)

## Installation

`pip install drf-orjson`

## Usage

```Python
from sendy import Sendy, SendyServerError, SendyAlreadySubscribed


sendy = Sendy('your-api_key', 'https://sendy-server-url')
try:
    sendy.subscribe('test@example.com', 'list-id')
except SendyServerError as e:
    print(f'Server error: {str(e)}')
except SendyAlreadySubscribed:
    print('Already subscribed')

status = sendy.get_subscription_status('test@example.com', 'list-id')

sendy.create_campaign(
    from_name='Your name',
    from_email='your-email@example.com',
    reply_to='no-reply@example.com',
    title='Title',
    subject='Subj',
    html_text='<h1>test</h1>',
    send_campaign=False
)

sendy.get_subscribers_count('list-id')

sendy.unsubscribe('test@example.com', 'list-id')

sendy.delete_subscriber('test@example.com', 'list-id')
```
