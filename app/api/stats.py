from dataclasses import asdict

from fastapi import APIRouter

from app.core.state import state

router = APIRouter()


@router.get("/stats")
async def get_stats():
    state.stats.local = len(state.quotes)

    return asdict(state.stats)