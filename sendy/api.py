import requests


class SendyException(Exception):

    def __init__(self, msg):
        self.msg = msg
        super().__init__()

    def __str__(self):
        return f'Sendy error: {self.msg}'


class Sendy:
    subscription_statuses = (
        'Subscribed',
        'Unsubscribed',
        'Unconfirmed',
        'Bounced',
        'Soft bounced',
        'Complained',
    )

    def __init__(self, api_key, url):
        self.api_key = api_key
        self.url = url.rstrip('/')

    def _make_request(self, resource, params, need_auth=True, success_value=None):
        if need_auth:
            params['api_key'] = self.api_key

        response = requests.post(f'{self.url}{resource}', data=params).text
        if type(success_value) is str and response != success_value:
            raise SendyException(response)
        elif hasattr(success_value, '__contains__') and response not in success_value:
            raise SendyException(response)
        elif callable(success_value):
            try:
                response = success_value(response)
            except ValueError:
                raise SendyException(response)

        return response

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

        self._make_request('/subscribe', params, False, '1')

    def unsubscribe(self, email, list_id):
        params = {
            'email': email,
            'list': list_id,
            'boolean': 'true',
        }
        self._make_request('/unsubscribe', params, False, '1')

    def delete_subscriber(self, email, list_id):
        params = {
            'email': email,
            'list_id': list_id,
        }
        self._make_request('/api/subscribers/delete.php', params, success_value='1')

    def get_subscription_status(self, email, list_id):
        params = {
            'email': email,
            'list_id': list_id,
        }
        return self._make_request('/api/subscribers/subscription-status.php', params,
                                  success_value=self.subscription_statuses)

    def get_subscribers_count(self, list_id):
        return self._make_request('/api/subscribers/active-subscriber-count.php', {'list_id': list_id},
                                  success_value=int)

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

        self._make_request('/api/campaigns/create.php', params,
                           success_value=('Campaign created', 'Campaign created and now sending'))
