"""
Scrapy Downloader Middlewares
"""

import logging
import random

from scrapy import signals
from scrapy.downloadermiddlewares.useragent import \
    UserAgentMiddleware as ScrapyUserAgentMiddleware

from user_agent_scrapy.api import UserAgentAPI


logger = logging.getLogger(__name__)


class UserAgentAPIMiddlewareError(Exception):
    '''Something went wrong'''


class UserAgentMiddleware(ScrapyUserAgentMiddleware):
    '''
    REQUIRED
    Custom UserAgent Scrapy Middleware to use a different user agent per request
    The User Agent Middleware use the keep_session special meta key
    Also you should disable the default scrapy UserAgentMiddleware
    '''
    def process_request(self, request, spider):
        if not request.meta.get('keep_session', False):
            super().process_request(request, spider)


class UserAgentScrapyMiddleware:
    '''Main User Agent Service Middleware'''

    def __init__(self):
        self.user_agents = {}
        self.api_client = None

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        api_config = {}
        middleware.set_api_config_from_settings(crawler.settings, api_config)
        middleware.api_client = UserAgentAPI(**api_config)
        crawler.signals.connect(middleware.spider_opened, signals.spider_opened)
        return middleware

    @staticmethod
    def set_api_config_from_settings(settings, config: dict):
        '''Set the middleware config from settings.py'''
        config['api_url'] = settings.get('USER_AGENT_SERVICE_API_URL', '')
        config['api_key'] = settings.get('USER_AGENT_SERVICE_API_KEY', '')

    def spider_opened(self, spider):
        '''When the spider is opened check if the middleware is enabled and load the agents'''
        if self.is_enabled(spider):
            self.load_agents(spider)

    def spider_closed(self, spider):
        '''When the spiders is closed...'''
        if spider.name in self.user_agents:
            del self.user_agents[spider.name]

    def process_request(self, request, spider):
        '''Check if the middleware is enabled and if is there any agent available
        Replace the User-Agent header with the returned value.
        It uses random.choice to return a random agent on each request'''
        if self.is_enabled(spider, request):
            available_agents = self.user_agents.get(spider.name)
            if available_agents is not None:
                current_agent = random.choice(available_agents)
                request.headers['User-Agent'] = current_agent
                logger.info('Request to "%s" using agent "%s"', request.url, current_agent)

    @staticmethod
    def is_enabled(spider, request=None):
        '''Check if the middleware is enabled'''
        enabled = getattr(spider, 'ua_enabled', False)
        keep_session = False
        if request is not None:
            keep_session = request.meta.get('keep_session', keep_session)
        return enabled and not keep_session

    def load_agents(self, spider):
        '''Call the API and load the user agents'''
        api_filters = getattr(spider, 'ua_filters', {})
        self.user_agents[spider.name] = self.api_client.get_agent_strings(**api_filters)
