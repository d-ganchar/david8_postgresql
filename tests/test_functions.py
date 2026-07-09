from david8.expressions import param, val
from david8.protocols.sql import FunctionProtocol
from parameterized import parameterized

from david8_postgresql.functions import (
    array_remove,
    array_replace,
    array_sample,
    array_to_string,
    concat,
    del_key,
    extract_field,
    has_key,
    jsonb_set,
    unnest,
)
from tests.base_test import BaseTest


class TestFunctionsStr(BaseTest):
    @parameterized.expand([
        (
            concat('col1', 1, 'col2', 0.5, concat(val('static'), param(2))).as_('new_field'),
            "SELECT concat(col1 || '1' || col2 || '0.5' || concat('static' || %(p1)s)) AS new_field",
            'SELECT concat("col1" || \'1\' || "col2" || \'0.5\' || concat(\'static\' || %(p1)s)) AS "new_field"',
            {'p1': 2}
        ),
    ])
    def test_concat(self, fn: FunctionProtocol, exp_sql: str, exp_w_sql: str, exp_params: dict):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual(query.get_parameters(), exp_params)

        query = self.qb_w.select(fn)
        self.assertEqual(query.get_sql(), exp_w_sql)
        self.assertEqual(query.get_parameters(), exp_params)


class TestFunctionsJson(BaseTest):
    @parameterized.expand([
        (
            extract_field('meta', 'version', 'name'),
            "SELECT meta->'version'->'name'",
            "SELECT \"meta\"->'version'->'name'",
        ),
        (
            extract_field('meta', 'version', 'name'),
            "SELECT meta->'version'->'name'",
            "SELECT \"meta\"->'version'->'name'",
        ),
    ])
    def test_extract_field(self, fn: FunctionProtocol, exp_sql: str, exp_w_sql: str):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), exp_sql)

        query = self.qb_w.select(fn)
        self.assertEqual(query.get_sql(), exp_w_sql)

    @parameterized.expand([
        (
            has_key('meta', 'version'),
            "SELECT meta?'version'",
            "SELECT \"meta\"?'version'",
        ),
    ])
    def test_has_key(self, fn: FunctionProtocol, exp_sql: str, exp_w_sql: str):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), exp_sql)

        query = self.qb_w.select(fn)
        self.assertEqual(query.get_sql(), exp_w_sql)

    @parameterized.expand([
        (
            del_key('meta', 'version'),
            "SELECT meta-'version'",
            "SELECT \"meta\"-'version'",
        ),
    ])
    def test_del_key(self, fn: FunctionProtocol, exp_sql: str, exp_w_sql: str):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), exp_sql)

        query = self.qb_w.select(fn)
        self.assertEqual(query.get_sql(), exp_w_sql)

    @parameterized.expand([
        (
            jsonb_set('meta', ['version', 'name'], 'Xia'),
            "SELECT jsonb_set(meta, '{version,name}', '\"Xia\"'::jsonb)",
            'SELECT jsonb_set("meta", \'{version,name}\', \'"Xia"\'::jsonb)',
        ),
        (
            jsonb_set('meta', ['version', 'major'], 22),
            "SELECT jsonb_set(meta, '{version,major}', '22'::jsonb)",
            'SELECT jsonb_set("meta", \'{version,major}\', \'22\'::jsonb)',
        ),
        (
            jsonb_set('meta', ['version'], {'name': 'Xia', 'major': 22}),
            'SELECT jsonb_set(meta, \'{version}\', \'{"name": "Xia", "major": 22}\')',
            'SELECT jsonb_set("meta", \'{version}\', \'{"name": "Xia", "major": 22}\')',
        ),
    ])
    def test_jsonb_set(self, fn: FunctionProtocol, exp_sql: str, exp_w_sql: str):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), exp_sql)

        query = self.qb_w.select(fn)
        self.assertEqual(query.get_sql(), exp_w_sql)


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
        (
            array_remove('column1', 1),
            "SELECT array_remove(column1, 1)",
            "SELECT array_remove(\"column1\", 1)",
        ),
        (
            array_remove('column1', 0.5),
            "SELECT array_remove(column1, 0.5)",
            "SELECT array_remove(\"column1\", 0.5)",
        ),
        (
            array_remove('column1', 'Legacy'),
            "SELECT array_remove(column1, 'Legacy')",
            "SELECT array_remove(\"column1\", 'Legacy')",
        ),
        (
            array_replace('column1', 'Legacy', 'Fixed'),
            "SELECT array_replace(column1, 'Legacy', 'Fixed')",
            'SELECT array_replace("column1", \'Legacy\', \'Fixed\')',
        ),
        (
            array_replace('column1', -1, 0),
            "SELECT array_replace(column1, -1, 0)",
            'SELECT array_replace("column1", -1, 0)',
        ),
        (
            array_to_string('column_name', ',', '*'),
            "SELECT array_to_string(column_name, ',', '*')",
            'SELECT array_to_string("column_name", \',\', \'*\')',
        ),
        (
            array_sample('column_name', 3),
            "SELECT array_sample(column_name, 3)",
            'SELECT array_sample("column_name", 3)',
        ),
    ])
    def test_array_fn(self, fn: FunctionProtocol, exp_sql: str, exp_w_sql: str):
        query = self.qb.select(fn)
        self.assertEqual(query.get_sql(), exp_sql)

        query = self.qb_w.select(fn)
        self.assertEqual(query.get_sql(), exp_w_sql)
