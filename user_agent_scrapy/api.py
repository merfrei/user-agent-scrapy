"""
User Agent API Client
"""

import requests
from w3lib.url import urljoin
from w3lib.url import add_or_replace_parameter


API_ENDPOINT = 'user_agents'


class UserAgentAPIError(Exception):
    '''Something went wrong'''


class UserAgentAPI:
    '''User Agent API Client to ask for a list of proxies'''

    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def get_agents(self, *, timeout=30, **filters):
        '''Get a list of user agent (objects)'''
        api_url = self.get_api_url(self.api_url, self.api_key, **filters)
        resp = requests.get(api_url, timeout=timeout)
        if resp.status_code != 200:
            raise UserAgentAPIError('API returned unexpected code {}'.format(resp.status_code))
        data = resp.json()
        return data['data']

    def get_agent_strings(self, *args, **kwargs):
        '''Get the list of user agents, only the strings'''
        return [agent['string'] for agent in self.get_agents(*args, **kwargs)]

    @staticmethod
    def get_api_url(api_url, api_key, **filters):
        '''Build the API URL to query a list of proxies'''
        api_url = urljoin(api_url, API_ENDPOINT)
        api_url = add_or_replace_parameter(api_url, 'api_key', api_key)
        for f_key, f_val in filters.items():
            api_url = add_or_replace_parameter(api_url, f_key, f_val)
        return api_url
