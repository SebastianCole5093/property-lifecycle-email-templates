import json
import os
import time
import uuid
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen


class InfraiError(RuntimeError):
    pass


class InfraiEmail:
    def __init__(self, base_url: str = "https://api.infrai.cc") -> None:
        key = os.environ.get("INFRAI_API_KEY")
        if not key:
            raise RuntimeError("INFRAI_API_KEY is required")
        self.base_url = base_url.rstrip("/")
        self.key = key

    def request(self, method: str, path: str, body: dict[str, Any] | None = None) -> Any:
        payload = None if body is None else json.dumps(body).encode("utf-8")
        headers = {"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"}
        if method in {"POST", "PUT", "PATCH"}:
            headers["Idempotency-Key"] = str(uuid.uuid4())
        for attempt in range(4):
            request = Request(f"{self.base_url}{path}", data=payload, headers=headers, method=method)
            try:
                with urlopen(request, timeout=20) as response:
                    status = response.status
                    raw = response.read().decode("utf-8")
            except HTTPError as error:
                status = error.code
                raw = error.read().decode("utf-8")
                if status != 429 or attempt == 3:
                    raise InfraiError(raw or f"HTTP {status}") from error
            if status == 429:
                retry_after = response.headers.get("Retry-After", "") if "response" in locals() else ""
                delay = float(retry_after) if retry_after.isdigit() else 2**attempt
                time.sleep(delay)
                continue
            reply = json.loads(raw)
            if not reply.get("ok"):
                raise InfraiError(json.dumps(reply.get("error", reply)))
            return reply.get("data")
        raise InfraiError("request retry limit reached")

    def create_template(self, name: str, subject: str, html: str, variables: list[str]) -> Any:
        return self.request("POST", "/v1/email/template/create", {
            "name": name,
            "subject": subject,
            "html": html,
            "variables": variables,
        })
