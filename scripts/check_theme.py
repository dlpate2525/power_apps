"""Check documented light-palette pairs; does not execute Power Fx or render controls.

Uses WCAG 2.2 relative luminance:
https://www.w3.org/TR/WCAG22/#dfn-relative-luminance
"""

import argparse
from pathlib import Path
import re
import sys


def luminance(color):
    channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in channels]
    return sum(v * weight for v, weight in zip(linear, (0.2126, 0.7152, 0.0722)))


def contrast(foreground, background):
    light, dark = sorted((luminance(foreground), luminance(background)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('theme', nargs='?', type=Path,
                        default=Path(__file__).resolve().parents[1] / 'examples/theme/App.Formulas.powerfx')
    args = parser.parse_args()
    source = args.theme.read_text(encoding='utf-8-sig')
    source = re.sub(r'//[^\n]*', '', source)
    record = re.fullmatch(r'\s*UiTheme\s*=\s*\{(.*)\}\s*;\s*', source, re.S)
    if not record:
        parser.error('Expected one UiTheme record. Check dynamic or alternative formulas in Studio.')

    colors = {}
    seen_fields = set()
    mode = None
    motion = None
    for raw_field in record.group(1).split(','):
        field = raw_field.strip()
        name = field.partition(':')[0].strip()
        if name in seen_fields:
            parser.error(f'Duplicate field: {name}')
        seen_fields.add(name)
        color = re.fullmatch(r'(\w+)\s*:\s*ColorValue\("(#[0-9A-Fa-f]{6})"\)', field)
        if color:
            key, value = color.groups()
            colors[key] = value.upper()
        elif re.fullmatch(r'Mode\s*:\s*"Light"', field) and mode is None:
            mode = 'Light'
        elif re.fullmatch(r'Motion\s*:\s*(true|false)', field) and motion is None:
            motion = field
        elif re.fullmatch(r'ButtonShape\s*:\s*"(Pill|Rounded)"', field):
            pass
        elif re.fullmatch(r'ButtonCornerRadius\s*:\s*-?\d+(?:\.\d+)?', field):
            pass
        else:
            parser.error(f'Cannot evaluate {field!r}. Use literal hex colors, light mode, and literal button settings for this check.')
    if mode != 'Light' or motion is None:
        parser.error('The default record must include Mode: "Light" and a Boolean Motion value.')

    pairs = [
        ('OnAccent', 'Accent', 4.5),
        ('OnAccent', 'AccentHover', 4.5),
        ('Text', 'Background', 4.5),
        ('Text', 'Surface', 4.5),
        ('TextMuted', 'Background', 4.5),
        ('TextMuted', 'Surface', 4.5),
        ('Accent', 'Background', 4.5),
        ('Accent', 'AccentSoft', 4.5),
        ('OnSecondary', 'Secondary', 4.5),
        ('SecondaryText', 'Background', 4.5),
        ('SecondaryText', 'Surface', 4.5),
        ('Focus', 'Background', 3.0),
        ('Focus', 'Surface', 3.0),
        ('ControlBorder', 'Background', 3.0),
        ('ControlBorder', 'Surface', 3.0),
    ]
    required = {name for a, b, _ in pairs for name in (a, b)} | {'Border', 'AccentBorder'}
    if missing := required - colors.keys():
        parser.error('Missing literal color fields: ' + ', '.join(sorted(missing)))

    failures = 0
    for foreground, background, minimum in pairs:
        ratio = contrast(colors[foreground], colors[background])
        passed = ratio >= minimum
        failures += not passed
        print(f'{"PASS" if passed else "FAIL"} {foreground}/{background}: {ratio:.4f}:1 (minimum {minimum}:1)')

    print(f'\n{len(pairs) - failures}/{len(pairs)} documented light-palette pairs passed.')
    print('Secondary, Border, and AccentBorder are decorative on light surfaces; use the documented text and control colors.')
    print('These results do not validate generated control palettes, dark mode, focus geometry, or Power Apps runtime behavior.')
    return int(bool(failures))


if __name__ == '__main__':
    sys.exit(main())
