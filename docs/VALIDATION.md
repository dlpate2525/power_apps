# Local validation

These checks validate source structure, documented color pairs, and HTML previews. They do not execute Power Fx.

Run commands from the repository root.

## Source and palette

1. Install the YAML parser in your development Python environment.

```sh
python -m pip install PyYAML==6.0.3
```

2. Check the three new source contracts and gallery files.

```sh
python scripts/check_components.py
```

3. Check the 32 documented light-palette pairs.

```sh
python scripts/check_theme.py
```

The source check rejects duplicate YAML keys, mismatched theme defaults, undeclared component references, and missing gallery files. It is not a Power Apps schema validator.

## Browser preview

1. Install Playwright in your development Node environment.

```sh
npm install --no-save playwright
```

2. Install its Chromium browser.

```sh
npx playwright install chromium
```

3. Run the browser checks.

```sh
node scripts/check_gallery.cjs
```

The script checks validation, combined filters, banner actions, keyboard activation, GIF controls, and all 15 layouts at 1440, 390, and 320 pixels. It rejects JavaScript errors and external network requests.

Screenshots go to a temporary directory. Set `ARTIFACT_DIR` to save them elsewhere. Set `BROWSER_EXECUTABLE` to use an installed Chrome or Chromium browser.

## Native release checks

Complete the native checklist in [Component expansion](COMPONENT-EXPANSION.md) before describing these samples as validated for Power Apps. Record the Studio version, environment, import method, control versions, test steps, and results.

Modern Dropdown is a preview dependency. Test two instances, host bindings, keyboard focus, screen-reader announcements, and responsive height in the actual player. Test the component library in a second app before claiming library compatibility.
