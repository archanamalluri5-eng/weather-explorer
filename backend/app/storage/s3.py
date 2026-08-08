"""AWS S3 backend (lazy-imported so dev/test need no boto3)."""

from __future__ import annotations

from datetime import timezone

from .base import StorageBackend, StoredFile


class S3Storage(StorageBackend):
    def __init__(self, bucket: str, region: str = "us-east-1") -> None:
        import boto3  # optional dependency

        self._bucket = bucket
        self._s3 = boto3.client("s3", region_name=region)

    def put(self, name: str, data: bytes) -> None:
        self._s3.put_object(
            Bucket=self._bucket,
            Key=name,
            Body=data,
            ContentType="application/json",
        )

    def get(self, name: str) -> bytes | None:
        try:
            response = self._s3.get_object(Bucket=self._bucket, Key=name)
            return response["Body"].read()
        except Exception as exc:  # noqa: BLE001 - SDK raises typed clients per vendor
            if getattr(exc, "response", {}).get("Error", {}).get("Code") == "NoSuchKey":
                return None
            raise

    def list(self) -> list[StoredFile]:
        files: list[StoredFile] = []
        paginator = self._s3.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=self._bucket):
            for obj in page.get("Contents", []):
                created = obj.get("LastModified")
                files.append(
                    StoredFile(
                        name=obj["Key"],
                        size=obj["Size"],
                        created_at=created.replace(tzinfo=timezone.utc)
                        if created else None,
                    )
                )
        files.sort(key=lambda f: f.created_at, reverse=True)
        return files

    def exists(self, name: str) -> bool:
        try:
            self._s3.head_object(Bucket=self._bucket, Key=name)
            return True
        except Exception as exc:  # noqa: BLE001
            if getattr(exc, "response", {}).get("Error", {}).get("Code") in (
                "404",
                "NoSuchKey",
                "NotFound",
            ):
                return False
            raise
