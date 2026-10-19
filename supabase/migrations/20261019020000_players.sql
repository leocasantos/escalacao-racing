-- Base de jogadores do FC 27 (copiada das páginas de times do site da EA)
create table if not exists public.players (
  id int primary key,
  busca text not null,
  ovr int,
  data jsonb not null
);
alter table public.players enable row level security;
create policy "todos podem ver jogadores" on public.players for select to anon, authenticated using (true);
create index if not exists players_ovr on public.players (ovr desc);
