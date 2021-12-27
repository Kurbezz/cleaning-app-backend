from typing import Any, Generic, Protocol, Sequence, TypeVar, runtime_checkable

from fastapi_pagination import Page, Params
from fastapi_pagination.bases import AbstractParams


@runtime_checkable
class ToDict(Protocol):
    def dict(self) -> dict:
        ...


T = TypeVar("T", ToDict, Any)


class CustomPage(Page[T], Generic[T]):
    @classmethod
    def create(
        cls,
        items: Sequence[T],
        total: int,
        params: AbstractParams,
    ) -> "CustomPage[T]":
        if not isinstance(params, Params):
            raise ValueError("Page should be used with Params")

        return cls(
            total=total,
            items=[item.dict() for item in items],
            page=params.page,
            size=params.size,
        )
