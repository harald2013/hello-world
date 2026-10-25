"""One-shot PostgreSQL dump to a private S3-compatible bucket."""

import hashlib
import os
import subprocess
import sys
import tempfile
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid4

PREFIX = "report-example/production/"


def backup(client, database_url, bucket, prefix=PREFIX, retention_days=7):
    # This bucket is shared. Never accept a wider deletion scope.
    if prefix != PREFIX or retention_days != 7:
        raise ValueError("Unexpected backup scope")
    if "sslmode=verify-full" not in database_url:
        raise ValueError("Database certificate verification required")
    now = datetime.now(UTC)
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "database.dump"
        env = {**os.environ, "PGDATABASE": database_url, "PGCONNECT_TIMEOUT": "15"}
        subprocess.run(
            [
                "pg_dump",
                "--format=custom",
                "--no-owner",
                "--no-acl",
                "--file",
                str(path),
            ],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=600,
            check=True,
        )
        subprocess.run(
            ["pg_restore", "--list", str(path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=60,
            check=True,
        )
        with path.open("rb") as archive:
            digest = hashlib.file_digest(archive, "sha256").hexdigest()
        key = f"{prefix}{now:%Y/%m/%d/%H%M%S}-{uuid4().hex}.dump"
        client.upload_file(
            str(path),
            bucket,
            key,
            ExtraArgs={
                "Metadata": {"sha256": digest},
                "ContentType": "application/octet-stream",
            },
        )
        stored = client.head_object(Bucket=bucket, Key=key)
        if (
            stored["ContentLength"] != path.stat().st_size
            or stored.get("Metadata", {}).get("sha256") != digest
        ):
            raise RuntimeError("Upload verification failed")
    # Prune only after a successful upload; no bucket-wide lifecycle mutation.
    cutoff = now - timedelta(days=retention_days)
    paginator = client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for item in page.get("Contents", []):
            if (
                item["Key"].startswith(prefix)
                and item["Key"].endswith(".dump")
                and item["LastModified"] < cutoff
            ):
                client.delete_object(Bucket=bucket, Key=item["Key"])
    print("Backup completed", flush=True)


def main():
    try:
        import boto3
        from botocore.config import Config

        endpoint = os.environ["BACKUP_ENDPOINT"]
        if not endpoint.startswith("https://"):
            raise ValueError("HTTPS backup endpoint required")
        client = boto3.client(
            "s3",
            endpoint_url=endpoint,
            region_name=os.getenv("AWS_DEFAULT_REGION", "auto"),
            config=Config(
                connect_timeout=15,
                read_timeout=60,
                retries={"max_attempts": 3, "mode": "standard"},
            ),
        )
        backup(
            client,
            os.environ["DATABASE_URL"],
            os.environ["BACKUP_BUCKET"],
            os.getenv("BACKUP_PREFIX", PREFIX),
            int(os.getenv("BACKUP_RETENTION_DAYS", "7")),
        )
        return 0
    except Exception as error:
        print(f"Backup failed ({type(error).__name__})", file=sys.stderr, flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
