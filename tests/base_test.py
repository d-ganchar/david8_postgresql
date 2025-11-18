import unittest

from david8_postgresql import get_qb


class BaseTest(unittest.TestCase):
    maxDiff = 1500

    qb = get_qb()                      # without quotes
    qb_w = get_qb(is_quote_mode=True)  # with quotes
