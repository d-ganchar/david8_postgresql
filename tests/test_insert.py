from david8.predicates import eq_c
from parameterized import parameterized

from david8_postgresql.on_conflict import do_nothing, do_select, do_update
from david8_postgresql.on_conflict import excluded as e
from david8_postgresql.protocols.sql import InsertProtocol
from tests.base_test import BaseTest


class TestInsert(BaseTest):
    @parameterized.expand([
        # do_nothing()
        (
            BaseTest.qb
            .insert()
            .into('t')
            .record({'id': 1, 'name': 'a'})
            .on_conflict(['id'], do_nothing()),
            'INSERT INTO t (id, name) VALUES (%(p1)s, %(p2)s) ON CONFLICT (id) DO NOTHING',
            {'p1': 1, 'p2': 'a'},
        ),
        (
            BaseTest.qb
            .insert()
            .into('t')
            .record({'id': 1, 'name': 'a'})
            .on_conflict(['id'], do_nothing())
            .returning('*'),
            'INSERT INTO t (id, name) VALUES (%(p1)s, %(p2)s) ON CONFLICT (id) DO NOTHING RETURNING *',
            {'p1': 1, 'p2': 'a'},
        ),
        (
            BaseTest.qb
            .insert()
            .into('t')
            .record({'id': 1, 'name': 'a'})
            .on_conflict(['id'], do_nothing(), [eq_c('col1', 'col2')]),
            'INSERT INTO t (id, name) VALUES (%(p1)s, %(p2)s) ON CONFLICT (id) WHERE col1 = col2 DO NOTHING',
            {'p1': 1, 'p2': 'a'},
        ),
        # do_select
        (
            BaseTest.qb
            .insert()
            .into('t')
            .record({'id': 1, 'name': 'a'})
            .on_conflict(['id'], do_select()),
            'INSERT INTO t (id, name) VALUES (%(p1)s, %(p2)s) ON CONFLICT (id) DO SELECT',
            {'p1': 1, 'p2': 'a'},
        ),
        (
            BaseTest.qb
            .insert()
            .into('t')
            .record({'id': 1, 'name': 'a'})
            .on_conflict(['id'], do_select())
            .returning('id', 'email'),
            'INSERT INTO t (id, name) VALUES (%(p1)s, %(p2)s) ON CONFLICT (id) DO SELECT RETURNING id, email',
            {'p1': 1, 'p2': 'a'},
        ),
        (
            BaseTest.qb
            .insert()
            .into('t')
            .record({'id': 1, 'name': 'a'})
            .on_conflict(['id'], do_select(), [eq_c('col1', 'col2')]),
            'INSERT INTO t (id, name) VALUES (%(p1)s, %(p2)s) ON CONFLICT (id) WHERE col1 = col2 DO SELECT',
            {'p1': 1, 'p2': 'a'},
        ),
        # do_update
        (
            BaseTest.qb
            .insert()
            .into('t')
            .record({'id': 1, 'name': 'a', 'val': 10})
            .on_conflict(
                ['id'],
                do_update({
                    'name': e('name'),
                    'val': e('val'),
                }),
                [eq_c('col1', 'col2')]
            ),
            'INSERT INTO t (id, name, val) VALUES (%(p1)s, %(p2)s, %(p3)s) ON CONFLICT (id) WHERE col1 = col2 '
            'DO UPDATE SET name = EXCLUDED.name, val = EXCLUDED.val',
            {'p1': 1, 'p2': 'a', 'p3': 10},
        ),
        (
            BaseTest.qb
            .insert()
            .into('t')
            .record({'id': 1, 'name': 'a', 'val': 10})
            .on_conflict(
                ['id'],
                do_update({
                    'name': e('name'),
                    'val': e('val'),
                })
            ),
            'INSERT INTO t (id, name, val) VALUES (%(p1)s, %(p2)s, %(p3)s) ON CONFLICT (id) DO UPDATE '
            'SET name = EXCLUDED.name, val = EXCLUDED.val',
            {'p1': 1, 'p2': 'a', 'p3': 10},
        ),
    ])
    def test_on_conflict(self, query: InsertProtocol, exp_sql: str, exp_params: dict):
        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual(query.get_parameters(), exp_params)

    @parameterized.expand([
        # do_nothing()
        (
            BaseTest.qb
            .insert()
            .into('users')
            .record({'email': 'name@test.com', 'name': 'david8'})
            .on_conflict_constraint('users_email_key', do_nothing()),
            'INSERT INTO users (email, name) VALUES (%(p1)s, %(p2)s) ON CONFLICT ON CONSTRAINT users_email_key'
            ' DO NOTHING',
            {'p1': 'name@test.com', 'p2': 'david8'},
        ),
        (
            BaseTest.qb
            .insert()
            .into('t')
            .record({'email': 'name@test.com', 'name': 'david8'})
            .on_conflict_constraint('users_email_key', do_nothing())
            .returning('*'),
            'INSERT INTO t (email, name) VALUES (%(p1)s, %(p2)s) ON CONFLICT ON CONSTRAINT users_email_key '
            'DO NOTHING RETURNING *',
            {'p1': 'name@test.com', 'p2': 'david8'},
        ),
        # do_select
        (
            BaseTest.qb
            .insert()
            .into('t')
            .record({'email': 'name@test.com', 'name': 'david8'})
            .on_conflict_constraint('users_email_key', do_select()),
            'INSERT INTO t (email, name) VALUES (%(p1)s, %(p2)s) ON CONFLICT ON CONSTRAINT users_email_key DO SELECT',
            {'p1': 'name@test.com', 'p2': 'david8'},
        ),
        (
            BaseTest.qb
            .insert()
            .into('t')
            .record({'email': 'name@test.com', 'name': 'david8'})
            .on_conflict_constraint('users_email_key', do_select())
            .returning('id', 'email'),
            'INSERT INTO t (email, name) VALUES (%(p1)s, %(p2)s) ON CONFLICT ON CONSTRAINT users_email_key DO '
            'SELECT RETURNING id, email',
            {'p1': 'name@test.com', 'p2': 'david8'},
        ),
        # do_update
        (
            BaseTest.qb
            .insert()
            .into('t')
            .record({'email': 'name@test.com', 'name': 'david8'})
            .on_conflict_constraint(
                'users_email_key',
                do_update({
                    'name': e('name'),
                    'val': e('val'),
                }),
            ),
            'INSERT INTO t (email, name) VALUES (%(p1)s, %(p2)s) ON CONFLICT ON CONSTRAINT users_email_key '
            'DO UPDATE SET name = EXCLUDED.name, val = EXCLUDED.val',
            {'p1': 'name@test.com', 'p2': 'david8'},
        ),
    ])
    def test_on_conflict_constraint(self, query: InsertProtocol, exp_sql: str, exp_params: dict):
        self.assertEqual(query.get_sql(), exp_sql)
        self.assertEqual(query.get_parameters(), exp_params)
