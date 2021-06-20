from typing import Any
from flask.json import JSONEncoder

from main.domain.common.entities import Dto


class MongoJSONEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, Dto):
            return o.__dict__
        else:
            super().default(o)
