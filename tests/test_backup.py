import subprocess
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import Mock

import pytest

from ops.backup import PREFIX, backup


def client_for_dump(monkeypatch):
    def dump(command, **kwargs):
        if command[0] == "pg_dump":
            Path(command[-1]).write_bytes(b"archive")

    monkeypatch.setattr(subprocess, "run", dump)
    client = Mock()

    def uploaded(filename, bucket, key, ExtraArgs):
        client.head_object.return_value = {
            "ContentLength": Path(filename).stat().st_size,
            "Metadata": ExtraArgs["Metadata"],
        }

    client.upload_file.side_effect = uploaded
    return client


def test_retention_never_deletes_outside_scope(monkeypatch):
    client = client_for_dump(monkeypatch)
    old = datetime.now(UTC) - timedelta(days=8)
    client.get_paginator.return_value.paginate.return_value = [
        {
            "Contents": [
                {"Key": PREFIX + "old.dump", "LastModified": old},
                {"Key": "other/old.dump", "LastModified": old},
                {"Key": PREFIX + "notes.txt", "LastModified": old},
                {"Key": PREFIX + "new.dump", "LastModified": datetime.now(UTC)},
            ]
        },
    ]
    backup(client, "postgresql://example/reports?sslmode=verify-full", "bucket")
    client.delete_object.assert_called_once_with(
        Bucket="bucket", Key=PREFIX + "old.dump"
    )
    assert client.upload_file.call_args.args[2].startswith(PREFIX)


def test_failed_dump_does_not_upload_or_prune(monkeypatch):
    def fail(*args, **kwargs):
        raise subprocess.CalledProcessError(1, "pg_dump")

    monkeypatch.setattr(subprocess, "run", fail)
    client = Mock()
    with pytest.raises(subprocess.CalledProcessError):
        backup(client, "postgresql://example/reports?sslmode=verify-full", "bucket")
    client.upload_file.assert_not_called()
    client.get_paginator.assert_not_called()


def test_unverified_upload_does_not_prune(monkeypatch):
    client = client_for_dump(monkeypatch)
    client.upload_file.side_effect = None
    client.head_object.return_value = {"ContentLength": 1, "Metadata": {}}
    with pytest.raises(RuntimeError):
        backup(client, "postgresql://example/reports?sslmode=verify-full", "bucket")
    client.get_paginator.assert_not_called()


def test_rejects_bucket_wide_prefix():
    with pytest.raises(ValueError):
        backup(Mock(), "postgresql://example/reports?sslmode=verify-full", "bucket", "")
