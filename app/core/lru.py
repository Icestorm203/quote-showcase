from app.core.state import state


MAX_CACHE_SIZE = 10_000


def touch(quote_id: str):
    if quote_id not in state.quotes:
        return

    quote = state.quotes.pop(quote_id)

    state.quotes[quote_id] = quote


def evict_if_needed():
    while len(state.quotes) > MAX_CACHE_SIZE:
        state.quotes.popitem(last=False)

        state.stats.evictions += 1