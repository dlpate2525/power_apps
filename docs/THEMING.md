# Shared theme setup

Use one host-app formula to edit the project's purple and coral palette. Bind component inputs to that formula for shared updates.

**Status:** source-reviewed setup; Power Apps Studio validation is pending. Review date: November 3, 2026. The starter supports a light palette; a coordinated dark palette is pending.

## What the shared settings control

| Name | Meaning | Behavior |
| --- | --- | --- |
| `UiTheme` | This guide's named formula record | Holds editable colors and preferences in the host app |
| `App.Theme` | Microsoft's active modern theme | Supplies native modern-control styling independently of this starter |
| Component `Theme` | An existing text input | Selects the component's internal light or dark palette |

The original 12 component `AccentColor` defaults use `#463782`. Defaults are independent fallbacks. Bind each instance to `UiTheme.Accent` to share subsequent changes.

`UiTheme` is a named formula, not mutable session state. Edit its values in **App.Formulas**; dependent formulas update automatically. See the [App object reference](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/functions/object-app#formulas-property).

The new Form field, Search and filter bar, and Message banner use a `Design` record instead of the older style inputs. Set their `Design` property to the complete `UiTheme` record.

## Set up the starter

For an existing app, enable **Settings > Updates > New > Modern controls and themes** if required by its controls.

1. Open the host app's **Formulas** property.
2. Append the formula from [App.Formulas.powerfx](../examples/theme/App.Formulas.powerfx).
3. Insert a component using its setup guide.
4. Select the component instance on the screen.
5. For the three new components, set `Design` to `UiTheme`.
6. For the original components, set `AccentColor` to `UiTheme.Accent`.
7. Set `Motion` to `UiTheme.Motion`, if that property exists.
8. Set its `Theme` property to `UiTheme.Mode`, if available.
9. Set the floating action button's `ContentColor` property to `UiTheme.OnAccent`, if used.
10. Set the Button's `Shape` property to `UiTheme.ButtonShape`, if used.
11. Set the Button's `CornerRadius` property to `UiTheme.ButtonCornerRadius`, if used.

Keep existing named formulas. Use another name if the app already defines `UiTheme`. Adjust formula separators for your authoring language.

The formulas belong on the host app and component instances. Inside reusable definitions, read the component's own inputs. Libraries cannot access host app scope. See [component scope](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/create-component#scope).

## Edit the palette in one place

Use [COLOR-PALETTE.txt](../COLOR-PALETTE.txt) to look up color names, hex codes, and uses. Its comments identify shared settings and fixed component colors. The editable formula also includes color-name comments.

Change color values in `UiTheme`, then verify every affected foreground/background pair. The starter defines these roles:

| Role | Fields and defaults | Intended use |
| --- | --- | --- |
| Primary action | `Accent` `#463782`; `OnAccent` `#FFFFFF` | Purple with white content |
| Primary hover | `AccentHover` `#362965` | Darker purple with `OnAccent` |
| Soft accent | `AccentSoft` `#ECEBF3`; `AccentBorder` `#C5BFD7` | Tinted surfaces with `Accent` text; decorative borders |
| Secondary accent | `Secondary` `#D88777`; `OnSecondary` `#292630` | Coral surfaces with dark content |
| Secondary text | `SecondaryText` `#8D4538` | Darker coral text on white or the light surface |
| Backgrounds | `Background` `#FFFFFF`; `Surface` `#F5F4F7` | Host screen and container fills |
| Text | `Text` `#292630`; `TextMuted` `#625F69` | Main and secondary text on the light backgrounds |
| Borders | `Border` `#DFDCE6`; `ControlBorder` `#625F69` | Decorative separators versus necessary control outlines |
| Focus | `Focus` `#463782` | A visible focus indicator on light backgrounds |
| Preferences | `Mode` `"Light"`; `Motion` `false` | Existing component inputs |
| Status pairs | `Error`/`ErrorSurface`, `Warning`/`WarningSurface`, `Success`/`SuccessSurface`, `Info`/`InfoSurface` | Independent text/icon and background colors for new patterns |
| Field and banner corners | `CornerRadius` `12` | Supported properties in the new components |
| Button corners | `ButtonShape` `"Pill"`; `ButtonCornerRadius` `12` | Pill default or adjustable rounded corners |

The component bindings above use `Accent`, `OnAccent`, `Mode`, `Motion`, `ButtonShape`, and `ButtonCornerRadius`. The three new components read supported fields through `Design`; their guides list native styling limits. Unused fields do not change those controls.

Set `ButtonShape` to `"Rounded"` to use the editable radius. Pill ignores `ButtonCornerRadius` and uses half the smaller dimension. See the [Button guide](../button/README.md).

For host screens, set `Fill` to `UiTheme.Background`. For supported containers, set `Fill` to `UiTheme.Surface`. Bind text and interaction properties only where the chosen control exposes them. Defining a token does not apply it automatically.

Status colors have separate variables. Success defaults to purple with a checkmark and a success label; it does not depend on color alone. Changing `Accent` does not change `Success`. The original components retain their existing internal status palettes.

### Color and interaction checks

Use **4.5:1** minimum contrast for ordinary text. WCAG permits **3:1** for large text: at least 18 pt regular or 14 pt bold. Compare unrounded ratios. [Text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)

The following calculations use opaque sRGB values. Displayed ratios are rounded; they describe these exact pairs, not complete components.

| Foreground / background | Contrast |
| --- | --- |
| `OnAccent` / `Accent` | 9.86:1 |
| `OnSecondary` / `Secondary` | 5.41:1 |
| `SecondaryText` / `Background` | 6.91:1 |
| `TextMuted` / `Surface` | 5.70:1 |

Do not use `Secondary` coral as plain text on white, or white text on coral: that pair is only **2.74:1**. Use `SecondaryText` on white or `OnSecondary` on coral.

`Border` and `AccentBorder` are decorative on white; neither reaches 3:1. Use `ControlBorder` where an outline is necessary to identify a control. Required icons and state indicators need **3:1 against adjacent colors**. [Non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)

Pair status colors with visible text, icons, or shapes. Color alone must not indicate errors, selection, or required action. [Use of color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)

Apply `Focus` to an actual outline or other persistent keyboard-focus indicator. Check its adjacent colors; a focus-color token alone creates no indicator. Keep focused controls visible beneath headers and overlays. [Focus visible](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html), [focus not obscured](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html)

Recheck pairs after changing colors, opacity, interaction states, or backgrounds. The current Button includes white primary text; other controls and SVG images contain literal colors.

## Optionally follow the modern app theme

To read Microsoft's active theme instead of the default purple, replace only the starter's `Accent` expression:

```powerfx
Accent: App.Theme.Colors.Primary
```

This is an explicit opt-in. It reads `App.Theme`; it does not change the native theme. It also does not regenerate `AccentHover`, `AccentSoft`, or other literals. Update the related pairs deliberately and recheck contrast.

Microsoft documents this theme reference and theme customization. **Lock primary color** remains preview and can reduce contrast; it is not required here. [Modern theming](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/modern-controls/modern-theming)

## Existing component limits

The original 12 components expose `AccentColor` and `Motion`. Of those, all except the floating action button expose `Theme`. Its `ContentColor` input does not replace every action-menu color.

The navigation shell's local theme takes precedence after its toggle is used; `CurrentTheme` reports the result. Set `ShowThemeToggle` to `false` on a fresh instance for this starter. Existing local state may require restarting the app session.

Changing `Mode` to `"Dark"` affects bound component inputs only. It does not switch `App.Theme` or the light host colors. Keep `Mode` at `"Light"` until a coordinated dark palette is validated.

Internal surfaces, status colors, SVG styles, typography, spacing, and corners remain component-specific. The three new components implement `Design` as a Record input. Button and KPI card still use their existing properties; extending the shared record to them remains planned. See the [roadmap](ROADMAP.md).

## Compatibility and validation

The source uses complete `ComponentDefinitions` YAML. Upstream paste instructions still need verification in Studio. Microsoft's [code-view guidance](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/code-view) supports specific Studio-generated formats, not every YAML document or paste surface.

If import fails, record the Studio version and error. Generic YAML parsing cannot validate Power Fx or Studio compatibility. The Attachments list enables `AccessAppScope` and uses shared collections; it must remain app-level or be redesigned before library distribution.

Check each control's [preview status](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/modern-controls/modern-controls-reference). [Enhanced component properties](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/component-properties) are enabled for new apps; existing apps may need the setting enabled.

Run `python scripts/check_theme.py` from the repository root. It checks 32 declared color pairs in the literal `UiTheme` light palette, including the four message states. It does not evaluate native control-generated colors. It does not require component fallback defaults to match your customized accent. Unsupported dynamic formulas or dark mode fail this limited check and require manual Studio validation. The script does not execute Power Fx or establish accessibility conformance.

1. Import the sample into a clean development app.
2. Record the Studio version and enabled features.
3. Bind the documented inputs.
4. Change a shared color and verify the rendered result.
5. Check contrast across supported interaction states.
6. Test keyboard focus and visible non-color state cues.
7. Check labels and announcements with a screen reader.
8. Inspect the running app at narrow and wide sizes.
9. Insert a second instance and check state isolation.
10. Exercise public events and outputs.
11. Record results and remaining limits before publishing a validated version.

For responsive host layouts, disable **Scale to fit**. This alone does not make component internals responsive. Follow Microsoft's [accessibility](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/accessible-apps) and [responsive layout](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/create-responsive-layout) guidance.
