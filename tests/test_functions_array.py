from david8.protocols.sql import FunctionProtocol
from parameterized import parameterized

from david8_postgresql.functions_array import unnest
from david8_postgresql.functions_str import concat
from tests.base_test import BaseTest


class TestFunctionsArray(BaseTest):

    @parameterized.expand([
        (
            unnest('column1', 'column2', 'column3'),
            'SELECT unnest(column1, column2, column3)',
            'SELECT unnest("column1", "column2", "column3")',
        ),
        (
            unnest(concat('column1', 'column2')),
            'SELECT unnest(concat(column1 || column2))',
            'SELECT unnest(concat("column1" || "column2"))',
        ),
    ])
    def test_unnest(self, fn: FunctionProtocol, exp_sql: str, exp_w_sql: str):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), exp_sql)

        query = self.qb_w.select(fn)
        self.assertEqual(query.get_sql(), exp_w_sql)
