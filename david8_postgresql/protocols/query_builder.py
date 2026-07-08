from david8.protocols.query_builder import QueryBuilderProtocol as _QueryBuilderProtocol
from david8.protocols.sql import AliasedProtocol, ExprProtocol, FunctionProtocol

from .sql import InsertProtocol, SelectProtocol, UpdateProtocol


class QueryBuilderProtocol(_QueryBuilderProtocol):
    def update(self) -> UpdateProtocol: ...

    def select(self, *args: str | AliasedProtocol | ExprProtocol | FunctionProtocol) -> SelectProtocol: ...

    def insert(self) -> InsertProtocol: ...
