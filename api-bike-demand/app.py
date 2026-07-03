from typing import Annotated

import pandas as pd
from fastapi import FastAPI, HTTPException

from predictor import BikeSharingPredictor
from schemas import BikeObservation, PredictionResponse


app = FastAPI(
    title="Bike Demand Prediction API",
    description="API para inferência de demanda de bicicletas.",
    version="1.0.0",
)

# O modelo e seus artefatos são carregados uma única vez ao iniciar a aplicação.
predictor = BikeSharingPredictor()

PredictionInput = Annotated[
    BikeObservation | list[BikeObservation],
    "Uma observação ou uma lista de observações",
]


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Bike Demand Prediction API"}


@app.post("/predict", response_model=PredictionResponse)
def predict(data: PredictionInput) -> PredictionResponse:
    observations = data if isinstance(data, list) else [data]

    if not observations:
        raise HTTPException(
            status_code=422,
            detail="A lista de observações não pode estar vazia.",
        )

    try:
        dataframe = pd.DataFrame(
            [observation.model_dump() for observation in observations]
        )
        predictions = predictor.predict(dataframe)
        return PredictionResponse(
            predictions=[float(prediction) for prediction in predictions]
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao realizar a inferência: {exc}",
        ) from exc
