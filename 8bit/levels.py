#!/usr/bin/env python3
"""Level generator and physics checks for DILI ORBIT.

Produces the three tile maps (Grid + level1..level3) and validates them against the
jump arc read straight out of game8_template.html, so a level can never ask for a
jump the hero cannot make.
"""
import os, json, math, re

H = 17
# tile chars:
#  ' ' empty   '#' metal hull   'R' asteroid rock   '-' one-way energy platform
#  'B' crate   '?' mystery crate  'o' orb   'e' walker   'f' drone
#  '^' plasma spike   'P' spawn   'G' goal portal

class Grid:
    def __init__(self, w):
        self.w, self.h = w, H
        self.g = [[' '] * w for _ in range(H)]

    def put(self, x, y, ch):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.g[y][x] = ch

    def rect(self, x0, y0, x1, y1, ch):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.put(x, y, ch)

    def ground(self, x0, x1, top=14, ch='#'):
        self.rect(x0, top, x1, self.h - 1, ch)

    def plat(self, x0, y, ln, ch='-'):
        self.rect(x0, y, x0 + ln - 1, y, ch)

    def row_of(self, x0, x1, y, ch='o', step=2):
        for x in range(x0, x1 + 1, step):
            self.put(x, y, ch)

    def rows(self):
        return [''.join(r) for r in self.g]


def bridge(g, x0, x1, ch='#'):
    """Bridge a gap up to ground level, leaving ONE obvious two-tile pit in the middle.

    A one-tile hole next to a raised walkway is a trap (the player runs off the ledge,
    hits the walkway's side wall and slides into it), so the pit is always two tiles
    wide with flat floor on both sides.
    """
    mid = (x0 + x1) // 2
    g.rect(x0, 14, x1, g.h - 1, ch)
    g.rect(mid, 14, mid + 1, g.h - 1, ' ')
    g.plat(mid - 1, 11, 4)                      # optional high perch above the pit
    g.put(mid, 10, 'o')
    g.put(mid + 1, 10, 'o')


# ------------------------------------------------------------------ LEVEL 1
def level1():
    g = Grid(212)
    g.ground(0, 40)
    g.put(3, 13, 'P')
    g.row_of(6, 9, 12)
    g.plat(10, 11, 4)
    g.row_of(10, 13, 10)
    g.put(7, 11, '?')
    g.rect(16, 12, 17, 13, 'B')
    g.put(20, 13, 'e'); g.put(24, 13, 'e')
    g.rect(29, 13, 31, 13, '^')
    g.plat(33, 11, 5)
    g.row_of(33, 37, 10)
    bridge(g, 41, 45)

    g.ground(46, 78)
    g.put(48, 11, '?'); g.put(49, 11, '?')
    g.put(52, 13, 'e'); g.put(56, 13, 'e')
    g.plat(58, 10, 5)
    g.row_of(58, 62, 9)
    g.put(66, 7, 'f')
    g.put(70, 13, '^')
    g.rect(72, 12, 73, 13, 'B')
    bridge(g, 79, 84)

    g.ground(85, 120)
    g.row_of(87, 91, 12)
    g.plat(92, 10, 4)
    g.row_of(92, 95, 9)
    g.put(95, 13, 'e'); g.put(99, 13, 'e'); g.put(103, 13, 'e')
    g.plat(100, 8, 4)
    g.row_of(100, 103, 7)
    g.rect(106, 13, 107, 13, '^')
    g.put(110, 11, '?'); g.put(111, 11, '?')
    g.put(112, 6, 'f')
    bridge(g, 121, 126)

    g.ground(127, 168)
    g.plat(130, 10, 4)
    g.row_of(130, 133, 9)
    g.put(135, 13, 'e'); g.put(139, 13, 'e')
    g.rect(142, 13, 144, 13, '^')
    g.rect(147, 12, 148, 13, 'B')
    g.put(150, 11, '?')
    g.plat(152, 9, 5)
    g.row_of(152, 156, 8)
    g.put(160, 7, 'f')
    g.row_of(163, 166, 12)
    bridge(g, 169, 172)

    g.ground(173, 211)
    g.put(180, 13, 'e'); g.put(184, 13, 'e')
    g.put(188, 13, '^')
    g.plat(190, 10, 4)
    g.row_of(190, 193, 9)
    g.put(196, 11, '?')
    g.row_of(198, 200, 12)
    g.put(205, 13, 'G')
    return {'name': 'ORBITAL STATION', 'sub': 'Sector 1 - Outer Station', 'theme': 0,
            'width': g.w, 'rows': g.rows()}


