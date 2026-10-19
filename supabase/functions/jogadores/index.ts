// Busca jogadores na base oficial de notas do EA FC 27 e devolve só o necessário para a carta.
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, apikey, content-type, x-client-info",
};

const GK = ["gkDiving", "gkHandling", "gkKicking", "gkReflexes", "acceleration", "gkPositioning"];
const GK_LABELS = ["DIV", "HAN", "KIC", "REF", "SPD", "POS"];
const OUT = ["pac", "sho", "pas", "dri", "def", "phy"];
const OUT_LABELS = ["PAC", "SHO", "PAS", "DRI", "DEF", "PHY"];

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  const q = (new URL(req.url).searchParams.get("q") || "").trim().slice(0, 40);
  if (q.length < 2) return Response.json([], { headers: CORS });

  const url = `https://drop-api.ea.com/rating/ea-sports-fc?locale=en&limit=20&search=${encodeURIComponent(q)}`;
  const r = await fetch(url, { headers: { "User-Agent": "Mozilla/5.0" } });
  if (!r.ok) return Response.json({ error: "busca indisponível" }, { status: 502, headers: CORS });
  const data = await r.json();

  const players = (data.items || []).map((p: any) => {
    const gk = p.position?.shortLabel === "GK";
    const keys = gk ? GK : OUT;
    const labels = gk ? GK_LABELS : OUT_LABELS;
    return {
      id: p.id,
      name: p.commonName || [p.firstName, p.lastName].filter(Boolean).join(" "),
      short: p.commonName || p.lastName || p.firstName,
      ovr: p.overallRating,
      pos: p.position?.shortLabel,
      photo: p.avatarUrl,
      club: p.team?.label,
      clubImg: p.team?.imageUrl,
      nation: p.nationality?.label,
      nationImg: p.nationality?.imageUrl,
      stats: keys.map((k, i) => [labels[i], p.stats?.[k]?.value ?? null]),
    };
  });

  return Response.json(players, {
    headers: { ...CORS, "Cache-Control": "public, max-age=3600" },
  });
});
