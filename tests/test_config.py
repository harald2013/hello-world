import pytest

from reports.config import Settings
from reports.models import summarize


def test_summary():
    assert summarize([-10, 0, 10, 20]) == {
        "count": 4,
        "sum": 20,
        "min": -10,
        "max": 20,
        "mean": 5,
    }


def production(**changes):
    return Settings(
        **{
            "database_url": "postgresql://user:secret@db.example/reports?sslmode=verify-full",
            "environment": "production",
            "api_token": "x" * 32,
            "temporal_api_key": "secret",
            "temporal_tls": True,
            **changes,
        }
    )


@pytest.mark.parametrize(
    "changes",
    [
        {"api_token": ""},
        {"temporal_api_key": ""},
        {"temporal_tls": False},
        {"database_url": "postgresql://db/reports?sslmode=require"},
        {"database_url": "postgresql://db/reports"},
    ],
)
def test_production_rejects_incomplete_security(changes):
    with pytest.raises(ValueError):
        production(**changes)


def test_production_accepts_managed_service_configuration():
    assert production().temporal_tls


def test_staging_requires_a_token():
    with pytest.raises(ValueError):
        Settings("postgresql://db/reports", environment="staging")
