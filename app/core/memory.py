import json

from app.core.state import state


def update_memory_stats():
    state.stats.local = len(state.quotes) - len(state.deleted_ids)

    state.stats.bytes = sum(
        len(
            json.dumps(
                quote,
                ensure_ascii=False
            ).encode("utf-8")
        )
        for quote in state.quotes.values()
    )