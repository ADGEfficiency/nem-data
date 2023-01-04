import pydantic


class Constants(pydantic.BaseModel):
    nem_tz: str = "Etc/GMT-10"
    transition_datetime_interval_end: str = "2021-10-01T00:05:00+1000"


constants = Constants()
