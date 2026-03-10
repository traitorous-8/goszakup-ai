from etl.ows_client import OWSClient

def fetch_subject(client: OWSClient, subject_id: str) -> dict:
    return client.get_text(f"subject/{subject_id}")