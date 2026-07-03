import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


BASE_URL = "http://127.0.0.1:8000"

OBSERVATION = {
    "instant": 5000,
    "season": 3,          # Outono (época com alta demanda no dataset)
    "yr": 1,              # Segundo ano do conjunto de dados
    "mnth": 9,            # Setembro
    "hr": 17,             # Horário de pico
    "holiday": 0,
    "weekday": 2,         # Terça-feira
    "workingday": 1,      # Dia útil
    "weathersit": 1,      # Clima favorável
    "temp": 0.70,         # Temperatura agradável
    "atemp": 0.68,
    "hum": 0.45,          # Umidade moderada
    "windspeed": 0.10     # Pouco vento
}

OBSERVATION_2 = {
    "instant": 5200,
    "season": 3,
    "yr": 1,
    "mnth": 10,
    "hr": 8,
    "holiday": 0,
    "weekday": 2,
    "workingday": 1,
    "weathersit": 1,
    "temp": 0.62,
    "atemp": 0.60,
    "hum": 0.55,
    "windspeed": 0.08,
}


def request_json(
    path: str,
    method: str = "GET",
    payload: Any | None = None,
) -> tuple[int, Any]:
    
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    
    request = Request(
        url=f"{BASE_URL}{path}",
        data=body,
        method=method,
        headers={"Content-Type": "application/json"},
    )

    with urlopen(request, timeout=30) as response:
        
        response_body = response.read().decode("utf-8")
        
        return response.status, json.loads(response_body)


def run_test(name: str, path: str, method: str = "GET", payload: Any = None) -> None:
    
    status, response = request_json(path, method, payload)
    
    if not 200 <= status < 300:
        raise AssertionError(f"{name}: status inesperado {status}")

    print(f"[OK] {name} - HTTP {status}")
    print(json.dumps(response, indent=2, ensure_ascii=False))


def main() -> None:
    print(f"Testando API em {BASE_URL}\n")

    run_test("Rota raiz", "/")
    #run_test("Previsão única", "/predict", "POST", OBSERVATION)
    run_test("Previsão em lote", "/predict", "POST", [OBSERVATION, OBSERVATION_2])

    print("\nTodos os testes foram concluídos com sucesso.")


if __name__ == "__main__":
    try:
        main()
    except HTTPError as exc:
        response_body = exc.read().decode("utf-8")
        print(f"[ERRO] API retornou HTTP {exc.code}: {response_body}")
        raise SystemExit(1) from exc
    except URLError as exc:
        print(
            "[ERRO] Não foi possível conectar à API. "
            "Execute 'uvicorn app:app --reload' dentro de api-bike-demand."
        )
        raise SystemExit(1) from exc
    except (AssertionError, json.JSONDecodeError) as exc:
        print(f"[ERRO] {exc}")
        raise SystemExit(1) from exc
