import inspect

import pytest
from sendyapi import Sendy


def get_empty_args(f):
    n_args = len(inspect.signature(f).parameters)
    return ('',) * n_args


def get_url_for_method(method):
    return 'http://example.com' + {
        'subscribe': '/subscribe',
        'unsubscribe': '/unsubscribe',
        'delete_subscriber': '/api/subscribers/delete.php',
        'get_subscription_status': '/api/subscribers/subscription-status.php',
        'get_subscribers_count': '/api/subscribers/active-subscriber-count.php',
        'create_campaign': '/api/campaigns/create.php',
    }.get(method)


@pytest.fixture
def sendy():
    return Sendy('test-api-key', 'http://example.com', request_timeout=15)
