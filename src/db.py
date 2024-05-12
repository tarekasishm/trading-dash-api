import psycopg2

from typing import Generator

from src.config import Config

CREATE_TRADES_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS trades (
        time                TIMESTAMPTZ NOT NULL,
        ticker              VARCHAR(10),
        account             VARCHAR(50),
        market_position     VARCHAR(10),
        entry_usd           FLOAT,
        entry_points        FLOAT,
        entry_ticks         INTEGER,
        exit_usd            FLOAT,
        exit_points         FLOAT,
        exit_ticks          INTEGER,
        profit_usd          FLOAT,
        profit_points       FLOAT,
        profit_ticks        INTEGER,
        commission          FLOAT
    );
"""
CREATE_TRADE_HYPERTABLE = "SELECT create_hypertable('trades', by_range('time'));"
CREATE_PROFIT_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS net_profit(
        time                TIMESTAMPTZ NOT NULL,
        ticker              VARCHAR(10),
        account             VARCHAR(50),
        profit_usd          FLOAT,
        profit_points       FLOAT,
        profit_ticks        FLOAT              
    );
"""
CREATE_PROFIT_HYPERTABLE = "SELECT create_hypertable('net_profit', by_range('time'));"


CREATE_TABLE_QUERIES = [
    CREATE_PROFIT_TABLE_QUERY,
    CREATE_TRADES_TABLE_QUERY,
]
HYPERTABLE_QUERIES = [
    CREATE_TRADE_HYPERTABLE,
    CREATE_PROFIT_HYPERTABLE,
]

def migrate() -> None:
    config = Config()
    CONNECTION = (
        f"postgres://{config.database.user}:{config.database.password}@"
        f"{config.database.host}:{config.database.port}/postgres"
    )
    print(CONNECTION)
    with psycopg2.connect(CONNECTION) as connection:
        cursor = connection.cursor()
        [cursor.execute(query) for query in CREATE_TABLE_QUERIES]
        [cursor.execute(hypertable) for hypertable in HYPERTABLE_QUERIES]
        connection.commit()

def db_connection() -> Generator[psycopg2.extensions.connection, None, None]:
    config = Config()
    CONNECTION = (
        f"postgres://{config.database.user}:{config.database.password}@"
        f"{config.database.host}:{config.database.port}/{config.database.db_name}"
    )
    connection = psycopg2.connect(CONNECTION)
    yield connection
    connection.close()
