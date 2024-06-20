from typing import Annotated, Any, Callable

from bson.objectid import ObjectId
from pydantic import BaseModel, Field, ConfigDict
from pydantic_core import core_schema


class _ObjectIdPydanticAnnotation:
    # Based on https://docs.pydantic.dev/latest/usage/types/custom/#handling-third-party-types.

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        def validate_from_str(input_value: str) -> ObjectId:
            return ObjectId(input_value)

        return core_schema.union_schema(
            [
                # check if it's an instance first before doing any further work
                core_schema.is_instance_schema(ObjectId),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ],
            serialization=core_schema.to_string_ser_schema(),
        )


PydanticObjectId = Annotated[ObjectId, _ObjectIdPydanticAnnotation]


class DbModel(BaseModel):
    id: PydanticObjectId = Field(alias="_id")

    model_config = ConfigDict(
        allow_population_by_field_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: lambda v: str(v)},
    )
