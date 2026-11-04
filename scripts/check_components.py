"""Check new YAML contracts and gallery packaging, not Power Fx execution.

Run after installing PyYAML 6.0.3 in your Python environment.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
NEW = {'form-field': 'uiFormField', 'search-filter-bar': 'uiSearchFilter',
       'message-banner': 'uiMessageBanner'}


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate keys that would otherwise silently replace formulas."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f'Duplicate YAML key: {key}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def record_fields(formula):
    # This check deliberately accepts only the literal starter record.
    literal = re.sub(r'//[^\n]*', '', formula).strip().rstrip(';')
    literal = literal[literal.index('{') + 1:literal.rindex('}')]
    return {key.strip(): value.strip() for key, value in
            (part.split(':', 1) for part in literal.split(','))}


class GalleryLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.components = set()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'Duplicate HTML id: {attrs["id"]}'
            self.ids.add(attrs['id'])
        if 'data-component' in attrs:
            self.components.add(attrs['id'])
        for attribute in ('href', 'src', 'data-gif', 'data-poster'):
            target = attrs.get(attribute, '')
            if target and not target.startswith(('http:', 'https:', 'data:', '#')):
                self.links.append(target)


def main():
    expected = record_fields((ROOT / 'examples/theme/App.Formulas.powerfx').read_text(encoding='utf-8'))
    for folder, name in NEW.items():
        source = (ROOT / folder / 'component.yaml').read_text(encoding='utf-8')
        document = yaml.load(source, Loader=UniqueKeyLoader)
        assert set(document['ComponentDefinitions']) == {name}, folder
        component = document['ComponentDefinitions'][name]
        assert component['DefinitionType'] == 'CanvasComponent', folder
        assert not component.get('AccessAppScope', False), f'{folder}: app scope must stay disabled'
        properties = component['CustomProperties']
        design = properties['Design']
        assert design['DataType'] == 'Record', folder
        assert record_fields(design['Default']) == expected, f'{folder}: Design default differs from UiTheme'
        builtins = {'Width', 'Height', 'Visible', 'Fill', 'DisplayMode', 'X', 'Y'}
        references = set(re.findall(r'\b' + name + r'\.(\w+)', source))
        assert references <= set(properties) | builtins, (folder, references - set(properties) - builtins)
        for prop, contract in properties.items():
            if contract['PropertyKind'] in {'Output', 'Action', 'OutputFunction'}:
                assert prop in component['Properties'], f'{folder}: missing formula for {prop}'
        assert not re.search(r'\b(?:ClearCollect|Collect|Patch|SubmitForm|Launch)\s*\(', source), folder
        assert (ROOT / folder / 'README.md').is_file(), folder
        print(f'PASS {folder}: YAML syntax, declared references, Design defaults, and host ownership')

    gallery = GalleryLinks()
    gallery.feed((ROOT / 'preview/index.html').read_text(encoding='utf-8'))
    folders = {file.parent.name for file in ROOT.glob('*/component.yaml')}
    assert len(folders) == 15 and gallery.components == folders, 'Catalog/gallery coverage differs'
    for link in gallery.links:
        assert (ROOT / 'preview' / link).resolve().is_file(), f'Missing gallery link: {link}'
    for folder in folders:
        assert (ROOT / 'assets/previews' / f'{folder}.gif').is_file(), folder
        assert (ROOT / 'assets/previews' / f'{folder}.png').is_file(), folder
    print(f'PASS all {len(folders)} components: gallery coverage, unique IDs, and {len(gallery.links)} local references')
    print('Native imports, Power Fx, screen readers, and component-library behavior still require Studio validation.')


if __name__ == '__main__':
    try:
        main()
    except (AssertionError, ValueError, KeyError, yaml.YAMLError) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        sys.exit(1)
