#!/usr/bin/env python3
"""Run inside a disposable local API container, never against production."""

import os
import subprocess
import urllib.request
from uuid import uuid4

import psycopg
from psycopg import sql
from psycopg.conninfo import make_conninfo

if os.environ.get("APP_ENV") != "local":
    raise SystemExit("This test requires the local disposable Compose database")

database = "migration_test_" + uuid4().hex
admin_url = os.environ["DATABASE_URL"]
test_url = make_conninfo(admin_url, dbname=database)
environment = {**os.environ, "DATABASE_URL": test_url}


def run(*args):
    return subprocess.run(
        ["/app/.venv/bin/python", *args],
        env=environment,
        capture_output=True,
        text=True,
        timeout=30,
    )


with psycopg.connect(admin_url, autocommit=True) as admin:
    admin.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database)))
    try:
        # Fail after DDL, inside the real migration transaction. No fault switch
        # is added to production code or the normal migration command.
        failed = run(
            "-c",
            "import reports.store as s; "
            "s.SCHEMA += '; SELECT 1 / 0'; raise SystemExit(s.main())",
        )
        assert failed.returncode == 1, failed.stdout
        assert "Migration failed (DivisionByZero)" in failed.stderr, failed.stderr
        assert "Migration completed" not in failed.stdout
        with psycopg.connect(test_url) as conn:
            assert conn.execute("SELECT to_regclass('reports')").fetchone()[0] is None

        for _ in range(2):
            success = run("-m", "reports.store")
            assert success.returncode == 0, success.stderr
            assert "Migration completed" in success.stdout, success.stdout
        with psycopg.connect(test_url) as conn:
            conn.execute("SELECT id FROM reports LIMIT 0")

        # The already running API must still be ready after the failed job.
        with urllib.request.urlopen("http://api:8000/ready", timeout=10) as response:
            assert response.status == 200
        print("Migrations: success, repeat, SQL failure, rollback and live API verified")
    finally:
        admin.execute(
            sql.SQL("DROP DATABASE {} WITH (FORCE)").format(sql.Identifier(database))
        )
