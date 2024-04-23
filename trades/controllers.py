from typing import Annotated

from fastapi import APIRouter, File, Depends
import psycopg2

from trades.config import Config
from trades.csv_parser import CsvParser
from trades.trade import Trade
from trades.trade_schema import TradeSchema
from trades.save_trades_use_case import SaveTradesUseCase
from trades.trade_repository import TradeRepository
from trades.db import db_connection

router = APIRouter()

@router.post(
    ""
)
async def load_trades(
    csv_trades: Annotated[bytes, File()],
    db_connection: Annotated[psycopg2.extensions.connection, Depends(db_connection)],
) -> None:
    csv_parser: CsvParser[TradeSchema] = CsvParser(TradeSchema)
    trade_schemas = csv_parser.from_stream(csv_trades)
    config = Config()
    trade_repository = TradeRepository(db_connection)
    save_trades_use_case = SaveTradesUseCase(trade_repository, config)
    save_trades_use_case.save(trade_schemas)

