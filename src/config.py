from typing import Type

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    TomlConfigSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

class Instrument(BaseModel):
    tick_price: float
    ticks_per_point: int

class DatabaseConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    db_name: str

class Config(BaseSettings):
    MNQ: Instrument
    MCL: Instrument
    MES: Instrument
    MGC: Instrument
    database: DatabaseConfig
    model_config = SettingsConfigDict(toml_file="config.toml")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (TomlConfigSettingsSource(settings_cls),)