# ------------------------------------------------------------------ LEVEL 2
def level2():
    g = Grid(232)
    segs = [(0, 26), (34, 58), (66, 92), (100, 124), (132, 158), (166, 190), (198, 231)]
    for a, b in segs:
        g.ground(a, b, 14, 'R')
    # little rock mounds for texture
    for x in (8, 12, 40, 44, 70, 104, 136, 170, 202):
        g.put(x, 13, 'R')
    g.put(3, 13, 'P')
    for (a1, b1), (a2, b2) in zip(segs, segs[1:]):   # bridge every void exactly
        bridge(g, b1 + 1, a2 - 1, 'R')

    g.row_of(6, 10, 12)
    g.put(9, 13, 'e')
    g.plat(14, 11, 4); g.row_of(14, 17, 10)
    g.rect(20, 13, 22, 13, '^')
    g.put(24, 13, 'e')
    g.put(30, 8, 'f')
    g.plat(36, 10, 5); g.row_of(36, 40, 9)
    g.put(38, 13, 'e'); g.put(42, 13, 'e')
    g.rect(46, 13, 47, 13, '^')
    g.rect(50, 12, 51, 13, 'B')
    g.put(54, 7, 'f')
    g.plat(52, 9, 3); g.row_of(52, 54, 8)
    g.put(68, 13, 'e'); g.put(72, 13, 'e'); g.put(76, 13, 'e')
    g.rect(80, 13, 82, 13, '^')
    g.put(85, 11, '?'); g.put(86, 11, '?')
    g.plat(84, 9, 4); g.row_of(84, 87, 8)
    g.put(90, 6, 'f')
    g.put(88, 13, 'R')
    g.put(102, 13, 'e'); g.put(106, 13, 'e')
    g.rect(110, 13, 111, 13, '^')
    g.plat(108, 10, 4); g.row_of(108, 111, 9)
    g.rect(114, 12, 116, 13, 'B')
    g.put(118, 8, 'f')
    g.row_of(120, 123, 12)
    g.put(134, 13, 'e'); g.put(138, 13, 'e'); g.put(142, 13, 'e')
    g.rect(146, 13, 148, 13, '^')
    g.put(150, 11, '?')
    g.plat(150, 9, 5); g.row_of(150, 154, 8)
    g.put(156, 7, 'f')
    g.put(168, 13, 'e'); g.put(172, 13, 'e')
    g.plat(174, 11, 4); g.row_of(174, 177, 10)
    g.rect(180, 13, 181, 13, '^')
    g.rect(184, 12, 185, 13, 'B')
    g.put(188, 8, 'f')
    g.row_of(200, 204, 12)
    g.put(206, 13, 'e')
    g.put(210, 11, '?')
    g.put(212, 13, '^')
    g.row_of(214, 216, 12)
    g.put(222, 13, 'G')
    return {'name': 'ASTEROID BELT', 'sub': 'Sector 2 - Asteroid Belt', 'theme': 1,
            'width': g.w, 'rows': g.rows()}


