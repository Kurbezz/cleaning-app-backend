from typing import TypeVar, Generic, Sequence, Protocol, Any, runtime_checkable
from dataclasses import asdict

from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.bases import AbstractParams


@runtime_checkable
class ToDict(Protocol):
    def dict(self) -> dict:
        ...


T = TypeVar("T", ToDict, Any)


class CustomPage(LimitOffsetPage[T], Generic[T]):
    @classmethod
    def create(
        cls,
        items: Sequence[T],
        total: int,
        params: AbstractParams,
    ) -> "CustomPage[T]":
        return cls(
            total=total,
            items=[item.dict() for item in items],
            **asdict(params.to_raw_params()),
        )
