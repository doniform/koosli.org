"""
    Settings that doesn't change between different setups, ie mostly everything except secrets,
    database uris, etc.
"""
import os

from koosli.search_providers import bing, yahoo

#=========================================
# Search Providers
#=========================================

YAHOO_CONSUMER_KEY = 'dj0yJmk9eDJ5bWYweThQNTl0JmQ9WVdrOVFtcFBjWGhMTm5VbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD0zZg--'

SEARCH_PROVIDERS = {
    'bing': bing.Bing,
    'yahoo': yahoo.Yahoo,
}
