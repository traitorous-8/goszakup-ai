import time
import requests
from typing import Any

class OWSGQLClient:
    def __init__(self, graphql_url: str, token: str | None = None, timeout: int = 180):
        self.graphql_url = graphql_url.strip()
        self.timeout = timeout
        self.s = requests.Session()
        if token: 
            self.s.headers.update({"Authorization": f"Bearer {token}"})
        self.s.headers.update({"Content-Type": "application/json"})

    def query(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = {"query": query, "variables": variables or {}}

        for attempt in range(5):
            try:
                r = self.s.post(self.graphql_url, json=payload, timeout=self.timeout)
                if r.status_code in (502, 503, 504):
                    time.sleep(2*(attempt + 1))
                    continue

                r.raise_for_status()

                data = r.json()
                if "errors" in data:
                    raise RuntimeError(str(data["errors"])[:500])
                return data
            
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                time.sleep(2 * (attempt + 1))
                continue

        raise RuntimeError("OWS GraphQL is unavailable after retries (502/timeout).")