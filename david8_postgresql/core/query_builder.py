from david8.core.base_query_builder import BaseQueryBuilder as _BaseQueryBuilder
from david8.protocols.dml import UpdateProtocol

from ..protocols.query_builder import QueryBuilderProtocol
from .dml import Update


class QueryBuilder(_BaseQueryBuilder, QueryBuilderProtocol):
    def update(self) -> UpdateProtocol:
        return Update(dialect=self._dialect)
