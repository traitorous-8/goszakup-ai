import os
from dotenv import load_dotenv

load_dotenv()

OWS_GRAPHQL_URL = os.getenv("OWS_GRAPHQL_URL")
OWS_TOKEN = os.getenv("OWS_TOKEN") or None

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "ows")
DB_USER = os.getenv("DB_USER", "ows")
DB_PASSWORD = os.getenv("DB_PASSWORD", "ows_pass")

BINS = [b.strip() for b in os.getenv("BINS", "").split(",") if b.strip()]

def dsn() -> str:
    return f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}"