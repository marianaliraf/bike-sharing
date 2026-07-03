from pydantic import BaseModel, ConfigDict, Field


class BikeObservation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    instant: int = Field(ge=1, description="Identificador sequencial do registro")
    season: int = Field(ge=1, le=4)
    yr: int = Field(ge=0, le=1)
    mnth: int = Field(ge=1, le=12)
    hr: int = Field(ge=0, le=23)
    holiday: int = Field(ge=0, le=1)
    weekday: int = Field(ge=0, le=6)
    workingday: int = Field(ge=0, le=1)
    weathersit: int = Field(ge=1, le=4)
    temp: float = Field(ge=0, le=1)
    atemp: float = Field(ge=0, le=1)
    hum: float = Field(ge=0, le=1)
    windspeed: float = Field(ge=0, le=1)


class PredictionResponse(BaseModel):
    predictions: list[float]
