from typing import Any
from bson import ObjectId
from pydantic_core import core_schema


class PyObjectId(ObjectId):

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler,
    ) -> core_schema.CoreSchema:

        def validate(value: str | ObjectId) -> ObjectId:
            if isinstance(value, ObjectId):
                return value

            if not ObjectId.is_valid(value):
                raise ValueError("Invalid ObjectId")

            return ObjectId(value)

        return core_schema.no_info_plain_validator_function(
            validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                str,
                return_schema=core_schema.str_schema(),
            ),
        )