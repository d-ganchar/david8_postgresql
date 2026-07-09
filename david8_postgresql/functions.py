from david8.core.fn_generator import SeparatedArgsFnFactory as _SeparatedArgsFnFactory

from .core.functions_array_factory import Col2AnyArgsFactory as _Col2AnyArgsFactory
from .core.functions_array_factory import Col3AnyArgsFactory as _Col3AnyArgsFactory
from .core.functions_array_factory import StrSeparatedArgsFactory as _StrSeparatedArgsFactory
from .core.functions_json_factory import (
    DelKeyFactory,
    ExtractFieldFactory,
    HasKeyFactory,
    JsonbSetFactory,
)

# json
extract_field = ExtractFieldFactory()
has_key = HasKeyFactory()
del_key = DelKeyFactory()
jsonb_set = JsonbSetFactory()

# string
concat = _SeparatedArgsFnFactory(name='concat', separator=' || ')

# array
unnest = _StrSeparatedArgsFactory(name='unnest')
array_remove = _Col2AnyArgsFactory(name='array_remove')
array_sample = _Col2AnyArgsFactory(name='array_sample')
array_replace = _Col3AnyArgsFactory(name='array_replace')
array_to_string = _Col3AnyArgsFactory(name='array_to_string')
