import json, re, sys, unicodedata, urllib.request, concurrent.futures as cf, os
S = sys.argv[1]
teams = json.load(open(f'{S}/teams.json'))
def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')
GK = ["gkDiving","gkHandling","gkKicking","gkReflexes","acceleration","gkPositioning"]; GKL=["DIV","HAN","KIC","REF","SPD","POS"]
OUT = ["pac","sho","pas","dri","def","phy"]; OUTL=["PAC","SHO","PAS","DRI","DEF","PHY"]
def get(tid, label):
    url = f'https://www.ea.com/games/ea-sports-fc/ratings/teams-ratings/{slug(label)}/{tid}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    for _ in range(3):
        try:
            s = urllib.request.urlopen(req, timeout=40).read().decode()
            pp = json.loads(re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', s, re.S).group(1))['props']['pageProps']
            items = pp['ratingsEntries']['items']
            out = []
            for p in items:
                gk = (p.get('position') or {}).get('shortLabel') == 'GK'
                ks, ls = (GK, GKL) if gk else (OUT, OUTL)
                st = p.get('stats') or {}
                out.append({
                    'id': p['id'],
                    'name': p.get('commonName') or ' '.join(x for x in [p.get('firstName'), p.get('lastName')] if x),
                    'short': p.get('commonName') or p.get('lastName') or p.get('firstName'),
                    'full': ' '.join(x for x in [p.get('firstName'), p.get('lastName'), p.get('commonName')] if x),
                    'ovr': p.get('overallRating'), 'pos': (p.get('position') or {}).get('shortLabel'),
                    'photo': p.get('avatarUrl'), 'club': (p.get('team') or {}).get('label'),
                    'clubImg': (p.get('team') or {}).get('imageUrl'),
                    'nation': (p.get('nationality') or {}).get('label'), 'nationImg': (p.get('nationality') or {}).get('imageUrl'),
                    'stats': [[l, (st.get(k) or {}).get('value')] for k, l in zip(ks, ls)],
                })
            return tid, label, out
        except Exception as e:
            err = str(e)
    return tid, label, None
res, fails = [], []
with cf.ThreadPoolExecutor(8) as ex:
    for tid, label, out in ex.map(lambda kv: get(*kv), teams.items()):
        if out is None: fails.append(label)
        else: res.extend(out)
seen = {}
for p in res: seen[p['id']] = p
json.dump(list(seen.values()), open(f'{S}/players.json', 'w'), ensure_ascii=False)
print('jogadores', len(seen), 'falhas', len(fails), fails[:30])
