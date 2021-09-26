from typing import Any, Mapping, cast

from district42 import Props, SchemaVisitor
from district42 import SchemaVisitorReturnType as ReturnType
from district42 import schema
from district42.types import AnySchema, Schema
from district42_exp_types.ci_multi_dict import CIMultiDictSchema
from district42_exp_types.multi_dict import MultiDictSchema
from niltype import Nil, Nilable

__all__ = ("HistoryRequestSchema", "HistoryRequestProps",)


class HistoryRequestProps(Props):
    def __init__(self, registry: Nilable[Mapping[str, Any]] = Nil) -> None:
        if registry is Nil:
            registry = {}
        registry["method"] = registry.get("method", schema.str)
        registry["path"] = registry.get("path", schema.str)
        registry["params"] = registry.get("params", MultiDictSchema())
        registry["headers"] = registry.get("headers", CIMultiDictSchema())
        registry["body"] = registry.get("body", schema.any)
        super().__init__(registry)

    @property
    def method(self) -> Nilable[str]:
        return self.get("method")

    @property
    def path(self) -> Nilable[str]:
        return self.get("path")

    @property
    def params(self) -> Nilable[MultiDictSchema]:
        return self.get("params")

    @property
    def headers(self) -> Nilable[CIMultiDictSchema]:
        return self.get("headers")

    @property
    def body(self) -> Nilable[AnySchema]:
        return self.get("body")


class HistoryRequestSchema(Schema[HistoryRequestProps]):
    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        return cast(ReturnType, visitor.visit_jj_history_request(self, **kwargs))
