from unittest.mock import patch

import pytest
from sendyapi import SendyException

from .conftest import get_empty_args, get_url_for_method


def test_request_params(sendy):
    with patch('requests.post') as mock:
        mock.return_value.text = '1'
        sendy.subscribe('test@example.com', 'list1')
        mock.assert_called_once_with('http://example.com/subscribe', data={
            'email': 'test@example.com',
            'list': 'list1',
            'name': '',
            'country': '',
            'ipaddress': '',
            'referrer': '',
            'gdpr': 'true',
            'silent': 'true',
            'boolean': 'true',
            'api_key': 'test-api-key',
        }, timeout=15)


def test_sendy_exception(sendy):
    with patch('requests.post') as mock, pytest.raises(SendyException) as e:
        mock.return_value.text = 'Some error'
        sendy.subscribe('', '')
        assert str(e.value) == 'Sendy error: Some error'


@pytest.mark.parametrize(
    'method, response, expected',
    (
        ('subscribe', '1', None),
        ('subscribe', 'err', SendyException),
        ('unsubscribe', '1', None),
        ('unsubscribe', 'err', SendyException),
        ('delete_subscriber', '1', None),
        ('delete_subscriber', 'err', SendyException),
        ('get_subscription_status', 'Subscribed', 'Subscribed'),
        ('get_subscription_status', 'Unconfirmed', 'Unconfirmed'),
        ('get_subscription_status', 'err', SendyException),
        ('get_subscribers_count', '100', 100),
        ('get_subscribers_count', 'err', SendyException),
        ('create_campaign', 'Campaign created', None),
        ('create_campaign', 'err', SendyException),
    )
)
def test_api_methods(method, response, expected, sendy):
    with patch('requests.post') as mock:
        mock.return_value.text = response
        api_method = getattr(sendy, method)
        args = get_empty_args(api_method)
        if expected is SendyException:
            with pytest.raises(SendyException):
                api_method(*args)
        else:
            result = api_method(*args)
            assert result == expected
            assert mock.call_args[0][0] == get_url_for_method(method)
