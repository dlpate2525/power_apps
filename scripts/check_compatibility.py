"""Check original component interfaces and defaults, without changing files.

This checks default preservation as source text, not semantic Power Fx parsing.
Only line endings and outer whitespace are normalized in default expressions.
Internal formatting, table values, and record values must stay unchanged.
AccentColor.Default is the one exception; it remains customizable.

Additional custom properties are allowed. Descriptions and display names are
not compared. Child controls and implementation formulas are outside this check.
Run with PyYAML 6.0.3 installed. No baseline-update command is provided.
"""

import argparse
import json
from pathlib import Path
import sys

import yaml

from check_components import UniqueKeyLoader


ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = Path(__file__).resolve().parent / 'baselines' / 'original-properties.json'
ORIGINAL_COMMIT = '2965dafd3df99ef942f35e7678c5238414924418'
UPSTREAM_REPOSITORY = 'https://github.com/posiauday/power-apps-components'
PROPERTY_FIELDS = ('PropertyKind', 'DataType', 'ReturnType', 'Default')
PARAMETER_FIELDS = ('DataType', 'Default')


def normalize_default(value):
    """Normalize source boundaries only; do not interpret an expression."""
    if isinstance(value, str):
        return value.replace('\r\n', '\n').replace('\r', '\n').strip()
    return value


def property_signature(property_definition):
    """Return the public signature, including ordered parameters and defaults."""
    if not isinstance(property_definition, dict):
        raise ValueError('Property definition must be a mapping')
    signature = {}
    for field in PROPERTY_FIELDS:
        if field in property_definition:
            value = property_definition[field]
            signature[field] = normalize_default(value) if field == 'Default' else value
    if 'Parameters' in property_definition:
        parameters = property_definition['Parameters']
        if not isinstance(parameters, list):
            raise ValueError('Parameters must be an ordered list')
        signature['Parameters'] = []
        names = set()
        for parameter in parameters:
            if not isinstance(parameter, dict) or len(parameter) != 1:
                raise ValueError('Each parameter must have exactly one name')
            name, definition = next(iter(parameter.items()))
            if not isinstance(name, str) or not isinstance(definition, dict):
                raise ValueError('Parameter name and definition are invalid')
            if name in names:
                raise ValueError(f'Duplicate parameter name: {name}')
            names.add(name)
            result = {'Name': name}
            for field in PARAMETER_FIELDS:
                if field in definition:
                    value = definition[field]
                    result[field] = normalize_default(value) if field == 'Default' else value
            signature['Parameters'].append(result)
    return signature


def load_baseline(path=BASELINE_PATH):
    """Read the frozen baseline. A fixture root never changes this path."""
    baseline = json.loads(Path(path).read_text(encoding='utf-8-sig'))
    if not isinstance(baseline, dict) or baseline.get('schema_version') != 1:
        raise ValueError('Unsupported compatibility baseline format')
    provenance = baseline.get('provenance', {})
    if (provenance.get('commit') != ORIGINAL_COMMIT or
            provenance.get('repository') != UPSTREAM_REPOSITORY):
        raise ValueError('Compatibility baseline provenance does not match the original source')
    components = baseline.get('components')
    if not isinstance(components, dict) or len(components) != 12:
        raise ValueError('Compatibility baseline must contain the original 12 components')
    total = 0
    for relative_path, component in components.items():
        parts = Path(relative_path).parts
        if (len(parts) != 2 or parts[1] != 'component.yaml' or
                parts[0] in {'.', '..'} or Path(relative_path).is_absolute()):
            raise ValueError(f'Invalid baseline source path: {relative_path}')
        if not isinstance(component, dict) or not isinstance(component.get('identifier'), str):
            raise ValueError(f'Invalid baseline component: {relative_path}')
        properties = component.get('properties')
        if not isinstance(properties, dict):
            raise ValueError(f'Invalid baseline properties: {relative_path}')
        total += len(properties)
    if total != 301:
        raise ValueError('Compatibility baseline must contain the original 301 properties')
    return baseline


def short_value(value):
    text = json.dumps(value, ensure_ascii=False)
    return text if len(text) <= 180 else text[:177] + '...'


def compare_values(expected, actual, location):
    """Report changed fields without treating ordered parameters as a set."""
    if type(expected) is not type(actual):
        return [f'{location}: expected {short_value(expected)}, got {short_value(actual)}']
    if isinstance(expected, dict):
        issues = []
        for field in sorted(expected.keys() | actual.keys()):
            target = f'{location}.{field}'
            if field not in actual:
                issues.append(f'{target}: missing original field')
            elif field not in expected:
                issues.append(f'{target}: field added to an original signature')
            else:
                issues.extend(compare_values(expected[field], actual[field], target))
        return issues
    if isinstance(expected, list):
        issues = []
        if len(expected) != len(actual):
            issues.append(f'{location}: expected {len(expected)} parameters, got {len(actual)}')
        for index, (old, new) in enumerate(zip(expected, actual)):
            issues.extend(compare_values(old, new, f'{location}[{index}]'))
        return issues
    if expected != actual:
        return [f'{location}: expected {short_value(expected)}, got {short_value(actual)}']
    return []


def compare_component(document, expected, source_name='component.yaml'):
    """Compare one parsed YAML document; useful for in-memory fixture checks."""
    definitions = document.get('ComponentDefinitions') if isinstance(document, dict) else None
    identifier = expected['identifier']
    if not isinstance(definitions, dict) or identifier not in definitions:
        return [f'{source_name}: missing original component identifier {identifier}']
    component = definitions[identifier]
    properties = component.get('CustomProperties') if isinstance(component, dict) else None
    if not isinstance(properties, dict):
        return [f'{source_name}: CustomProperties must be a mapping']
    issues = []
    for name, original_signature in expected['properties'].items():
        location = f'{source_name}:{identifier}.{name}'
        if name not in properties:
            issues.append(f'{location}: original property removed')
            continue
        try:
            current_signature = property_signature(properties[name])
        except ValueError as error:
            issues.append(f'{location}: {error}')
            continue
        saved_signature = dict(original_signature)
        if name == 'AccentColor':
            saved_signature.pop('Default', None)
            current_signature.pop('Default', None)
        issues.extend(compare_values(saved_signature, current_signature, location))
    return issues


def check_repository(root=ROOT, baseline=None):
    """Return failures for a repository or temporary fixture; never write files."""
    root = Path(root).resolve()
    baseline = load_baseline() if baseline is None else baseline
    issues = []
    for relative_path, expected in baseline['components'].items():
        try:
            source = (root / relative_path).read_text(encoding='utf-8-sig')
            document = yaml.load(source, Loader=UniqueKeyLoader)
            issues.extend(compare_component(document, expected, relative_path))
        except (OSError, UnicodeError, ValueError, yaml.YAMLError) as error:
            issues.append(f'{relative_path}: {error}')
    return issues


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT,
                        help='Read component files from this repository or fixture directory')
    args = parser.parse_args(argv)
    baseline = load_baseline()
    issues = check_repository(args.root, baseline)
    if issues:
        for issue in issues:
            print(f'FAIL {issue}', file=sys.stderr)
        return 1
    print('PASS original 12 components: 301 public properties, types, ordered parameters, and defaults preserved.')
    print('AccentColor defaults may change. Additional properties are allowed.')
    print('Default comparison preserves source text; it does not parse Power Fx semantics or validate runtime behavior.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, UnicodeError, ValueError, KeyError, TypeError, yaml.YAMLError) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        sys.exit(1)
