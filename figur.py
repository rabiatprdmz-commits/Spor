"""Kadın figür çizimleri (hareket rehberi için). Her hareketin başlangıç ve bitiş pozu.

Açılar ekran koordinatında derece: 0 = sağ, 90 = aşağı, -90 = yukarı, 180 = sol.
Poz: H = kalça noktası (sonradan yere oturtulur), t = kalçadan omuza açı,
legs/arms = [yakın, uzak] (yan görünüş) ya da [sol, sağ] (ön görünüş),
her bacak (uyluk, kaval, ayak), her kol (üst kol, ön kol).
face: +1 / -1 yüzün baktığı taraf (gövde yönünün sağı/solu).
"""
import math
from reportlab.graphics.shapes import Drawing, Group, Line, Circle, Rect, Polygon, String
from reportlab.lib import colors

L_TH, L_SH, L_FT, L_UA, L_FA, L_TO = 13, 12.5, 4.2, 9.5, 8.5, 18
FLOOR = 64
C = dict(skin='#e9b99c', skin2='#c99880', top='#d4506a', leg='#2f5d50', leg2='#4f7a6d',
         shoe='#ffffff', shoe2='#d9d9d9', hair='#4a3326', db='#555555', band='#2f7fd9',
         bg='#e1ead9', floor='#b9c7b3', mat='#a9c4ba', prop='#c8b49a')
col = lambda k: colors.HexColor(C[k])


def P(o, ang, ln):
    a = math.radians(ang)
    return (o[0] + ln * math.cos(a), o[1] + ln * math.sin(a))


def unit(a):
    a = math.radians(a)
    return (math.cos(a), math.sin(a))


def solve(p):
    """Eklem noktalarını hesapla."""
    H = p.get('H', (50, 40)); u = unit(p['t']); face = p.get('face', 1)
    f = (-u[1] * face, u[0] * face)  # yüz yönü (yan) / sağ taraf (ön)
    S = (H[0] + u[0] * L_TO, H[1] + u[1] * L_TO)
    J = dict(H=H, S=S, u=u, f=f, front=p.get('view') == 'front')
    J['Hd'] = (S[0] + u[0] * 7.5, S[1] + u[1] * 7.5)
    sc = p.get('scale', {})
    for i, (th, sh, ft) in enumerate(p['legs']):
        hp = H
        if J['front']:
            s = -1 if i == 0 else 1
            hp = (H[0] + f[0] * 4.3 * s, H[1] + f[1] * 4.3 * s)
        k = P(hp, th, L_TH * sc.get('th', 1)); a = P(k, sh, L_SH * sc.get('sh', 1))
        J[f'h{i}'], J[f'k{i}'], J[f'a{i}'], J[f't{i}'] = hp, k, a, P(a, ft, L_FT)
    for i, (ua, fa) in enumerate(p['arms']):
        sp = S
        if J['front']:
            s = -1 if i == 0 else 1
            sp = (S[0] + f[0] * 6.8 * s, S[1] + f[1] * 6.8 * s)
        e = P(sp, ua, L_UA * sc.get('ua', 1)); w = P(e, fa, L_FA * sc.get('fa', 1))
        J[f's{i}'], J[f'e{i}'], J[f'w{i}'] = sp, e, w
    return J


def pts_radii(J):
    out = [(J['Hd'], 5.5), (J['H'], 4.6), (J['S'], 4)]
    for i in (0, 1):
        out += [(J[f'k{i}'], 2.8), (J[f'a{i}'], 2), (J[f't{i}'], 1.4), (J[f'e{i}'], 1.6), (J[f'w{i}'], 1.6)]
    return out


