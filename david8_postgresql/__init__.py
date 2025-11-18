from david8.core.base_dialect import BaseDialect
from david8.param_styles import PyFormatParamStyle
from david8.protocols.dialect import ParamStyleProtocol


class PostgresqlDialect(BaseDialect):
    def __init__(self, param_style: ParamStyleProtocol = None, is_quote_mode: bool = False):
        super().__init__(param_style, is_quote_mode)
        self._is_quote_mode = is_quote_mode
        self._param_style = param_style or PyFormatParamStyle()
