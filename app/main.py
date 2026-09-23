from fastapi import FastAPI

from app.api.catalog import router as catalog_router
from app.api.health import router as health_router
from app.api.quotes import router as quotes_router
from app.api.stats import router as stats_router

app = FastAPI(
    title="Quote Showcase",
    version="1.0.0"
)

app.include_router(health_router)
app.include_router(catalog_router)
app.include_router(quotes_router)
app.include_router(stats_router)