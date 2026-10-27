"""Build the outline map (and big-city labels) of one country's regions for the regional mode.

Usage: python tools/build_regionmap.py <admin1.geojson> <places.geojson> <ADM0_A3> <out.js> <key> [n_cities] [min_gap_px]
Example: python tools/build_regionmap.py ne_10m_admin_1_states_provinces.geojson ne_10m_populated_places_simple.geojson MEX data/regions/mx-map.js mx 22
Inputs: Natural Earth 1:10m admin-1 and populated places (public domain), from
https://github.com/nvkelso/natural-earth-vector/tree/master/geojson . Needs: pip install shapely numpy
Writes REGION_MAPS[key] = {w, h, units: [{code, name, d, cx, cy, area}], cities: [{name, x, y, a: label side s|e, pop}], frames: [...]},
codes = ISO 3166-2 suffix (JAL, TX...). For the USA, Alaska and Hawaii are moved into insets at the bottom left.
"""
import json, math, sys
import numpy as np, shapely
from shapely.geometry import shape, MultiPolygon, Point, box
from shapely.ops import unary_union

adm1, places, adm0, out, key = sys.argv[1:6]
NCITY = int(sys.argv[6]) if len(sys.argv) > 6 else 20
RENAME = {'MX-DIF': 'Mexico City', 'MX-MEX': 'State of Mexico', 'US-DC': 'District of Columbia'}
W, TOL_PX, MIN_AREA_PX = 1000, 0.6, 2
CITY_GAP_PX = float(sys.argv[7]) if len(sys.argv) > 7 else 40
INSETS = {'USA': {'US-AK': (0.24, (-154, 50, 70)), 'US-HI': (0.15, (-157, 19, 22))}}  # code: (width share, (lon0, lat1, lat2))

def albers_for(lon0, lat1, lat2, lat0):
    p1, p2, p0, l0 = map(math.radians, (lat1, lat2, lat0, lon0))
    n = (math.sin(p1) + math.sin(p2)) / 2; C = math.cos(p1) ** 2 + 2 * n * math.sin(p1)
    r0 = math.sqrt(C - 2 * n * math.sin(p0)) / n
    def f(c):
        lon, lat = np.radians(c[:, 0]), np.radians(c[:, 1])
        r = np.sqrt(C - 2 * n * np.sin(lat)) / n; t = n * (lon - l0)
        return np.column_stack([r * np.sin(t), -(r0 - r * np.cos(t))])
    return f

feats = [f for f in json.load(open(adm1, encoding='utf8'))['features']
         if f['properties'].get('adm0_a3') == adm0 and not (f['properties'].get('iso_3166_2') or '~').endswith('~')]
geo = {}
for f in feats:
    g = shape(f['geometry'])
    parts = [p for p in (g.geoms if isinstance(g, MultiPolygon) else [g]) if adm0 != 'USA' or p.bounds[0] < 0]  # Aleutians past 180°
    if f['properties']['iso_3166_2'] == 'US-HI': parts = [p for p in parts if p.bounds[0] > -161]  # main islands only
    geo[f['properties']['iso_3166_2']] = unary_union(parts)
names = {f['properties']['iso_3166_2']: RENAME.get(f['properties']['iso_3166_2']) or f['properties']['name_en'] for f in feats}
insets = INSETS.get(adm0, {})
main = [k for k in geo if k not in insets]
minx, miny, maxx, maxy = unary_union([geo[k] for k in main]).bounds
span = maxy - miny
proj_main = albers_for((minx + maxx) / 2, miny + span / 6, maxy - span / 6, (miny + maxy) / 2)
P = {k: shapely.transform(geo[k], proj_main) for k in main}
bx = unary_union(list(P.values())).bounds
s = W / (bx[2] - bx[0]); H = (bx[3] - bx[1]) * s
fit_main = lambda c: (c - [bx[0], bx[1]]) * s
P = {k: shapely.transform(g, fit_main) for k, g in P.items()}
transforms = {k: (lambda pr, ft: (lambda c: ft(pr(c))))(proj_main, fit_main) for k in main}
# insets: own projection, scaled to a share of the width, placed left to right along the bottom
x0, frames, inset_geoms = 8.0, [], {}
for k, (share, (lon0, la1, la2)) in insets.items():
    if k not in geo: continue
    pr = albers_for(lon0, la1, la2, (la1 + la2) / 2)
    g = shapely.transform(geo[k], pr); b = g.bounds
    sc = W * share / (b[2] - b[0]); h = (b[3] - b[1]) * sc
    # as high as possible without touching the main map in that column; grow the canvas if needed
    above = unary_union(list(P.values())).intersection(box(x0 - 6, 0, x0 + W * share + 6, H))
    oy = (above.bounds[3] + 14) if not above.is_empty else H - h - 8
    H = max(H, oy + h + 8)
    ox = x0
    ft = (lambda b, sc, ox, oy: (lambda c: (c - [b[0], b[1]]) * sc + [ox, oy]))(b, sc, ox, oy)
    P_inset = shapely.transform(g, ft); transforms[k] = (lambda pr, ft: (lambda c: ft(pr(c))))(pr, ft)
    frames.append([round(ox - 4, 1), round(oy - 4, 1), round(W * share + 8, 1), round(h + 8, 1)])
    x0 += W * share + 24
    inset_geoms[k] = P_inset
