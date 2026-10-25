import os
from dataclasses import dataclass

from psycopg.conninfo import conninfo_to_dict
from temporalio.client import Client


@dataclass(frozen=True)
class Settings:
    database_url: str
    temporal_address: str = "localhost:7233"
    temporal_namespace: str = "default"
    task_queue: str = "reports-v1"
    environment: str = "local"
    api_token: str = ""
    temporal_api_key: str = ""
    temporal_tls: bool = False

    def __post_init__(self):
        if self.environment not in {"local", "test", "staging", "production"}:
            raise ValueError("Unknown APP_ENV")
        if self.environment in {"staging", "production"} and len(self.api_token) < 32:
            raise ValueError("Staging/production require API_TOKEN of 32+ characters")
        if self.environment == "production":
            if not self.temporal_tls or not self.temporal_api_key:
                raise ValueError("Production requires Temporal TLS and API key")
            if conninfo_to_dict(self.database_url).get("sslmode") != "verify-full":
                raise ValueError("Production DATABASE_URL requires sslmode=verify-full")

    @classmethod
    def from_env(cls):
        return cls(
            database_url=os.environ["DATABASE_URL"],
            temporal_address=os.getenv("TEMPORAL_ADDRESS", "localhost:7233"),
            temporal_namespace=os.getenv("TEMPORAL_NAMESPACE", "default"),
            task_queue=os.getenv("TEMPORAL_TASK_QUEUE", "reports-v1"),
            environment=os.getenv("APP_ENV", "local"),
            api_token=os.getenv("API_TOKEN", ""),
            temporal_api_key=os.getenv("TEMPORAL_API_KEY", ""),
            temporal_tls=os.getenv("TEMPORAL_TLS", "false").lower() == "true",
        )


async def connect_temporal(settings: Settings) -> Client:
    return await Client.connect(
        settings.temporal_address,
        namespace=settings.temporal_namespace,
        api_key=settings.temporal_api_key or None,
        tls=settings.temporal_tls,
    )
