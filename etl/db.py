from typing import Optional, Tuple
from datetime import datetime
import json
import psycopg

def connect(dsn: str) -> psycopg.Connection:
    return psycopg.connect(dsn, autocommit=True)

def get_state(conn, source: str, bin_: str) -> Tuple[Optional[datetime], Optional[str]]:
    with conn.cursor() as cur:
        cur.execute(
            "select last_updated_at, last_external_id from etl_state_ where source=%s and bin=%s",
            (source, bin_),
        )
        row = cur.fetchone()
        if not row:
             return None, None
        return row[0], row[1]

def upsert_state(conn, source: str, bin_: str, last_updated_at: Optional[datetime], last_external_id: Optional[str]) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            insert into etl_state(source, bin, last_updated_at, last_external_id)
            values (%s,%s,%s,%s)
            on conflict (source, bin) do update
              set last_updated_at=excluded.last_updated_at,
                  last_external_id=excluded.last_external_id,
                  updated_at=now()
            """,
            (source, bin_, last_updated_at, last_external_id),
        )

def upsert_raw(conn, source: str, bin_: str, external_id: str, payload: dict, updated_at: Optional[datetime] = None) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            insert into raw_ows(source, bin, external_id, payload, updated_at)
            values (%s,%s,%s,%s,%s)
            on conflict (source, bin, external_id) do update
              set payload=excluded.payload,
                  updated_at=coalesce(excluded.updated_at, raw_ows.updated_at),
                  loaded_at=now()
            """,
            (source, bin_, external_id, json.dumps(payload), updated_at),
        ) 