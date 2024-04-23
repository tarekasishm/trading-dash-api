from __future__ import annotations
from datetime import datetime
from typing import Any
from enum import Enum

from trades.trade_schema import TradeSchema
from trades.config import Instrument

class MarketPosition(Enum):
    SHORT: str = "SHORT"
    LONG: str = "LONG"

    @classmethod
    def _missing_(cls, value: object) -> Any:
        if not isinstance(value, str):
            raise ValueError("Invalid market position")
        if value.upper() in MarketPosition:
            return MarketPosition(value.upper())
        raise ValueError("Invalid market position")

class Trade:
    def __init__(
        self,
        ticker: str,
        account: str,
        entry_time: datetime,
        market_position: MarketPosition,
        entry: float,
        exit: float,
        ticks_per_point: int,
        usd_per_point: int,
        commission: float,
    ) -> None:
        self._ticker = ticker
        self._account = account
        self._entry_time = entry_time
        self._market_position = market_position
        self._entry = entry
        self._exit = exit
        self._ticks_per_point = ticks_per_point
        self._usd_per_point = usd_per_point
        self._commision = commission

    @classmethod
    def from_trade_schema(cls, trade_schema: TradeSchema, instrument: Instrument) -> Trade:
        return Trade(
            trade_schema.ticker,
            trade_schema.account,
            trade_schema.entry_time,
            MarketPosition(trade_schema.market_position),
            trade_schema.entry,
            trade_schema.exit,
            instrument.ticks_per_point,
            instrument.tick_price * instrument.ticks_per_point,
            trade_schema.commission,
        )

    @property
    def ticker(self) -> str:
        return self._ticker
    
    @property
    def account(self) -> str:
        return self._account
    
    @property
    def entry_time(self) -> datetime:
        return self._entry_time

    @property
    def market_position(self) -> str:
        return self._market_position.value
    
    @property
    def entry_usd(self) -> float:
        return self._entry * self._usd_per_point
    
    @property
    def entry_points(self) -> float:
        return self._entry
    
    @property
    def entry_ticks(self) -> int:
        return int(self._entry * self._ticks_per_point)

    @property
    def exit_usd(self) -> float:
        return self._exit * self._usd_per_point
    
    @property
    def exit_points(self) -> float:
        return self._exit
    
    @property
    def exit_ticks(self) -> int:
        return int(self._exit * self._ticks_per_point)
    
    @property
    def commision(self) -> float:
        return self._commision
    
    @property
    def profit_usd(self) -> float:
        profit = self.exit_usd - self.entry_usd
        if self._market_position == MarketPosition.SHORT:
            profit *= -1
        return profit
    
    @property
    def profit_point(self) -> float:
        profit = self.exit_points - self.entry_points
        if self._market_position == MarketPosition.SHORT:
            profit *= -1
        return profit
    
    @property
    def profit_ticks(self) -> int:
        profit = self.exit_ticks - self.entry_ticks
        if self._market_position == MarketPosition.SHORT:
            profit *= -1
        return profit