# ------------------------------------------------------------------ LEVEL 3
def level3():
    g = Grid(252)
    g.rect(0, 0, 251, 1, '#')          # mothership ceiling
    g.ground(0, 30)
    g.put(3, 13, 'P')
    g.put(8, 11, '?'); g.put(9, 11, '?')
    g.row_of(12, 16, 12)
    g.put(14, 13, 'e')
    g.plat(18, 11, 4); g.row_of(18, 21, 10)
    g.put(24, 13, 'e'); g.put(27, 13, 'e')
    g.rect(28, 13, 29, 13, '^')
    bridge(g, 31, 36)

    g.ground(37, 66)
    g.put(39, 10, 'f')
    g.rect(42, 12, 44, 13, 'B')
    g.put(46, 13, 'e'); g.put(50, 13, 'e')
    g.plat(48, 10, 5); g.row_of(48, 52, 9)
    g.put(54, 8, 'f')
    g.rect(56, 13, 58, 13, '^')
    g.put(60, 11, '?'); g.put(61, 11, '?')
    g.plat(62, 9, 4); g.row_of(62, 65, 8)
    bridge(g, 67, 72)

    g.ground(73, 104)
    g.put(75, 13, 'e'); g.put(79, 13, 'e'); g.put(83, 13, 'e')
    g.rect(86, 13, 88, 13, '^')
    g.plat(76, 11, 4); g.row_of(76, 79, 10)
    g.plat(84, 9, 4); g.row_of(84, 87, 8)
    g.put(90, 7, 'f'); g.put(96, 7, 'f')
    g.put(92, 11, '?'); g.put(93, 11, '?')
    g.rect(98, 12, 100, 13, 'B')
    g.row_of(101, 103, 12)
    bridge(g, 105, 110)

    g.ground(111, 142)
    g.put(113, 13, 'e'); g.put(117, 13, 'e')
    g.rect(120, 13, 122, 13, '^')
    g.plat(112, 10, 5); g.row_of(112, 116, 9)
    g.put(124, 8, 'f')
    g.put(126, 11, '?'); g.put(127, 11, '?'); g.put(128, 11, '?')
    g.put(130, 13, 'e'); g.put(134, 13, 'e')
    g.plat(130, 9, 5); g.row_of(130, 134, 8)
    g.put(138, 7, 'f')
    g.rect(138, 12, 140, 13, 'B')
    bridge(g, 143, 148)

    g.ground(149, 180)
    g.put(151, 13, 'e'); g.put(155, 13, 'e'); g.put(159, 13, 'e')
    g.rect(162, 13, 164, 13, '^')
    g.plat(150, 10, 5); g.row_of(150, 154, 9)
    g.put(157, 8, 'f')
    g.put(166, 11, '?')
    g.plat(166, 10, 4); g.row_of(166, 169, 9)
    g.rect(172, 12, 174, 13, 'B')
    g.put(176, 7, 'f')
    g.row_of(176, 179, 12)
    bridge(g, 181, 186)

    g.ground(187, 218)
    g.put(189, 13, 'e'); g.put(193, 13, 'e')
    g.rect(196, 13, 197, 13, '^')
    g.plat(190, 10, 5); g.row_of(190, 194, 9)
    g.put(199, 11, '?'); g.put(200, 11, '?')
    g.put(203, 8, 'f')
    g.rect(204, 12, 206, 13, 'B')
    g.row_of(208, 212, 12)
    g.put(214, 13, 'e')
    bridge(g, 219, 224)

    g.ground(225, 251)
    g.row_of(228, 232, 12)
    g.put(230, 11, '?')
    g.rect(236, 13, 238, 13, '^')
    g.plat(240, 11, 4); g.row_of(240, 243, 10)
    g.put(246, 13, 'G')
    return {'name': 'ALIEN MOTHERSHIP', 'sub': 'Sector 3 - Mothership Core', 'theme': 2,
            'width': g.w, 'rows': g.rows()}