def place(J, p):
    pr = pts_radii(J)
    if p.get('db'): pr += [(J['w0'], 4), (J['w1'], 4)]
    top = min(y - r for (x, y), r in pr); bot = max(y + r for (x, y), r in pr)
    if bot - top > 60:  # çerçeveye sığmıyorsa küçült
        k = 60 / (bot - top)
        for key, v in list(J.items()):
            if isinstance(v, tuple) and key not in ('u', 'f'):
                J[key] = (v[0] * k, bot - (bot - v[1]) * k)
        pr = pts_radii(J)
        if p.get('db'): pr += [(J['w0'], 4), (J['w1'], 4)]
    dy = FLOOR - max(y + r for (x, y), r in pr)
    xs = [x - r for (x, y), r in pr] + [x + r for (x, y), r in pr]
    dx = 50 - (min(xs) + max(xs)) / 2 + p.get('dx', 0)
    for k, v in list(J.items()):
        if isinstance(v, tuple) and k not in ('u', 'f'):
            J[k] = (v[0] + dx, v[1] + dy)
    return J


def seg(g, a, b, w, c):
    g.add(Line(a[0], 70 - a[1], b[0], 70 - b[1], strokeColor=c, strokeWidth=w, strokeLineCap=1))


def dot(g, a, r, c):
    g.add(Circle(a[0], 70 - a[1], r, fillColor=c, strokeColor=None))


def poly(g, ps, c):
    flat = []
    for x, y in ps: flat += [x, 70 - y]
    g.add(Polygon(flat, fillColor=c, strokeColor=None))


def torso(g, J):
    S, H, f = J['S'], J['H'], J['f']
    if J['front']:
        prof = [(0, 7.6, 7.6), (.3, 6.6, 6.6), (.62, 5.0, 5.0), (1, 7.4, 7.4)]
    else:
        prof = [(0, 3.6, 3.6), (.3, 5.0, 3.8), (.62, 3.2, 3.3), (1, 4.2, 4.8)]
    def side(s, w, sign):
        x = S[0] + (H[0] - S[0]) * s; y = S[1] + (H[1] - S[1]) * s
        return (x + f[0] * w * sign, y + f[1] * w * sign)
    fr = [side(s, a, 1) for s, a, b in prof]; bk = [side(s, b, -1) for s, a, b in prof]
    poly(g, fr + bk[::-1], col('leg'))
    # üst (atlet) göğüsten belin biraz altına
    cut = .7
    fr2 = [side(s, a, 1) for s, a, b in prof if s <= cut]; bk2 = [side(s, b, -1) for s, a, b in prof if s <= cut]
    a7 = (3.6 + (4.2 - 3.6) * 0) if not J['front'] else 5.6
    fr2.append(side(cut, 3.5 if not J['front'] else 5.4, 1)); bk2.append(side(cut, 3.6 if not J['front'] else 5.4, -1))
    poly(g, fr2 + bk2[::-1], col('top'))
    if not J['front']:
        dot(g, H, 4.5, col('leg'))


def head(g, J, p):
    Hd, u, f = J['Hd'], J['u'], J['f']
    nk = (J['S'][0] + u[0] * 2.5, J['S'][1] + u[1] * 2.5)
    seg(g, J['S'], nk, 3.4, col('skin'))
    if J['front']:
        dot(g, (Hd[0] + u[0] * .9, Hd[1] + u[1] * .9), 5.6, col('hair'))
        dot(g, (Hd[0] - u[0] * .5, Hd[1] - u[1] * .5), 4.7, col('skin'))
        top = (Hd[0] + u[0] * 6, Hd[1] + u[1] * 6)
        dot(g, top, 2.6, col('hair'))  # topuz
        return
    b = (-f[0], -f[1])
    if b[1] > .6:   # sırt üstü yatış: atkuyruğu yerde, başın üstüne doğru uzanır
        gx, gy = u
        root = (Hd[0] + u[0] * 3.5 + b[0] * 2.5, Hd[1] + u[1] * 3.5 + b[1] * 2.5)
    else:
        gx, gy = b[0] * .75, b[1] * .75 + .65
        n = math.hypot(gx, gy); gx, gy = gx / n, gy / n
        root = (Hd[0] + b[0] * 3.6 + u[0] * 2.2, Hd[1] + b[1] * 3.6 + u[1] * 2.2)
    seg(g, root, (root[0] + gx * 6.5, root[1] + gy * 6.5), 3.2, col('hair'))
    dot(g, Hd, 5.2, col('skin'))
    # saç: başın arka-üst kısmı, yüz açıkta kalır
    dot(g, (Hd[0] + b[0] * 2.3 + u[0] * 1.9, Hd[1] + b[1] * 2.3 + u[1] * 1.9), 3.6, col('hair'))
    dot(g, (Hd[0] + u[0] * 3.0 + b[0] * .6, Hd[1] + u[1] * 3.0 + b[1] * .6), 2.5, col('hair'))


