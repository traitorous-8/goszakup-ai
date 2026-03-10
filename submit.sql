-- submit.sql

-- 0) На всякий случай: если функция/вью уже были
drop function if exists f_search(text, int);
drop view if exists v_search_items;

-- 1) Итоговая витрина для поиска
drop table if exists d_search_items;
create table d_search_items (
  source text not null,
  loaded_at timestamptz not null,
  source_external_id text not null,
  item_id text not null,
  item_text text not null,
  tsv tsvector,
  primary key (source, loaded_at, source_external_id, item_id)
);

-- 2) Универсальная VIEW (собираем item_text из *_items)
create view v_search_items as
select 'trdbuy'::text as source,
       loaded_at,
       source_external_id,
       id::text as item_id,
       item::text as item_text
from d_trdbuy_items
union all
select 'obtrdbuy'::text as source,
       loaded_at,
       source_external_id,
       id::text as item_id,
       item::text as item_text
from d_obtrdbuy_items
union all
select 'contract'::text as source,
       loaded_at,
       source_external_id,
       id::text as item_id,
       item::text as item_text
from d_contract_items;

-- 3) Заполняем d_search_items из view (не даем NULL попасть в item_text)
insert into d_search_items (source, loaded_at, source_external_id, item_id, item_text)
select
  source,
  loaded_at,
  source_external_id,
  item_id,
  coalesce(item_text, '') as item_text
from v_search_items
on conflict do nothing;

-- 4) tsv и индекс
update d_search_items
set tsv = to_tsvector(
  'simple',
  coalesce(item_text,'') || ' ' ||
  coalesce(source,'') || ' ' ||
  coalesce(source_external_id,'')
);

create index if not exists idx_d_search_items_tsv on d_search_items using gin(tsv);

-- 5) Функция поиска
create function f_search(q text, k int default 10)
returns table(
  source text,
  loaded_at timestamptz,
  source_external_id text,
  item_id text,
  item_preview text
)
language sql
as $$
  select
    source,
    loaded_at,
    source_external_id,
    item_id,
    left(item_text, 200) as item_preview
  from d_search_items
  where tsv @@ plainto_tsquery('simple', q)
  order by loaded_at desc
  limit k
$$;

-- 6) Проверки
select source, count(*) from d_search_items group by source order by 2 desc;

select * from f_search('contract', 5);
select * from f_search('trdbuy', 5);
select * from f_search('obtrdbuy', 5);