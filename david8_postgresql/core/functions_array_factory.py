import dataclasses

from david8.core.fn_generator import FnCallableFactory, SeparatedArgsFn
from david8.protocols.sql import ExprProtocol, FunctionProtocol


@dataclasses.dataclass(slots=True)
class StrSeparatedArgsFnFactory(FnCallableFactory):
    separator: str = ', '

    def __call__(self, *args: str | ExprProtocol) -> FunctionProtocol:
        return SeparatedArgsFn(self.name, fn_items=args, separator=self.separator)