def leg(g, J, i, far):
    lc = col('leg2') if far else col('leg')
    seg(g, J[f'h{i}'], J[f'k{i}'], 5.6, lc); seg(g, J[f'k{i}'], J[f'a{i}'], 4.2, lc)
    seg(g, J[f'a{i}'], J[f't{i}'], 3.2, col('shoe2')); seg(g, J[f'a{i}'], J[f't{i}'], 2.2, col('shoe') if not far else col('shoe2'))


def arm(g, J, i, far):
    c = col('skin2') if far else col('skin')
    seg(g, J[f's{i}'], J[f'e{i}'], 3.4, c); seg(g, J[f'e{i}'], J[f'w{i}'], 2.9, c)
    dot(g, J[f'w{i}'], 1.7, c)


def dumbbell(g, at, ang):
    a = math.radians(ang); d = (math.cos(a) * 2.8, math.sin(a) * 2.8)
    p1 = (at[0] - d[0], at[1] - d[1]); p2 = (at[0] + d[0], at[1] + d[1])
    seg(g, p1, p2, 1.2, col('db'))
    for q in (p1, p2):
        n = (-math.sin(a) * 2, math.cos(a) * 2)
        seg(g, (q[0] - n[0], q[1] - n[1]), (q[0] + n[0], q[1] + n[1]), 2.2, col('db'))


def lerp(a, b, t): return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def band(g, J, spec):
    kind = spec[0]; bc = col('band')
    if kind == 'cuff':
        t = spec[1]
        c0 = lerp(J['h0'], J['k0'], t); c1 = lerp(J['h1'], J['k1'], t)
        if J['front']:
            # iki uyluğun dışından dışına
            d = (c1[0] - c0[0], c1[1] - c0[1]); n = math.hypot(*d) or 1; d = (d[0] / n * 3, d[1] / n * 3)
            seg(g, (c0[0] - d[0], c0[1] - d[1]), (c1[0] + d[0], c1[1] + d[1]), 2.4, bc)
            return
        for c, h, k in ((c1, 'h1', 'k1'), (c0, 'h0', 'k0')):
            dx, dy = J[k][0] - J[h][0], J[k][1] - J[h][1]; n = math.hypot(dx, dy)
            nx, ny = -dy / n * 3.4, dx / n * 3.4
            seg(g, (c[0] - nx, c[1] - ny), (c[0] + nx, c[1] + ny), 2.2, bc)
        if math.dist(c0, c1) > 3: seg(g, c0, c1, 1.5, bc)
    elif kind == 'hands':
        seg(g, J['w0'], J['w1'], 1.8, bc)


