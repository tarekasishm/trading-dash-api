from fastapi import FastAPI

from contextlib import asynccontextmanager

from src.controllers import router
from src.db import migrate

@asynccontextmanager
async def lifespan(app: FastAPI):
    migrate()
    yield

app = FastAPI(
    title="Trading Dash API",
    version="0.0.1",
    lifespan=lifespan
)

app.include_router(router, prefix="/trades")



# SELECT time_bucket('1 day', "time") as day, SUM(profit_usd) FROM trades GROUP BY day order by day LIMIT 50;

