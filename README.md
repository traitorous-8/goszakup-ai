Агент реализован в `agent.py`.



Пайплайн:

1\) Пользователь вводит вопрос (RU/KZ) в консоли.

2\) Агент извлекает релевантный контекст из PostgreSQL через функцию `f\_search(q, k)` (витрина `d\_search\_items`, tsvector + GIN).

3\) Найденные строки (source, source\_external\_id, item\_id, item\_preview) передаются в LLM как контекст.

4\) LLM генерирует ответ на естественном языке на основе контекста (если контекста нет — сообщает, что ничего не найдено).



Конфигурация:

\- Переменные берутся из `.env`: `AI\_BASE\_URL`, `AI\_API\_KEY`, `AI\_MODEL`, параметры БД (`DB\_HOST/PORT/NAME/USER/PASSWORD`).



Запуск:

```bash

pip install python-dotenv psycopg2-binary requests

python agent.py





Примеры запросов:



найди contract по limit\_5



что есть по trdbuy



Ожидаемый результат:



Агент выводит таблицу найденных item\_id и краткий текстовый ответ, сформированный LLM.

