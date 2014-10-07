"""
    Settings that doesn't change between different setups, ie mostly everything except secrets,
    database uris, etc.
"""
import os

from koosli.search_providers import bing

#=========================================
# Search Providers
#=========================================

#BING_API_KEY = '' # Fill in to use live bing search

SEARCH_PROVIDERS = {
    'bing': bing.BingMock,
    #'bing': bing.Bing,
}
