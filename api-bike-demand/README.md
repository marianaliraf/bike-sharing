# Bike Demand Prediction API

API REST desenvolvida com FastAPI para realizar previsões de demanda de
bicicletas. A aplicação valida os dados recebidos, cria um DataFrame e utiliza
a classe `BikeSharingPredictor` existente para executar a inferência.

O modelo é carregado uma única vez durante a inicialização da aplicação.

## Estrutura do projeto

```text
api-bike-demand/
├── artefacts/
├── app.py
├── predictor.py
├── schemas.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Instalação

Entre na pasta do projeto, crie um ambiente virtual e instale as dependências:

```bash
cd api-bike-demand
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

No Linux ou macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Execução

Execute o comando abaixo a partir da pasta `api-bike-demand`:

```bash
uvicorn app:app --reload
```

A documentação interativa estará disponível em:

http://127.0.0.1:8000/docs

## Exemplo de requisição

O endpoint `POST /predict` aceita um objeto ou uma lista de objetos.

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "instant": 1,
    "season": 1,
    "yr": 0,
    "mnth": 1,
    "hr": 0,
    "holiday": 0,
    "weekday": 6,
    "workingday": 0,
    "weathersit": 1,
    "temp": 0.24,
    "atemp": 0.2879,
    "hum": 0.81,
    "windspeed": 0.0
  }'
```

Resposta:

```json
{
  "predictions": [16.42]
}
```

Para várias previsões, envie um array contendo objetos com a mesma estrutura.
