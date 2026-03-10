import os
import re
import json
import psycopg2
import psycopg2.extras
import requests
from dotenv import load_dotenv

load_dotenv()

AI_BASE_URL = os.getenv("AI_BASE_URL", "").rstrip("/")
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_MODEL = os.getenv("AI_MODEL", "openai/gpt-oss-120b")

print(f"LLM: {AI_MODEL}")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "ows")
DB_USER = os.getenv("DB_USER", "ows")
DB_PASSWORD = os.getenv("DB_PASSWORD", "ows_pass")

K_DEFAULT = int(os.getenv("K_DEFAULT", "5"))


def clean_query(user_q: str) -> str:
    """
    ВАЖНО: f_search использует plainto_tsquery => если передать "что есть по trdbuy",
    оно превратится в AND по словам "что & есть & по & trdbuy" и даст 0.
    Поэтому чистим до латиницы/цифр/underscore/dash.
    """
    toks = re.findall(r"[A-Za-z0-9_-]+", user_q)
    q = " ".join(toks).replace("_", " ").strip()
    return q or user_q.strip()


def db_conn():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def db_search(q: str, k: int = 5):
    sql = "select source, loaded_at, source_external_id, item_id, item_preview from f_search(%s, %s);"
    with db_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, (q, k))
            return cur.fetchall()


def call_llm(user_question: str, rows: list[dict]) -> str:
    if not AI_BASE_URL or not AI_API_KEY:
        return "AI_BASE_URL/AI_API_KEY не заданы в .env."

    url_candidates = [
        f"{AI_BASE_URL}/v1/chat/completions",
        f"{AI_BASE_URL}/chat/completions",
        f"{AI_BASE_URL}/v1/responses",
        f"{AI_BASE_URL}/responses",
    ]

    context = "\n".join(
        [
            f"- source={r['source']}, loaded_at={r['loaded_at']}, ext_id={r['source_external_id']}, item_id={r['item_id']}, preview={r['item_preview']}"
            for r in rows
        ]
    )

    system = (
        "Ты помощник по данным госзакупок. Отвечай на RU/KZ. "
        "Используй ТОЛЬКО переданный контекст (результаты поиска). "
        "Если контекста недостаточно — скажи, что данных нет/нужно уточнить."
    )
    user = f"Вопрос: {user_question}\n\nКонтекст (результаты поиска):\n{context}"

    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload_chat = {
        "model": AI_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.2,
    }

    payload_resp = {
        "model": AI_MODEL,
        "input": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }

    last_err = None
    for url in url_candidates:
        try:
            if url.endswith("/responses"):
                r = requests.post(url, headers=headers, json=payload_resp, timeout=60)
                r.raise_for_status()
                data = r.json()
                if isinstance(data, dict):
                    if "output_text" in data and isinstance(data["output_text"], str):
                        return data["output_text"].strip()
                    if "output" in data:
                        try:
                            return data["output"][0]["content"][0]["text"].strip()
                        except Exception:
                            pass
                return json.dumps(data, ensure_ascii=False)[:1500]
            else:
                r = requests.post(url, headers=headers, json=payload_chat, timeout=60)
                r.raise_for_status()
                data = r.json()
                return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            last_err = e

    return f"LLM запрос не прошёл: {last_err}"


def main():
    print("agent.py ready. Введите вопрос (exit для выхода).")
    while True:
        try:
            q_user = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not q_user:
            continue
        if q_user.lower() in ("exit", "quit", "q"):
            break

        q_clean = clean_query(q_user)
        rows = db_search(q_clean, K_DEFAULT)

        if not rows:
            print(f"По запросу <{q_clean}> в базе данных ничего не найдено.")
            continue

        answer = call_llm(q_user, rows)
        print(answer)
        print()


if __name__ == "__main__":
    main()
