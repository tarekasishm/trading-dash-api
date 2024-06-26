from trades.trade import Trade
from trades.trade_schema import TradeSchema
from trades.config import Instrument, Config
from trades.trade_repository import TradeRepository

class SaveTradesUseCase:
    def __init__(self, trade_repository: TradeRepository, config: Config) -> None:
        self._trade_repository = trade_repository
        self._config = config

    def save(self, trade_schemas: list[TradeSchema]) -> None:
        for trade_schema in trade_schemas:
            instrument = Instrument(**self._config.model_dump()[trade_schema.ticker])
            trade = Trade.from_trade_schema(trade_schema, instrument)
            self._trade_repository.save(trade)

