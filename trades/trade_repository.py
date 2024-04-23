import psycopg2

from trades.trade import Trade


class TradeRepository:
    INSERT_TEMPLATE: str = (
        "INSERT INTO trades ("
        "time, ticker, account, market_position, entry_usd, entry_points,"
        "entry_ticks, exit_usd, exit_points, exit_ticks, profit_usd, profit_points, profit_ticks, commission"
        ") VALUES ("
        "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s"
        ");"
    )
    def __init__(self, connection: psycopg2.extensions.connection) -> None:
        self._connection = connection

    def save(self, trade: Trade) -> None:
        data = (
            trade.entry_time, trade.ticker, trade.account, trade.market_position, trade.entry_usd, 
            trade.entry_points, trade.entry_ticks, trade.exit_usd, trade.exit_points, trade.exit_ticks,
            trade.profit_usd, trade.profit_point, trade.profit_ticks, trade.commision 
        )
        print(data)
        cursor = self._connection.cursor()
        cursor.execute(self.INSERT_TEMPLATE, data)
        self._connection.commit()
