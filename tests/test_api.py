import asyncio

import pytest
from fastapi import HTTPException

from src.api.main import (
    QueryRequest,
    health_check,
    list_languages,
    list_models,
    process_query,
    process_query_v1,
    prometheus_metrics,
)


def run_async(coro):
    return asyncio.run(coro)


def test_health_check_returns_healthy_status():
    response = run_async(health_check())

    assert response.status == "healthy"


def test_v1_query_returns_answer_sources_and_metadata():
    body = run_async(process_query_v1(
        QueryRequest(query="What is FastAPI?", language="english")
    ))

    assert body.response
    assert len(body.sources) == 3
    assert body.detected_language == "English"
    assert body.model_used == "groq-mixtral"


def test_legacy_query_endpoint_still_works():
    response = run_async(process_query(QueryRequest(query="What is FAISS?")))

    assert response.response


def test_query_rejects_empty_input():
    with pytest.raises(HTTPException) as exc_info:
        run_async(process_query_v1(QueryRequest(query="   ")))

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Query cannot be empty"


def test_config_and_metrics_endpoints_are_available():
    models_response = run_async(list_models())
    languages_response = run_async(list_languages())
    metrics_response = run_async(prometheus_metrics())

    assert models_response["available_models"]
    assert languages_response["supported_languages"]
    assert "rag_queries_total" in metrics_response.body.decode()
