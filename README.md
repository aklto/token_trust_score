## Запуск через Docker

### 1. Сборка образа:

```bash
docker build -t token-trust-score .
```

### 2. Запуск контейнера:

```bash
docker run -d -p 8000:8000 --name trust-api token-trust-score
```

---

## Конфигурация

API-ключи положить в .env

---

## Endpoint

### `POST /trust-score`

**Описание:** возвращает `trust_score` и анализ контракта.

**Пример запроса:**

```json
{
  "token_id": "chainlink",
  "github_repo": "smartcontractkit/chainlink",
  "contract_address": "0x514910771af9ca656af840dff83e8264ecf986ca"
}
```

**Пример ответа:**

```json
{
  "token_id": "chainlink",
  "trust_score": 0.742,
  "contract_analysis": {
    "is_verified": true,
    "has_delegatecall": false,
    "has_selfdestruct": false,
    "holders_count": 10,
    "top_holder_ratio": 0.65
  }
}
```

---

## Структура проекта

```
token_trust_score/
├── main.py
├── config.py
├── requirements.txt
├── api/
│   └── routes.py
├── models/
│   └── request_models.py
├── services/
│   ├── coingecko_service.py
│   ├── github_service.py
│   ├── contract_service.py
│   ├── embedding_service.py
│   └── trust_score.py
└── utils/
    └── normalization.py
```
