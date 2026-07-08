import dataclasses

from david8.protocols.dialect import DialectProtocol
from david8.protocols.sql import ExprProtocol

from ..protocols.sql import DoProtocol


@dataclasses.dataclass(slots=True)
class Excluded(ExprProtocol):
    column: str

    def get_sql(self, dialect: DialectProtocol) -> str:
        return f'EXCLUDED.{dialect.quote_ident(self.column)}'


@dataclasses.dataclass(slots=True)
class DoSelect(DoProtocol):
    def get_sql(self, dialect: DialectProtocol) -> str:
        return 'DO SELECT'


@dataclasses.dataclass(slots=True)
class DoNothing(DoProtocol):
    def get_sql(self, dialect: DialectProtocol) -> str:
        return 'DO NOTHING'


@dataclasses.dataclass(slots=True)
class DoUpdate(DoProtocol):
    fields: dict[str, ExprProtocol] = dataclasses.field(default_factory=dict)

    def get_sql(self, dialect: DialectProtocol) -> str:
        fields = (f'{dialect.quote_ident(k)} = {v.get_sql(dialect)}' for k, v in  self.fields.items())
        return f'DO UPDATE SET {", ".join(fields)}'
