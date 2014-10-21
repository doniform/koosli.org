"""
    Settings that doesn't change between different setups, ie mostly everything except secrets,
    database uris, etc.
"""
import os

from koosli.search_providers import bing, yahoo

#=========================================
# Search Providers
#=========================================

#BING_API_KEY = '' # Fill in to use live bing search

YAHOO_CONSUMER_KEY = 'dj0yJmk9M2hXOEVSaG9VTVZIJmQ9WVdrOVVEVTNSWHB6TXpZbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD0xZQ--'

SEARCH_PROVIDERS = {
    'bing': bing.BingMock,
    #'bing': bing.Bing,
    'yahoo': yahoo.Yahoo,
}
