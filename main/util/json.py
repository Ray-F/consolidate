from datetime import datetime, date
from typing import Any

from bson import ObjectId
from flask.json import JSONEncoder


class MongoJSONEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        if isinstance(o, ObjectId):
            return str(o)
        else:
            return super().default(o)
