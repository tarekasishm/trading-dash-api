from trades.config import Config, Instrument

c = Config()
print(Instrument(**c.model_dump()["MNQ"]))