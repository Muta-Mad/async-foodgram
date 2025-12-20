from fastapi import Query, Request
from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from settings import settings


class Paginator:
    def __init__(
        self, 
        request: Request,
        page: int = Query(1, ge=1), 
        limit: int = Query(settings.pagination.page_size, ge=1)
    ):
        self.request = request
        self.page = page
        self.limit = limit

    async def get_paginate(
        self, 
        session: AsyncSession, 
        model: type, 
        base_query: Select | None = None
    ) -> dict:
        if base_query is None:
            base_query = select(model)
        count_query = select(func.count()).select_from(model)
        total_count: int = (await session.execute(count_query)).scalar() or 0
        offset = (self.page - 1) * self.limit
        results_query = base_query.offset(offset).limit(self.limit)
        result = await session.execute(results_query)
        items = result.scalars().all()
        base_url = str(self.request.url).split('?')[0]
        
        def create_url(p: int):
            return f'{base_url}?page={p}&limit={self.limit}'
        next_url = create_url(self.page + 1) if offset + self.limit < total_count else None
        prev_url = create_url(self.page - 1) if self.page > 1 else None
        return {
            'count': total_count,
            'next': next_url,
            'previous': prev_url,
            'results': items
        }