"""Generate the public property reference from the component YAML files."""

import argparse
from html import escape
from pathlib import Path
import re

import yaml

from check_components import UniqueKeyLoader


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / 'docs/COMPONENT-PROPERTIES.md'


def cell(value):
    return escape(' '.join(str(value).split()), quote=False).replace('|', '&#124;').replace('`', '&#96;')


def default_cell(value, source):
    if value is None:
        return '—'
    literal = str(value)
    # Link whitespace-sensitive formulas so Markdown cannot change their literals.
    if len(literal) > 80 or re.search(r'\s{2,}|[\r\n\t]', literal):
        return f'[Source formula]({source})'
    literal = escape(literal, quote=False).replace('|', '&#124;').replace('`', '&#96;')
    return f'<code>{literal}</code>'


def render():
    lines = [
        '# Component properties', '',
        'Use this reference to configure the 15 samples without opening an external guide. '
        'Each property links to its YAML declaration.', '',
        'Generated from the current source. Descriptions express the source contract; '
        'Power Apps Studio import and runtime behavior remain unverified.', '',
        'An **input** supplies a value. An **output** exposes a value. An **event** calls a host-app formula. '
        'An **action** lets the host call component behavior. Function properties accept parameters and return values.', '',
        'Set properties on a component instance in Studio. Replace instance names in formulas with your own names.', '',
        'Start with [shared settings](THEMING.md). The original 12 components use `AccentColor`, `Motion`, '
        'and supported individual inputs. The three new components use `Design = UiTheme`.', '',
        'Keep existing Studio identifiers when updating an app. Changing a public identifier can break existing formulas.', '',
        'Long table and record defaults link to their complete source formulas, including sample field names. '
        'An em dash means no custom default is declared.', '',
        '## Index', '',
    ]
    sources = sorted(ROOT.glob('*/component.yaml'))
    for path in sources:
        title = (path.parent / 'README.md').read_text(encoding='utf-8').splitlines()[0].removeprefix('# ')
        lines.append(f'- [{title}](#{path.parent.name})')
    for path in sources:
        folder = path.parent.name
        title = (path.parent / 'README.md').read_text(encoding='utf-8').splitlines()[0].removeprefix('# ')
        text = path.read_text(encoding='utf-8')
        definitions = yaml.load(text, Loader=UniqueKeyLoader)['ComponentDefinitions']
        name, component = next(iter(definitions.items()))
        lines.extend(['', f'<a id="{folder}"></a>', '', f'## {title}', '',
                      f'**Studio name:** `{name}` · [Setup guide](../{folder}/README.md) · [Source](../{folder}/component.yaml)', '',
                      '| Property | Kind | Type / parameters | Default | Purpose |',
                      '| --- | --- | --- | --- | --- |'])
        source_lines = text.splitlines()
        for prop, contract in component['CustomProperties'].items():
            line = source_lines.index(f'      {prop}:') + 1
            source = f'../{folder}/component.yaml#L{line}'
            kind = contract['PropertyKind']
            result = contract.get('DataType', contract.get('ReturnType', 'None'))
            parameters = []
            for item in contract.get('Parameters', []):
                parameter, specification = next(iter(item.items()))
                parameters.append(f'{parameter}: {specification["DataType"]}')
            signature = f'({", ".join(parameters)}) → {result}' if parameters else result
            shown_default = default_cell(contract.get('Default'), source)
            lines.append(f'| [{prop}]({source}) | {cell(kind)} | {cell(signature)} | {shown_default} | {cell(contract.get("Description", ""))} |')
    lines.extend(['', '## Keep this reference current', '',
                  '1. Edit the component source.',
                  '2. Run `python scripts/component_reference.py --write`.',
                  '3. Run `python scripts/component_reference.py --check`.', '',
                  'Run `python scripts/check_compatibility.py` to check the original public properties. '
                  'See [preservation findings](COMPONENT-PRESERVATION.md) for the scope and remaining limits.', ''])
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true', help='Update the reference from current source.')
    mode.add_argument('--check', action='store_true', help='Fail if the reference differs from current source.')
    args = parser.parse_args()
    expected = render()
    if args.write:
        REFERENCE.write_text(expected, encoding='utf-8')
        print('Updated docs/COMPONENT-PROPERTIES.md')
    elif not REFERENCE.exists() or REFERENCE.read_text(encoding='utf-8') != expected:
        parser.exit(1, 'FAIL: property reference is stale. Run with --write after reviewing source changes.\n')
    else:
        print('PASS: property reference matches all 15 component definitions.')


if __name__ == '__main__':
    main()
