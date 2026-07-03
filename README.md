# 🚲 Bike Demand Prediction API

API REST desenvolvida com **FastAPI** para previsão da demanda de bicicletas compartilhadas utilizando um modelo de Machine Learning baseado em **XGBoost** otimizado com **Optuna**.

Este projeto demonstra uma etapa completa de implantação de um modelo de Machine Learning, desde a exportação do modelo treinado até sua disponibilização por meio de uma API para inferência.

---

# 📖 Sobre o projeto

O modelo foi treinado utilizando o conjunto de dados **Bike Sharing Dataset**, cujo objetivo é prever a quantidade de bicicletas alugadas em determinado instante com base em informações como:

- estação do ano;
- mês;
- hora do dia;
- dia da semana;
- feriados;
- condições climáticas;
- temperatura;
- umidade;
- velocidade do vento.

Antes da inferência, os dados passam automaticamente pelas mesmas etapas de engenharia de atributos utilizadas durante o treinamento, garantindo consistência entre treinamento e produção.

---

# 🏗️ Estrutura do projeto

```
api-bike-demand/
│
├── artifacts/
│   ├── bike_sharing_xgb_model.joblib
│   ├── ...
│
├── predictor.py
├── app.py
├── schemas.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Tecnologias utilizadas

- Python 3.11+
- FastAPI
- XGBoost
- Scikit-Learn
- Pandas
- Joblib
- Uvicorn
- Pydantic

---

# 🚀 Como executar o projeto

## 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/api-bike-demand.git
```

Entre na pasta do projeto:

```bash
cd api-bike-demand
```

---

## 2. Crie um ambiente virtual (opcional)

Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 4. Execute a API

```bash
uvicorn app:app --reload
```

A API será iniciada em:

```
http://127.0.0.1:8000
```

---

# 📚 Documentação da API

O FastAPI gera automaticamente uma interface interativa para testes.

Após iniciar a aplicação, acesse:

```
http://127.0.0.1:8000/docs
```

Nessa interface é possível:

- visualizar os endpoints;
- testar requisições;
- visualizar exemplos de entrada e saída;
- validar automaticamente os dados enviados.

---

# 📡 Endpoints

## GET /

Verifica se a API está em funcionamento.

### Resposta

```json
{
  "message": "Bike Demand Prediction API"
}
```

---

## POST /predict

Realiza a previsão da demanda de bicicletas.

### Exemplo de requisição

```json
{
  "instant": 5000,
  "season": 3,
  "yr": 1,
  "mnth": 9,
  "hr": 17,
  "holiday": 0,
  "weekday": 2,
  "workingday": 1,
  "weathersit": 1,
  "temp": 0.70,
  "atemp": 0.68,
  "hum": 0.45,
  "windspeed": 0.10
}
```

### Exemplo de resposta

```json
{
  "prediction": 612.48
}
```

---

# 🧠 Fluxo da predição

A cada requisição, a API executa automaticamente as seguintes etapas:

1. Recebe os dados enviados pelo cliente.
2. Valida os dados utilizando Pydantic.
3. Converte os dados para um DataFrame do Pandas.
4. Aplica a mesma engenharia de atributos utilizada durante o treinamento.
5. Carrega o modelo previamente treinado.
6. Realiza a inferência.
7. Retorna a previsão ao cliente.

---

# 📈 Modelo de Machine Learning

Modelo utilizado:

- XGBoost Regressor

O modelo foi otimizado utilizando **Optuna**, que realizou a busca automática pelos melhores hiperparâmetros antes da etapa de implantação.

---

# 🎯 Objetivo educacional

Este projeto foi desenvolvido como parte do curso **Modelos Regressivos: Avançando nos Modelos de Regressão**.

O objetivo é demonstrar como transformar um modelo treinado em uma aplicação pronta para consumo por outros sistemas utilizando FastAPI.

---

# 📄 Licença

Este projeto possui finalidade exclusivamente educacional.
