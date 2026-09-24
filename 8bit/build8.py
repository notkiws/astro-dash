#!/usr/bin/env python3
"""Build dili-orbit.html: generate the tile levels and inject them into the
8-bit (256x240 / NES-style) template. Self-contained: everything it needs is in
this folder (levels.py + game8_template.html)."""
import os
import levels as L

HERE = os.path.dirname(os.path.abspath(__file__))


def check_geometry(lv, SOLID):
    rows = lv['rows']
    assert all(len(r) == lv['width'] for r in rows), lv['name']
    assert rows[0].count('P') <= 1, lv['name']
    # the hero is 19px tall on 16px tiles: his head reaches into row 12, and row 12
    # floats are invisible walls. Row 13 solids are fine (containers stand on the floor)
    for x in range(lv['width']):
        if rows[12][x] in SOLID and rows[13][x] not in SOLID:
            raise AssertionError('%s: floating row-12 solid at x=%d' % (lv['name'], x))
    # pits must be exactly two tiles: visible, jumpable, no side-wall trap
    xs = [x for x in range(lv['width']) if rows[15][x] == ' ']
    groups = []
    for x in xs:
        if groups and x == groups[-1][-1] + 1:
            groups[-1].append(x)
        else:
            groups.append([x])
    bad = [g for g in groups if len(g) != 2]
    if bad:
        raise AssertionError('%s: pit not 2 tiles wide: %s' % (lv['name'], bad))


def main():
    levels = [L.level1(), L.level2(), L.level3()]
    SOLID = set('#RB?')
    for lv in levels:
        check_geometry(lv, SOLID)

    # ---- reachability gate: nothing in the level may be impossible to reach ----
    G, V, vRun = L.physics_from_template(os.path.join(HERE, 'game8_template.html'))
    rise_px = (V * V) / (2 * G) * 0.95        # measured in-game, slightly below the analytic value
    problems = 0
    for lv in levels:
        badp, bado, total, seen = L.reach_report(lv, rise_px, V, G, vRun)
        print('  %-18s surfaces %d/%d reachable | unreachable orbs: %d'
              % (lv['name'], seen, total, len(bado)))
        if badp:
            print('     UNREACHABLE PLATFORMS:', badp[:14])
            problems += 1
        if bado:
            print('     UNREACHABLE ORBS:', bado[:14])
            problems += 1
    if problems:
        raise AssertionError('level geometry has unreachable platforms or orbs')

    body = 'const LEVELS = [\n' + ',\n'.join('  ' + L.js(lv) for lv in levels) + '\n];'
    with open(os.path.join(HERE, 'game8_template.html'), encoding='utf-8') as f:
        tpl = f.read()
    out = tpl.replace('/*%%LEVELS%%*/', body)
    assert '%%LEVELS%%' not in out
    target = os.path.join(HERE, 'dili-orbit.html')
    with open(target, 'w', encoding='utf-8') as f:
        f.write(out)
    print('sectors:', [(lv['name'], lv['width']) for lv in levels])
    print('wrote', target, os.path.getsize(target), 'bytes')


if __name__ == '__main__':
    main()
