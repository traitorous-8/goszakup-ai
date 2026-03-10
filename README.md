ETL + Postgres search mart + LLM agent (RAG-lite) for OWS v3 (GraphQL).

Что есть:
- raw_ows (JSONB) + витрины d_* + d_search_items (tsvector + GIN)
- SQL функция f_search(q,k)
- agent.py: вопрос RU/KZ -> f_search -> контекст -> LLM (nitec-ai) -> ответ

Запуск:
1) Поднять Postgres:
docker compose up -d

2) Применить SQL:
PowerShell: Get-Content .\submit.sql | docker exec -i goszakup-ai-db-1 psql -U ows -d ows

3) Запустить агента:
pip install python-dotenv psycopg2-binary requests,
python agent.py

Проверки (psql):
select source, count(*) from d_search_items group by source;
select * from f_search('contract', 5);
select * from f_search('trdbuy', 5);
select * from f_search('obtrdbuy', 5);

.env:
Используй .env.example как шаблон. .env не коммитить.
