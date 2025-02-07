from __future__ import annotations

from typing import Any, Generic, TypeVar, List, Optional, Sequence
from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractPage, AbstractParams

T = TypeVar("T")


class PageResponse(AbstractPage[T], Generic[T]):
    total: int
    page: int
    page_size: int
    num_pages: int
    page_range: List[int]
    items: List[T]
    first_page: Optional[str]
    previous_page: Optional[str]
    next_page: Optional[str]
    last_page: Optional[str]

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        params: AbstractParams,
        *,
        total: Optional[int] = None,
        **kwargs: Any,
    ) -> PageResponse[T]:
        if not isinstance(params, Params):
            raise ValueError("params must be an instance of Params")

        if total is None:
            raise ValueError("total must be provided")

        page = params.page
        page_size = params.size
        num_pages = (total // page_size) + (1 if total % page_size > 0 else 0)
        page_range = list(range(1, num_pages + 1))

        base_url = kwargs.get("base_url", "")
        first_page = str(base_url.include_query_params(page=1, size=page_size))
        last_page = str(base_url.include_query_params(page=num_pages, size=page_size))
        previous_page = (
            str(base_url.include_query_params(page=page - 1, size=page_size))
            if page > 1
            else None
        )
        next_page = (
            str(base_url.include_query_params(page=page + 1, size=page_size))
            if page < num_pages
            else None
        )

        return cls(
            total=total,
            page=page,
            page_size=page_size,
            num_pages=num_pages,
            page_range=page_range,
            items=list(items),
            first_page=first_page,
            previous_page=previous_page,
            next_page=next_page,
            last_page=last_page,
        )
