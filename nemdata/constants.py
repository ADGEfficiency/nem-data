import pydantic


class Constants(pydantic.BaseModel):
    nem_tz: str = "Etc/GMT-10"


constants = Constants()