def draw_pose(p, w=84, h=59):
    J = place(solve(p), p)
    dr = Drawing(w, h); g = Group(); g.transform = (w / 100, 0, 0, h / 70, 0, 0); dr.add(g)
    g.add(Rect(0, 0, 100, 70, fillColor=col('bg'), strokeColor=None))
    seg(g, (2, FLOOR + .6), (98, FLOOR + .6), 1.2, col('floor'))
    pr = pts_radii(J); xs = [x for (x, y), r in pr]
    if p.get('mat'):
        g.add(Rect(min(xs) - 6, 70 - FLOOR - .2, max(xs) - min(xs) + 12, 1.4, fillColor=col('mat'), strokeColor=None))
    for kind, names in p.get('props', []):
        ps = [J[n] for n in names]
        top = min(y for x, y in ps) + (2.6 if kind == 'couch' else 2.2)
        x0 = min(x for x, y in ps) - 5; x1 = max(x for x, y in ps) + (14 if kind == 'couch' else 5)
        g.add(Rect(x0, 70 - FLOOR, x1 - x0, FLOOR - top, fillColor=col('prop'), strokeColor=None))
    far = 0 if J['front'] else 1
    if not J['front']:
        arm(g, J, 1, True); leg(g, J, 1, True)
    else:
        leg(g, J, 0, False); leg(g, J, 1, False)
    if not J['front']:
        dot(g, J['S'], 2.2, col('skin'))
    torso(g, J); head(g, J, p)
    if not J['front']:
        leg(g, J, 0, False)
    for i in ((0,) if not J['front'] else (0, 1)):
        arm(g, J, i, False)
    for name, ang in p.get('db', []):
        at = J[name] if isinstance(name, str) else lerp(J[name[0]], J[name[1]], .5)
        dumbbell(g, at, ang)
    if p.get('band'): band(g, J, p['band'])
    return dr


# ---------------------------------------------------------------- pozlar
ST = dict(t=-90, legs=[(90, 90, 0), (90, 90, 0)], arms=[(90, 90), (90, 90)])
def pose(base=ST, **kw):
    d = dict(base); d.update(kw); return d

