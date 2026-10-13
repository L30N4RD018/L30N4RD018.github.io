"""Datos del mapa de la página personal, solo con fuentes públicas.

- Contorno de Colombia: Natural Earth 1:10m vía world-atlas (TopoJSON, id 170).
- Sedes de salud: REPS público de datos.gov.co (c36g-9fc2), contadas por municipio y por ESE sí/no.
- Coordenadas de los municipios: DIVIPOLA de datos.gov.co (gdxc-w37w).
"""
import json
import math
import sys

D, OUT = sys.argv[1], sys.argv[2]

W = 1000
minx, miny, maxx, maxy = -79.1, -4.3, -66.8, 12.6  # continente; San Andrés va en recuadro
lat0 = math.radians((miny + maxy) / 2)
kx = math.cos(lat0)
scale = W / ((maxx - minx) * kx)
H = round((maxy - miny) * scale)


def proj(lon, lat):
    return ((lon - minx) * kx * scale, (maxy - lat) * scale)


# --- contorno desde TopoJSON
topo = json.load(open(f"{D}/countries-10m.json"))
sx, sy = topo["transform"]["scale"]
tx, ty = topo["transform"]["translate"]


def arc(i):
    rev = i < 0
    a = topo["arcs"][~i if rev else i]
    x = y = 0
    pts = []
    for dx, dy in a:
        x += dx
        y += dy
        pts.append((x * sx + tx, y * sy + ty))
    return pts[::-1] if rev else pts


col = next(g for g in topo["objects"]["countries"]["geometries"] if g.get("id") == "170")
polys = col["arcs"] if col["type"] == "MultiPolygon" else [col["arcs"]]
paths = []
for poly in polys:
    ring = []
    for i in poly[0]:
        seg = arc(i)
        ring.extend(seg if not ring else seg[1:])
    xs = [p[0] for p in ring]
    if max(xs) < minx:  # islas fuera del recuadro
        continue
    out, last = [], None
    for lon, lat in ring:
        x, y = proj(lon, lat)
        p = (round(x), round(y))
        if p != last:
            out.append(p)
            last = p
    if len(out) > 8:
        paths.append("M" + "L".join(f"{x},{y}" for x, y in out) + "Z")

# --- sedes por municipio
coords = {}
nombres = {}
for m in json.load(open(f"{D}/divipola.json")):
    try:
        coords[m["cod_mpio"]] = (float(m["longitud"].replace(",", ".")), float(m["latitud"].replace(",", ".")))
        nm, dp = m["nom_mpio"].title(), m["dpto"].title()
        nombres[m["cod_mpio"]] = nm if nm == dp else f"{nm}, {dp}"

    except (KeyError, ValueError):
        pass

agg = {}
for r in json.load(open(f"{D}/reps_mpio.json")):
    code = r.get("municipiosede", "").zfill(5)
    a = agg.setdefault(code, [0, 0])
    a[0] += int(r["n"])
    if r.get("ese") == "SI":
        a[1] += int(r["n"])

pts, names, sin_coord, total = [], [], 0, 0
for code, (n, ese) in agg.items():
    total += n
    if code not in coords:
        sin_coord += n
        continue
    lon, lat = coords[code]
    if not (minx <= lon <= maxx and miny <= lat <= maxy):
        continue
    x, y = proj(lon, lat)
    pts.extend([round(x, 1), round(y, 1), n, ese])
    names.append(nombres[code])

with open(OUT, "w") as f:
    f.write("// Datos públicos: REPS (datos.gov.co c36g-9fc2) por municipio, DIVIPOLA (gdxc-w37w), Natural Earth.\n")
    f.write(f"window.MAPA={{w:{W},h:{H},total:{total},municipios:{len(pts)//4},dep:{json.dumps(''.join(paths))},p:{json.dumps(pts, separators=(',', ':'))},n:{json.dumps(names, ensure_ascii=False, separators=(',', ':'))}}};\n")

print("total", total, "municipios", len(pts) // 4, "sin coordenadas", sin_coord, "alto", H, "path", sum(map(len, paths)))
