from urllib.parse import urljoin

import requests

from .exceptions import *


class Sendy:
    subscription_statuses = (
        'Subscribed',
        'Unsubscribed',
        'Unconfirmed',
        'Bounced',
        'Soft bounced',
        'Complained',
    )

    # 'method_name': (resource, success_value, need_auth)
    methods = {
        'subscribe': ('/subscribe', '1', False),
        'unsubscribe': ('/unsubscribe', '1', False),
        'delete_subscriber': ('/api/subscribers/delete.php', '1', True),
        'get_subscription_status': ('/api/subscribers/subscription-status.php', subscription_statuses, True),
        'get_subscribers_count': ('/api/subscribers/active-subscriber-count.php', int, True),
        'create_campaign': ('/api/campaigns/create.php', ('Campaign created', 'Campaign created and now sending'),
                            True),
    }

    _default_timeout = 10

    def __init__(self, api_key, url, request_timeout=None):
        self.api_key = api_key
        self.url = url
        self.timeout = request_timeout or self._default_timeout

    @staticmethod
    def _raise(response):
        if 'Already subscribed' in response:
            raise SendyAlreadySubscribed(response)
        elif 'Email does not exist in list' in response:
            raise SendyNotSubscribed(response)
        else:
            raise SendyException(response)

    def _validate_response(self, success_value, response):
        if type(success_value) is str and response != success_value:
            self._raise(response)
        elif hasattr(success_value, '__contains__') and response not in success_value:
            self._raise(response)
        elif callable(success_value):
            try:
                response = success_value(response)
            except ValueError:
                self._raise(response)
        return response

    def _get_url(self, resource):
        return urljoin(self.url, resource)

    def _make_request(self, method, params):
        resource, success_value, need_auth = self.methods.get(method)

        if need_auth:
            params['api_key'] = self.api_key

        try:
            response = requests.post(self._get_url(resource), data=params, timeout=self.timeout).text
        except requests.exceptions.RequestException as e:
            raise SendyServerError(str(e))

        return self._validate_response(success_value, response)

    def subscribe(self, email, list_id, name='', country='', ipaddress='', referrer='', gdpr=True, silent=True,
                  custom_fields=None):
        params = {
            'email': email,
            'list': list_id,
            'name': name,
            'country': country,
            'ipaddress': ipaddress,
            'referrer': referrer,
            'gdpr': gdpr,
            'silent': silent,
            'boolean': 'true',
        }

        if custom_fields:
            params.update(custom_fields)

        self._make_request('subscribe', params)

    def unsubscribe(self, email, list_id):
        params = {
            'email': email,
            'list': list_id,
            'boolean': 'true',
        }
        self._make_request('unsubscribe', params)

    def delete_subscriber(self, email, list_id):
        params = {
            'email': email,
            'list_id': list_id,
        }
        self._make_request('delete_subscriber', params)

    def get_subscription_status(self, email, list_id):
        params = {
            'email': email,
            'list_id': list_id,
        }
        return self._make_request('get_subscription_status', params)

    def get_subscribers_count(self, list_id):
        return self._make_request('get_subscribers_count', {'list_id': list_id})

    def create_campaign(self, from_name, from_email, reply_to, title, subject, html_text, send_campaign, plain_text='',
                        list_ids='', segment_ids='', exclude_list_ids='', exclude_segments_ids='', brand_id='',
                        query_string=''):
        params = {
            'from_name': from_name,
            'from_email': from_email,
            'reply_to': reply_to,
            'title': title,
            'subject': subject,
            'html_text': html_text,
            'plain_text': plain_text,
            'list_ids': list_ids,
            'segment_ids': segment_ids,
            'exclude_list_ids': exclude_list_ids,
            'exclude_segments_ids': exclude_segments_ids,
            'brand_id': brand_id,
            'query_string': query_string,
        }

        if type(send_campaign) is bool:
            send_campaign = '1' if send_campaign else '0'

        params['send_campaign'] = send_campaign

        self._make_request('create_campaign', params)