POSES = {
 'goblet': (pose(arms=[(80, -95), (85, -95)], db=[(('w0', 'w1'), 90)]),
            pose(t=-62, legs=[(12, 108, 0), (14, 108, 0)], arms=[(95, -60), (100, -60)], db=[(('w0', 'w1'), 90)])),
 'rdl': (pose(db=[('w0', 0)]),
         pose(t=-12, legs=[(84, 96, 0), (84, 96, 0)], arms=[(90, 90), (92, 92)], db=[('w0', 0)])),
 'srdl': (pose(db=[('w0', 0)]),
          pose(t=-4, legs=[(84, 96, 0), (178, 178, 95)], arms=[(90, 90), (92, 92)], db=[('w0', 0)])),
 'bridge': (pose(t=0, face=-1, legs=[(-128, 72, 180), (-126, 74, 180)], arms=[(178, 180), (178, 180)], mat=True, band=('cuff', .8)),
            pose(t=24, face=-1, legs=[(-158, 92, 180), (-156, 94, 180)], arms=[(170, 180), (170, 180)], mat=True, band=('cuff', .8))),
 'hipthrust': (pose(t=-38, face=-1, legs=[(-150, 75, 180), (-100, 175, 180)], arms=[(110, 160), (110, 160)], props=[('couch', ['S'])], db=[('H', 0)]),
               pose(t=-2, face=-1, legs=[(178, 88, 180), (-125, -170, 180)], arms=[(140, -170), (140, -170)], props=[('couch', ['S'])], db=[('H', 0)])),
 'lunge': (pose(db=[('w0', 0)]),
           pose(legs=[(5, 95, 0), (118, 172, 120)], arms=[(90, 90), (90, 90)], db=[('w0', 0)])),
 'lateral': (pose(view='front', legs=[(98, 88, 180), (82, 92, 0)], arms=[(119, 51), (61, 129)], scale=dict(th=.85), band=('cuff', .82)),
             pose(view='front', legs=[(112, 96, 180), (62, 86, 0)], arms=[(119, 51), (61, 129)], scale=dict(th=.85), band=('cuff', .82))),
 'sumo': (pose(view='front', legs=[(102, 98, 180), (78, 82, 0)], arms=[(84, 75), (96, 105)], db=[(('w0', 'w1'), 90)], band=('cuff', .82)),
          pose(view='front', legs=[(160, 100, 180), (20, 80, 0)], arms=[(88, 82), (92, 98)], db=[(('w0', 'w1'), 90)], band=('cuff', .82))),
 'donkey': (pose(t=-16, legs=[(90, 180, 180), (90, 180, 180)], arms=[(90, 90), (90, 90)], mat=True, band=('cuff', .8)),
            pose(t=-16, legs=[(-176, -88, 180), (90, 180, 180)], arms=[(90, 90), (90, 90)], mat=True, band=('cuff', .8))),
 'kpush': (pose(t=-33, legs=[(147, 180, 180), (147, 180, 180)], arms=[(90, 90), (90, 90)], mat=True),
           pose(t=-11, legs=[(169, 182, 180), (169, 182, 180)], arms=[(-165, 90), (-165, 90)], mat=True)),
 'row': (pose(t=-8, legs=[(95, 90, 0), (90, 180, 180)], arms=[(90, 90), (90, 90)], props=[('bench', ['k1', 'a1', 'w1'])], db=[('w0', 0)]),
         pose(t=-8, legs=[(95, 90, 0), (90, 180, 180)], arms=[(-160, 88), (90, 90)], props=[('bench', ['k1', 'a1', 'w1'])], db=[('w0', 0)])),
 'press': (pose(view='front', legs=[(95, 90, 180), (85, 90, 0)], arms=[(180, -90), (0, -90)], db=[('w0', 0), ('w1', 0)]),
           pose(view='front', legs=[(95, 90, 180), (85, 90, 0)], arms=[(-105, -95), (-75, -85)], db=[('w0', 0), ('w1', 0)])),
 'pull': (pose(view='front', legs=[(95, 90, 180), (85, 90, 0)], arms=[(90, 90), (90, 90)], scale=dict(ua=.3, fa=.3), band=('hands',)),
          pose(view='front', legs=[(95, 90, 180), (85, 90, 0)], arms=[(172, 178), (8, 2)], band=('hands',))),
 'plank': (pose(t=-25, legs=[(155, 180, 180), (155, 180, 180)], arms=[(90, 0), (90, 0)], mat=True),
           pose(t=-12.5, legs=[(167.5, 167.5, 100), (167.5, 167.5, 100)], arms=[(90, 0), (90, 0)], mat=True)),
 'dead': (pose(t=0, face=-1, legs=[(-90, 180, 180), (-92, 180, 180)], arms=[(-90, -90), (-92, -92)], mat=True),
          pose(t=0, face=-1, legs=[(-90, 180, 180), (-176, -178, 180)], arms=[(-25, -15), (-92, -92)], mat=True)),
 'side': (pose(view='front', t=-32, legs=[(180, 180, -90), (180, 180, -90)], arms=[(150, 30), (90, 0)], mat=True),
          pose(view='front', t=-12.5, legs=[(167.5, 167.5, -80), (167.5, 167.5, -80)], arms=[(-70, -110), (90, 0)], mat=True)),
}
LABELS = {'plank': ('Kolay: dizler yerde', 'Tam plank'), 'side': ('Kalça yerde', 'Kalça yukarıda')}

if __name__ == '__main__':  # önizleme: python3 figur.py çıktı.pdf
    import sys
    from reportlab.graphics import renderPDF
    keys = list(POSES); W, Hh = 84 * 3, 59 * 3
    dr = Drawing(2 * W + 10, len(keys) * (Hh + 12))
    for r, k in enumerate(keys):
        for c in (0, 1):
            d = draw_pose(POSES[k][c], W, Hh); g = Group(*d.contents)
            g.translate(c * (W + 10), (len(keys) - 1 - r) * (Hh + 12) + 12); dr.add(g)
        dr.add(String(2, (len(keys) - 1 - r) * (Hh + 12) + 2, k, fontSize=9))
    renderPDF.drawToFile(dr, sys.argv[1])
