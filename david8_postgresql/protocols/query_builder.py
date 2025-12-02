from david8.protocols.query_builder import QueryBuilderProtocol as _QueryBuilderProtocol

from .dml import UpdateProtocol


class QueryBuilderProtocol(_QueryBuilderProtocol):
    def update(self) -> UpdateProtocol:
        pass
