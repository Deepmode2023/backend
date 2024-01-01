from typing import Any

from pydantic_core import CoreSchema, core_schema
from pydantic import GetCoreSchemaHandler, TypeAdapter


class StrWithLimits(str):
    @classmethod
    def validate(cls, v):
        if len(v) > cls.limit:
            raise ValueError(
                f"Page length is longer than the specified limit {cls.limit}")

        return v

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(cls.validate))

    @classmethod
    def get_limmit_params(cls, limit):
        cls.limit = limit
