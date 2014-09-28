# -*- coding: utf-8 -*-

import string
import random
import os
import arrow

# Form validation
PASSWORD_LEN_MIN = 3
PASSWORD_LEN_MAX = 1024

# Model
STRING_LEN = 64


def get_current_time():
    # Must be a datetime object for database
    return arrow.utcnow().datetime

def pretty_date(time):
    return arrow.get(time).humanize()
