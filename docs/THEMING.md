# Shared theme setup

Use one host-app formula to supply the style inputs that the existing components already expose. This starter does not change their internal YAML.

**Status:** source-reviewed example; Power Apps Studio validation is pending. Review date: November 2, 2026.

## Three different meanings of theme

| Name | Meaning | Current behavior |
| --- | --- | --- |
| `App.Theme` | Microsoft's active modern theme object | Provides the app's brand ramp and font |
| `UiTheme` | The host-app record defined by this guide | Supplies values to component inputs |
| Component `Theme` | An existing text input | Selects that component's internal light or dark palette |

Microsoft documents `App.Theme.Colors.Primary` for styling controls from the active theme. Modern controls normally follow the app theme, but explicit property formulas can override that behavior. See [modern theming](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/modern-controls/modern-theming).

Setting `UiTheme.Mode` to `"Dark"` does not switch `App.Theme` or make every control dark. It only affects bound component inputs.

## Set up the starter

For an existing app, enable **Settings > Updates > New > Modern controls and themes** if required. The available settings depend on the app and environment.

1. Select a modern theme in your development app.
2. Open the app's **Formulas** property.
3. Append the formula from [App.Formulas.powerfx](../examples/theme/App.Formulas.powerfx).
4. Insert a component using its setup guide.
5. Select the component instance on the screen.
6. Set its `AccentColor` property to `UiTheme.Accent`.
7. Set its `Motion` property to `UiTheme.Motion`.
8. Set its `Theme` property to `UiTheme.Mode`, if available.
9. Set the floating action button's `ContentColor` property to `UiTheme.OnAccent`, if used.

Keep existing named formulas when adding this one. Use another name if the app already defines `UiTheme`. Adjust formula separators for your authoring language.

Use named formulas for derived configuration. Use variables for values that users change during a session. Microsoft explains named formulas in the [App object reference](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/functions/object-app#formulas-property).

The formulas belong on the host app and its component instances. Do not add references to host-app globals inside a reusable component definition. Component libraries cannot access host app scope. Pass values through input properties instead. See [component scope](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/create-component#scope).

## Change the brand color

Choose or customize the modern app theme. The `UiTheme.Accent` formula follows its primary color.

For a component palette that deliberately differs from the app theme, replace the `Accent` expression in the starter:

```powerfx
Accent: ColorValue("#0F6CBD")
```

This changes the bound components only. It does not update the app's modern theme. Prefer the active theme as the shared source when both should match.

Check foreground and background colors together. The starter's white `OnAccent` value is an example, not a guarantee of contrast on any brand color. The current Button also specifies white text in its primary state. Test the actual rendered control after changing its palette.

Microsoft's **Lock primary color** setting is marked preview and can affect contrast. It is not required by this starter. See [modern theming](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/modern-controls/modern-theming).

## Current property coverage

| Inputs | Components |
| --- | --- |
| `AccentColor`, `Theme`, `Motion` | Accordion, Attachments list, Button, Carousel, Data table, Kanban board, KPI card, Month calendar, Navigation shell, Stepper, Tree view |
| `AccentColor`, `ContentColor`, `Motion` | Floating action button |

The floating action button has no `Theme` input. Its `ContentColor` input does not replace all colors in its action menu.

The navigation shell keeps a local theme after its toggle is used. That local value takes precedence over its `Theme` input; `CurrentTheme` reports the result. For the starter, set `ShowThemeToggle` to `false` on a fresh instance before testing. Existing local state may require restarting the app session.

A future runtime theme switch needs one clear owner for mode state. Updating the shared mode, navigation output, and native app theme must be tested together.

## What remains component-specific

The existing controls contain literal colors, corner sizes, font sizes, and spacing. Binding the four starter values does not change those literals.

Examples include the KPI card's surface color and 20-pixel corners, the Button's confirmation color, and status colors in the Data table. SVG images also embed style values.

For your own screen containers, put repeated spacing and typography values in named formulas. Bind supported container or text properties to those formulas. Existing component internals need a separate implementation change before they can consume those values.

## Proposed component interface

The next implementation should pilot one **Record input**, provisionally named `Design`, on Button and KPI card. A Record groups related values into one input.

| Proposed group | Example fields | Purpose |
| --- | --- | --- |
| Colors | `Accent`, `OnAccent`, `Surface`, `Text`, `Border` | Common brand and neutral colors |
| Status | `Success`, `Warning`, `Error` and matching foregrounds | Meaningful status presentation |
| Typography | `Font`, `BodySize` | Shared readable text |
| Layout | `Space`, `CornerRadius` | Common spacing and corners |
| Behavior | `Mode`, `Motion` | Explicit display preferences |

This is a proposal, not an input that exists today. The pilot must confirm which fields both components need. Avoid adding fields without a demonstrated use.

The implementation must define field types, defaults, and supported values. It must also specify precedence between the new record and existing inputs. Preserve existing behavior through a documented migration path.

Native modern-control themes should remain the starting point. Add custom styling only where the reusable pattern needs it. Do not wrap a native control unless the module hides useful repeated behavior.

## Compatibility and validation

The source uses `ComponentDefinitions` YAML. Each folder contains upstream paste instructions, but this fork has not repeated those steps in Studio.

Microsoft's [code-view documentation](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/code-view) supports specific Studio-generated YAML. That does not establish that every complete component definition can be pasted through every code-view surface. Treat a successful import as an explicit compatibility check.

If import fails, capture the Studio version and error. Resolve the format in a development app before changing the published sample. Generic YAML parsing does not validate Power Fx or Studio compatibility.

The Attachments list sets `AccessAppScope: true` and uses app collections. It needs separate work before library distribution or multiple-instance support can be claimed.

Check availability per control. Microsoft marks some modern controls or features as preview. See the [modern control reference](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/modern-controls/modern-controls-reference).

The dedicated [component-properties documentation](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/component-properties) says enhanced properties are enabled for new apps. Existing apps may need the setting enabled. Check your environment instead of relying on older experimental labels.

### Minimum manual checks

1. Import the sample into a clean development app.
2. Record the Studio version, environment settings, and component version.
3. Bind the properties listed in this guide.
4. Change the app theme and verify the rendered accents.
5. Change `Mode` and verify both palettes where supported.
6. Check contrast in default, focused, selected, disabled, and error states.
7. Test all interactive controls using the keyboard.
8. Check labels and state announcements with a screen reader.
9. Test the running app at different window sizes and orientations for clipping and reading order.
10. Insert a second instance and check state isolation.
11. Exercise the component's public events and outputs.
12. Record results and known limits before publishing a validated version.

For responsive host layouts, disable **Scale to fit**. This setting alone does not make the existing component internals responsive.

Use [Microsoft's accessibility guidance](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/accessible-apps) and [responsive layout guidance](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/create-responsive-layout). An accessibility checker pass does not replace keyboard and assistive-technology testing.
