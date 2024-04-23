from datetime import datetime

from pydantic import BaseModel, field_validator

from src.config import Instrument

class TradeSchema(BaseModel):
    trade_number: str
    ticker: str
    account: str
    strategy: str
    market_position: str
    qty: int
    entry: float
    exit: float
    entry_time: datetime
    exit_time: datetime
    entry_name: str
    exit_name: str
    profit: int
    cum_net_profit: int
    commission: float

    def entry_usd(self, instrument: Instrument) -> float:
        return self.entry * instrument.tick_price

    def entry_ticks(self, instrument: Instrument) -> int:
        return int(self.entry * instrument.ticks_per_point)    

    def exit_usd(self, instrument: Instrument) -> float:
        return self.exit * instrument.tick_price

    def exit_ticks(self, instrument: Instrument) -> int:
        return int(self.exit * instrument.ticks_per_point)
    
    def profit_ticks(self, instrument: Instrument) -> int:
        return self.exit_ticks(instrument) - self.entry_ticks(instrument)
    
    def profit_usd(self, instrument: Instrument) -> float:
        return self.profit_ticks(instrument) * instrument.tick_price 

    @field_validator("ticker")
    def tick_validator(cls, ticker: str) -> str:
        """Remove contract date"""
        return ticker.split(" ")[0]

    @field_validator("entry", mode="before")
    def entry_validator(cls, entry: str) -> float:
        return cls.replace_decimal(entry)
    
    @field_validator("exit", mode="before")
    def exit_validator(cls, exit: str) -> float:
        return cls.replace_decimal(exit)

    @field_validator("entry_time", mode="before")
    def entry_time_validator(cls, entry_time: str) -> datetime:
        return cls.date_formatter(entry_time)

    @field_validator("exit_time", mode="before")
    def exit_time_validator(cls, exit_time: str) -> datetime:
        return cls.date_formatter(exit_time)

    @field_validator("commission", mode="before")
    def commission_validator(cls, commission: str) -> float:
        return float(commission.replace(",", ".").removesuffix("$"))

    @staticmethod
    def date_formatter(date_str: str) -> datetime:
        return datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")

    @staticmethod
    def replace_decimal(value: str) -> float:
        return float(value.replace(",", "."))
