#!/usr/bin/env python3
"""Build astro-dash-8bit.html: reuse the tile levels from ../build.py, inject into the
8-bit (256x240 / NES-style) template."""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import build as levels_src          # noqa: E402  (level generator lives one level up)


def main():
    levels = [levels_src.level1(), levels_src.level2(), levels_src.level3()]
    SOLID = set('#RB?')
    for lv in levels:
        rows = lv['rows']
        assert all(len(r) == lv['width'] for r in rows), lv['name']
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
    body = 'const LEVELS = [\n' + ',\n'.join('  ' + json.dumps(lv) for lv in levels) + '\n];'
    with open(os.path.join(HERE, 'game8_template.html'), encoding='utf-8') as f:
        tpl = f.read()
    out = tpl.replace('/*%%LEVELS%%*/', body)
    assert '%%LEVELS%%' not in out
    target = os.path.join(HERE, 'astro-dash-8bit.html')
    with open(target, 'w', encoding='utf-8') as f:
        f.write(out)
    print('sectors:', [(lv['name'], lv['width']) for lv in levels])
    print('wrote', target, os.path.getsize(target), 'bytes')


if __name__ == '__main__':
    main()
