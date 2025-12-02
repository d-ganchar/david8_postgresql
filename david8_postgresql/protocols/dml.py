from david8.protocols.dml import UpdateProtocol as _UpdateProtocol


class UpdateProtocol(_UpdateProtocol):
    def returning(self, *args: str) -> 'UpdateProtocol':
        pass

    def from_table(self, table_name: str, alias: str = '', db_name: str = '') -> 'UpdateProtocol':
        pass
