import dataclasses

from david8.core.base_dml import BaseInsert, BaseUpdate, FullTableName
from david8.core.base_dql import BaseWhereConstruction
from david8.protocols.dialect import DialectProtocol
from david8.protocols.sql import PredicateProtocol

from ..protocols.sql import DoProtocol, InsertProtocol, UpdateProtocol


@dataclasses.dataclass(slots=True)
class Update(BaseUpdate, UpdateProtocol):
    returning_columns: tuple[str, ...] = dataclasses.field(default_factory=tuple)
    from_table_constr: FullTableName = dataclasses.field(default_factory=FullTableName)
    from_table_alias: str = ''

    def _from_table_to_sql(self, dialect: DialectProtocol) -> str:
        if not self.from_table_constr.table:
            return ''

        from_table = f' FROM {self.from_table_constr.get_sql(dialect)}'
        if self.from_table_alias:
            from_table = f'{from_table} AS {dialect.quote_ident(self.from_table_alias)}'

        return from_table

    def _get_sql(self, dialect: DialectProtocol) -> str:
        table = self._table_to_sql(dialect)
        set_columns = self._set_construction_to_sql(dialect)
        from_ = self._from_table_to_sql(dialect)
        where = self.where_construction.get_sql(dialect)
        if self.returning_columns:
            returning = f' RETURNING {", ".join(dialect.quote_ident(r) for r in self.returning_columns)}'
        else:
            returning = ''

        return f'UPDATE {table}{set_columns}{from_}{where}{returning}'

    def returning(self, *args: str) -> 'UpdateProtocol':
        self.returning_columns += args
        return self

    def from_table(self, table_name: str, alias: str = '', db_name: str = '') -> 'UpdateProtocol':
        self.from_table_constr.set_names(table_name, db_name)
        self.from_table_alias = alias
        return self


@dataclasses.dataclass
class Insert(BaseInsert, InsertProtocol):
    returning_columns: tuple[str, ...] = dataclasses.field(default_factory=tuple)
    on_conflict_columns: tuple[str, ...] | list[str] = dataclasses.field(default_factory=tuple)
    where_conflict: BaseWhereConstruction = dataclasses.field(default_factory=BaseWhereConstruction)
    do: DoProtocol | None = None
    on_conflict_constraint_key: str = ''

    def on_conflict(
        self,
        columns: list[str] | tuple[str, ...],
        do: DoProtocol,
        where: tuple[PredicateProtocol, ...] | list[PredicateProtocol] = None,
    ) -> 'InsertProtocol':
        self.on_conflict_columns = columns
        self.do = do
        if where:
            self.where_conflict.add_conditions(*where)
        return self

    def returning(self, *args: str) -> 'InsertProtocol':
        self.returning_columns = args
        return self

    def _render_on_conflict(self, dialect: DialectProtocol) -> str:
        if not self.on_conflict_columns:
            if self.on_conflict_constraint_key:
                return f' ON CONFLICT ON CONSTRAINT {self.on_conflict_constraint_key}'
            return ''

        return f' ON CONFLICT ({", ".join(dialect.quote_ident(c) for c in self.on_conflict_columns)})'

    def _render_do(self, dialect: DialectProtocol) -> str:
        if not self.do:
            return ''

        return f' {self.do.get_sql(dialect)}'

    def _render_returning(self, dialect: DialectProtocol) -> str:
        if not self.returning_columns:
            return ''

        return f' RETURNING {", ".join(dialect.quote_ident(c) for c in self.returning_columns)}'

    def on_conflict_constraint(self, name: str, do: DoProtocol) -> 'InsertProtocol':
        self.on_conflict_constraint_key = name
        self.do = do
        return self

    def _get_sql(self, dialect: DialectProtocol) -> str:
        sql = super()._get_sql(dialect)
        on_conflict = self._render_on_conflict(dialect)
        do = self._render_do(dialect)
        where = self.where_conflict.get_sql(dialect)
        returning = self._render_returning(dialect)

        return f'{sql}{on_conflict}{where}{do}{returning}'
