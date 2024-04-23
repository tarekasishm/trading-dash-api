# type: ignore
# PEP 695 generics are not yet supported 
from io import StringIO
from pydantic import BaseModel

class CsvParser[T: BaseModel]: # type:ignore
    def __init__(self, base: type[T]):
        self._base = base

    def from_stream(self, stream: bytes, has_headers: bool = True) -> list[T]:
        csv_string = StringIO(stream.decode("utf-8"))
        if has_headers:
            next(csv_string)
        parsed: list[T] = []
        for csv_row in csv_string:
            row = csv_row.split(";")
            base_dict = {
                key: value for key, value in zip(self._base.model_fields, row)
            }
            parsed.append(self._base(**base_dict))
        return parsed

        