from david8.protocols.sql import ExprProtocol

from .core.do import DoNothing as _DoNothing
from .core.do import DoSelect as _DoSelect
from .core.do import DoUpdate as _DoUpdate
from .core.do import Excluded as _Excluded
from .protocols.sql import DoProtocol


def do_select() -> DoProtocol:
    return _DoSelect()


def do_nothing() -> DoProtocol:
    return _DoNothing()


def do_update(fields: dict[str, ExprProtocol]) -> DoProtocol:
    return _DoUpdate(fields)


def excluded(field: str) -> ExprProtocol:
    return _Excluded(field)