P.update(inset_geoms)
units = []
for code, g in sorted(P.items()):
    polys = sorted(g.geoms if isinstance(g, MultiPolygon) else [g], key=lambda p: -p.area)
    kept = [polys[0]] + [p for p in polys[1:] if p.area >= MIN_AREA_PX]
    d = []
    for p in kept:
        p = p.simplify(TOL_PX, preserve_topology=True)
        for ring in [p.exterior, *p.interiors]:
            pts = list(ring.coords)[:-1]
            if len(pts) >= 3: d.append('M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + 'Z')
    c = g.representative_point()
    units.append({'code': code.split('-')[1], 'name': names[code], 'd': ''.join(d), 'cx': round(c.x, 1), 'cy': round(c.y, 1), 'area': round(g.area)})
# big cities: most populous first, skipping any too close to one already kept
pl = [f for f in json.load(open(places, encoding='utf8'))['features'] if f['properties'].get('adm0_a3') == adm0]
pl.sort(key=lambda f: -(f['properties'].get('pop_max') or 0))
cities, boxes = [], []
CH, FS = 7.2, 12          # approx. label character width and height, in map px
def overlaps(r): return any(not (r[2] < b[0] or r[0] > b[2] or r[3] < b[1] or r[1] > b[3]) for b in boxes)
for f in pl:
    lon, lat = f['geometry']['coordinates'][:2]
    code = next((k for k, g in geo.items() if g.buffer(0.05).contains(Point(lon, lat))), None)
    if not code: continue
    x, y = map(float, transforms[code](np.array([[lon, lat]], dtype=float))[0])
    if any(math.hypot(x - c['x'], y - c['y']) < CITY_GAP_PX for c in cities): continue
    name = ' '.join(f['properties']['name'].split()); tw = CH * len(name)
    # label to the right of the dot, else to the left; drop the city if both collide or leave the map
    # label beside the dot (right, left), then above or below it; drop the city if every spot collides
    for side, dy in (('s', 0), ('e', 0), ('s', FS), ('e', FS), ('s', -FS), ('e', -FS)):
        cy = y + dy
        r = (x + 6, cy - FS / 2 - 1, x + 6 + tw, cy + FS / 2 + 1) if side == 's' else (x - 6 - tw, cy - FS / 2 - 1, x - 6, cy + FS / 2 + 1)
        if r[0] >= 2 and r[2] <= W - 2 and r[1] >= 2 and r[3] <= H - 2 and not overlaps(r): break
    else: continue
    boxes += [r, (x - 4, y - 4, x + 4, y + 4)]
    cities.append({'name': name, 'x': round(x, 1), 'y': round(y, 1), 'a': side, 'dy': dy, 'pop': f['properties'].get('pop_max')})
    if len(cities) >= NCITY: break
data = {'w': W, 'h': round(H), 'units': units, 'cities': cities, 'frames': frames}
js = (f'// Generated by tools/build_regionmap.py from Natural Earth 1:10m (public domain). Do not edit.\n'
      f'(window.REGION_MAPS ||= {{}})["{key}"] = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
open(out, 'w', encoding='utf8').write(js)
print(len(units), 'units,', len(cities), 'cities,', round(len(js) / 1024), 'KB, viewBox', W, 'x', round(H))
print(', '.join(c['name'] for c in cities))
