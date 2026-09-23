import asyncio
from collections import OrderedDict

from app.core.stats import Stats


class AppState:
    def __init__(self):
        self.catalog_url: str | None = None

        self.quotes = OrderedDict()

        self.deleted_ids: set[str] = set()

        self.pending_requests: dict[str, asyncio.Lock] = {}

        self.stats = Stats()


state = AppState()