def physics_from_template(path):
    """Read the jump constants out of the template so this check can never drift."""
    with open(path, encoding='utf-8') as f:
        t = f.read()
    g = abs(float(re.search(r'G:\s*(-?[\d.]+)', t).group(1)))
    j = abs(float(re.search(r'JUMP:\s*(-?[\d.]+)', t).group(1)))
    r = abs(float(re.search(r'MAXRUN:\s*(-?[\d.]+)', t).group(1)))
    return g, j, r


T = 16
SOLID = set('#RB?')
BEAM = '-'


def _clear(ch):
    """Beams and markers are passable; only the solid tiles block."""
    return ch not in SOLID


def reach_report(lv, rise_px, V, G, vRun):
    """Which standable surfaces and orbs can never be reached from the spawn?

    Mirrors the jump arc used by the game: the hero rises at most `rise_px`
    (measured in-game, slightly below the analytic value), and horizontal
    travel is bounded by the arc's duration at running speed.
    """
    rows = lv['rows']
    W, H = lv['width'], len(rows)

    def at(x, y):
        if x < 0 or x >= W or y < 0 or y >= H:
            return '#'                      # outside the map counts as solid
        return rows[y][x]

    nodes, index = [], {}
    for y in range(2, H):                   # two clear rows of headroom needed
        for x in range(W):
            ch = at(x, y)
            if ch not in SOLID and ch != BEAM:
                continue
            if not _clear(at(x, y - 1)) or not _clear(at(x, y - 2)):
                continue
            index[(x, y)] = len(nodes)
            nodes.append((x, y))

    def arc_dx(level_px):
        """How far sideways the hero can travel while gaining level_px of height."""
        lift = level_px + 3 if level_px > 0 else 3
        disc = V * V - 2 * G * lift
        if level_px > 0 and disc < 0:
            return -1.0
        return vRun * ((V + math.sqrt(max(disc, 0.0))) / G)

    adj = [[] for _ in nodes]
    for i, (ax, ay) in enumerate(nodes):
        for j, (bx, by) in enumerate(nodes):
            if i == j or abs(ax - bx) > 7:
                continue
            rise = (ay - by) * T              # >0: target is higher up
            if rise > rise_px:
                continue
            reach = arc_dx(rise)
            if reach >= 0 and abs(ax - bx) * T - 8 <= reach:
                adj[i].append(j)

    spawn = None
    for y in range(H):
        for x in range(W):
            if at(x, y) == 'P':
                for sy in range(y, H):
                    if (x, sy) in index:
                        spawn = index[(x, sy)]
                        break
        if spawn is not None:
            break
    assert spawn is not None, '%s: no spawn found' % lv['name']

    seen, queue = {spawn}, [spawn]
    while queue:
        i = queue.pop()
        for j in adj[i]:
            if j not in seen:
                seen.add(j)
                queue.append(j)
        ax, ay = nodes[i]
        for dx in (1, -1):
            j = index.get((ax + dx, ay))       # walking only on the same row
            if j is not None and j not in seen:
                seen.add(j)
                queue.append(j)

    bad_platforms = [nodes[i] for i in range(len(nodes)) if i not in seen]
    bad_orbs = []
    for y in range(H):
        for x in range(W):
            if at(x, y) != 'o':
                continue
            ox, oy = x * T + 8, y * T + 8
            ok = False
            for i, (nx, ny) in enumerate(nodes):
                if i not in seen:
                    continue
                need = ny * T - oy - 26        # rise needed for the hitboxes to touch
                d = max(0, abs(ox - (nx * T + 8)) - 8)
                if need <= 0 and d <= 8:
                    ok = True
                    break
                if need > rise_px:
                    continue
                reach = arc_dx(need)
                if reach >= 0 and d <= reach:
                    ok = True
                    break
            if not ok:
                bad_orbs.append((x, y))
    return bad_platforms, bad_orbs, len(nodes), len(seen)


def js(obj):
    """Serialise a level for injection into the template."""
    return json.dumps(obj, ensure_ascii=True)
