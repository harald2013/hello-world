"""Run inside the backup image against the LOCAL synthetic Compose stack only."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, "/app")
import backup as implementation

url = "postgresql://reports:local-demo-only@postgres/reports?sslmode=verify-full"
original_environment = implementation.postgres_environment


def local_environment(value):
    assert value == url
    env = original_environment(value)
    assert env["PGHOST"] == "postgres" and env["PGDATABASE"] == "reports"
    # Only this fixed local Compose database has no TLS listener.
    env["PGSSLMODE"] = "disable"
    return env


implementation.postgres_environment = local_environment


class LocalObjectStore:
    def upload_file(self, filename, bucket, key, ExtraArgs):
        self.archive = Path(filename).read_bytes()
        self.metadata = ExtraArgs["Metadata"]

    def head_object(self, **kwargs):
        return {"ContentLength": len(self.archive), "Metadata": self.metadata}

    def get_paginator(self, operation):
        assert operation == "list_objects_v2"
        return self

    def paginate(self, **kwargs):
        return [{"Contents": []}]


def run(command, env):
    return subprocess.run(command, env=env, capture_output=True, text=True,
                          check=True, timeout=60).stdout.strip()


env = local_environment(url)
store = LocalObjectStore()
implementation.backup(store, url, "local-test-bucket")
target = "backup_check_" + uuid4().hex
query = "SELECT coalesce(json_agg(t ORDER BY id)::text,'[]') FROM (SELECT id,status,input,result FROM reports) t"
source_rows = json.loads(run(["psql", "-XAt", "-c", query], env))
try:
    run(["createdb", "--maintenance-db=reports", target], env)
    with tempfile.TemporaryDirectory() as directory:
        archive = Path(directory) / "restore.dump"
        archive.write_bytes(store.archive)
        run(["pg_restore", "--dbname=" + target, "--no-owner", "--no-acl",
             "--exit-on-error", str(archive)], env)
    restored_rows = json.loads(run(["psql", "-d", target, "-XAt", "-c", query], env))
    assert source_rows == restored_rows
    print("Backup archive restored; local report rows match")
finally:
    run(["dropdb", "--maintenance-db=reports", "--if-exists", target], env)
