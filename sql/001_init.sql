create table if not exists raw_ows (
  source text not null,
  bin text not null,
  external_id text not null,
  payload jsonb not null,
  updated_at timestamptz null,
  loaded_at timestamptz not null default now(),
  primary key (source, bin, external_id)
);

create table if not exists etl_state (
  source text not null,
  bin text not null,
  last_updated_at timestamptz null,
  last_external_id text null,
  updated_at timestamptz not null default now(),
  primary key (source, bin)
);

create index if not exists idx_raw_ows_loaded_at on raw_ows (loaded_at desc);
create index if not exists idx_raw_ows_updated_at on raw_ows (updated_at desc);