create table if not exists public.slots (
  id text primary key,
  sort int not null,
  label text not null,
  player text,
  overall int,
  picked_by text,
  updated_at timestamptz not null default now()
);

alter table public.slots enable row level security;

create policy "todos podem ver" on public.slots for select to anon, authenticated using (true);
create policy "todos podem editar" on public.slots for update to anon, authenticated using (true) with check (true);

insert into public.slots (id, sort, label) values
  ('gk',  1,  'GOL'),
  ('zge', 2,  'ZAG'),
  ('zgc', 3,  'ZAG'),
  ('zgd', 4,  'ZAG'),
  ('ale', 5,  'ALA E'),
  ('vle', 6,  'VOL'),
  ('vld', 7,  'VOL'),
  ('ald', 8,  'ALA D'),
  ('mei', 9,  'MEI'),
  ('ate', 10, 'ATA'),
  ('atd', 11, 'ATA'),
  ('r1',  12, 'RES'),
  ('r2',  13, 'RES'),
  ('r3',  14, 'RES'),
  ('r4',  15, 'RES')
on conflict (id) do nothing;

alter publication supabase_realtime add table public.slots;
