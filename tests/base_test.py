import unittest

from david8 import get_qb

from david8_postgresql import PostgresqlDialect


class BaseTest(unittest.TestCase):
    maxDiff = 1500

    qb = get_qb(PostgresqlDialect())                      # without quotes
    qb_w = get_qb(PostgresqlDialect(is_quote_mode=True))  # with quotes
