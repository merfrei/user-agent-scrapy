"""
Setup for User Agent Scrapy
"""

from setuptools import setup


setup(name='user-agent-scrapy',
      version='1.0',
      description='Utilities to use User Agent Service with Scrapy',
      url='https://github.com/merfrei/user-agent-scrapy',
      author='Emiliano M. Rudenick',
      author_email='erude@merfrei.com',
      license='MIT',
      packages=['user_agent_scrapy'],
      install_requires=[
          'w3lib',
          'requests',
      ],
      zip_safe=False)
