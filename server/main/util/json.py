from typing import Any
from flask.json import JSONEncoder

from main.domain.common.entities import Dto


class DtoJsonEncoder(JSONEncoder):
    """
    Encoding for accepting Domain Transfer Objects.
    """

    def default(self, o: Any) -> Any:
        if isinstance(o, Dto):
            return o.__dict__
        else:
            super().default(o)
