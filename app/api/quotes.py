from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.core.state import state
from app.core.memory import update_memory_stats
from app.core.lru import touch
from app.core.lru import evict_if_needed
from app.services.catalog_client import CatalogClient

import asyncio

router = APIRouter()

catalog_client = CatalogClient()


@router.get("/quotes/{quote_id}")
async def get_quote(quote_id: str):

    # удалённые редакцией
    if quote_id in state.deleted_ids:
        raise HTTPException(
            status_code=404,
            detail="not found"
        )

    # локальная запись
    quote = state.quotes.get(quote_id)

    if quote is not None:
        touch(quote_id)
        state.stats.served_local += 1

        return JSONResponse(
            content=quote,
            headers={
                "X-Source": "LOCAL"
            }
        )

    # каталог ещё не настроен
    if state.catalog_url is None:
        raise HTTPException(
            status_code=404,
            detail="not found"
        )

    lock = state.pending_requests.setdefault(
        quote_id,
        asyncio.Lock()
    )

    async with lock:

        quote = state.quotes.get(quote_id)

        if quote is not None:
            touch(quote_id)

            state.stats.served_local += 1

            return JSONResponse(
                content=quote,
                headers={
                    "X-Source": "LOCAL"
                }
            )

        state.stats.catalog_reads += 1

        response = await catalog_client.get_quote(
            state.catalog_url,
            quote_id
        )


    if response is None:
        raise HTTPException(
            status_code=503,
            detail="catalog unavailable"
        )

    # найдено в каталоге
    if response.status_code == 200:

        quote = response.json()

        state.quotes[quote_id] = quote

        evict_if_needed()

        update_memory_stats()

        state.stats.served_from_catalog += 1

        return JSONResponse(
            content=quote,
            headers={
                "X-Source": "CATALOG"
            }
        )

    # нет в каталоге
    if response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="not found"
        )

    # каталог занят
    if response.status_code == 503:
        raise HTTPException(
            status_code=503,
            detail="catalog busy"
        )

    raise HTTPException(
        status_code=500,
        detail="unexpected catalog response"
    )