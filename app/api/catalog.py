from fastapi import APIRouter
from fastapi import HTTPException

from app.core.state import state
from app.core.memory import update_memory_stats
from app.core.lru import evict_if_needed
from app.models.requests import (
    CatalogSourceRequest,
    ImportRequest,
    QuoteUpdateRequest,
)


router = APIRouter()

@router.post("/catalog/source")
async def set_catalog_source(
        payload: CatalogSourceRequest
):
    state.catalog_url = str(payload.url).rstrip("/")

    return {
        "source": state.catalog_url
    }

@router.post("/import")
async def import_catalog(
        payload: ImportRequest
):
    old_ids = set(state.quotes.keys())

    state.quotes = {}

    imported = 0

    for quote in payload.quotes:
        if "id" not in quote:
            continue
        
        quote_id = quote["id"]

        state.quotes[quote_id] = quote

        evict_if_needed()

        imported += 1

    new_ids = set(state.quotes.keys())

    dropped = len(old_ids - new_ids)

    state.deleted_ids.clear()

    state.stats.catalog = imported
    state.stats.local = len(state.quotes) - len(state.deleted_ids)

    update_memory_stats()

    return {
        "imported": imported,
        "dropped": dropped
    }


@router.put("/catalog/{quote_id}")
async def update_quote(
        quote_id: str,
        payload: QuoteUpdateRequest
):
    quote = {
        "id": quote_id,
        "author": payload.author,
        "text": payload.text
    }

    state.quotes[quote_id] = quote
    evict_if_needed()
    state.deleted_ids.discard(quote_id)

    update_memory_stats()
    
    return quote


@router.delete("/catalog/{quote_id}")
async def delete_quote(
        quote_id: str
):
    if quote_id not in state.quotes:
        raise HTTPException(
            status_code=404,
            detail="not found"
        )

    state.deleted_ids.add(quote_id)

    update_memory_stats()

    return {
        "deleted": True
    }


