# Component preservation review

Reviewed November 3, 2026. This is a source comparison, not a Power Apps Studio test.

## Result

All **301 original public properties** remain in the 12 inherited components. Their names, kinds, types, ordered parameters, and non-color defaults are unchanged.

The intentional changes are the 12 purple `AccentColor` defaults and the Button's added `Shape` and `CornerRadius` inputs. Its busy animation follows the selected corners. These changes preserve the original event and state formulas.

The [property reference](COMPONENT-PROPERTIES.md) now lists the full interface of all 15 local components. Each property links to its source, including complete table and record defaults.

## Evidence and scope

The comparison uses the [original source at commit `2965daf`](https://github.com/posiauday/power-apps-components/tree/2965dafd3df99ef942f35e7678c5238414924418) and this fork after [PR #3](https://github.com/dlpate2525/power_apps/pull/3). The original repository's `main` still resolved to that commit during this review.

The [original catalog](https://lowcodestacks.com/components) lists 16 released components and 15 planned components. Its four additional released patterns are Breadcrumbs, Chat thread, Tag picker, and Toast. They are outside the 12-component source baseline reviewed here. This fork adds Form field, Search and filter bar, and Message banner, for 15 local samples.

The current website and the pinned source repository do not have identical catalog coverage. The website's Studio test claims are not validation evidence for this fork. Detailed website guides were accessible for KPI card and Stepper; the source comparison covers all 12 inherited definitions.

| Component | Original properties retained | Useful configuration and behavior retained |
| --- | ---: | --- |
| [Accordion](COMPONENT-PROPERTIES.md#accordion) | 13 | Item table, one/multiple open sections, open keys, toggle actions |
| [Attachments](COMPONENT-PROPERTIES.md#attachments-list) | 27 | File rules, staging/removal payloads, upload event, reset actions |
| [Button](COMPONENT-PROPERTIES.md#button) | 16 | Four appearances, icon, busy state, timed confirmation, click event |
| [Carousel](COMPONENT-PROPERTIES.md#carousel) | 21 | Slide table, autoplay, pause, navigation, change/select events |
| [Data table](COMPONENT-PROPERTIES.md#data-table) | 30 | Columns, rows, layouts, badge styles, sorting and selection |
| [Floating action button](COMPONENT-PROPERTIES.md#floating-action-button) | 22 | Icon, label, content color, menu actions and placement |
| [Kanban board](COMPONENT-PROPERTIES.md#kanban-board) | 24 | Columns/cards, limits, move events and keyboard interaction |
| [KPI card](COMPONENT-PROPERTIES.md#kpi-card) | 22 | Number format, comparison, target and status behavior |
| [Month calendar](COMPONENT-PROPERTIES.md#month-calendar) | 20 | Start of week, event table, visible month and selection |
| [Navigation shell](COMPONENT-PROPERTIES.md#navigation-shell) | 43 | Menu table, layout, breakpoint, selection and theme events |
| [Stepper](COMPONENT-PROPERTIES.md#stepper) | 34 | Steps, validation hook, navigation actions and completion state |
| [Tree view](COMPONENT-PROPERTIES.md#tree-view) | 29 | Flat node table, hierarchy, expansion and selection |

The total comprises 181 inputs, 59 outputs, 29 events, 28 actions, two input functions, and two output functions. Source identifiers remain stable so existing formulas can keep using them. Required notices remain in [LICENSE](../LICENSE).

## Practices to preserve

**Pass settings through public inputs.** Retain `AccentColor`, `Motion`, `Theme`, and FAB `ContentColor`. Add settings without silently removing existing names or changing types. Microsoft distinguishes data, functions, events, and actions; they are not interchangeable. [Component properties](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/component-properties)

**Keep app responsibilities explicit.** The host supplies data and handles persistence through events. Component actions and local variables handle interaction state. Libraries cannot read host app scope. Preserve the Attachments exception in its documentation until it is redesigned and tested. [Component scope](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/create-component#scope)

**Use one host theme record.** Bind existing inputs to `UiTheme`; bind the three new components through `Design`. Named formulas recalculate from dependencies. They do not replace mutable selection, confirmation, or open/closed state. [App formulas](https://learn.microsoft.com/en-us/power-platform/power-fx/reference/object-app#formulas-property)

**Keep status meaning separate from color.** Preserve KPI `GoodWhen`, Stepper health values, and table badge keys when changing rendered colors. A decrease can be good for costs and bad for revenue. Keep the existing value rules and change the visual settings independently. See the [KPI](COMPONENT-PROPERTIES.md#kpi-card), [Stepper](COMPONENT-PROPERTIES.md#stepper), and [Data table](COMPONENT-PROPERTIES.md#data-table) contracts.

**Keep the native theme distinction.** The component's text `Theme` input is separate from `App.Theme`. A palette seed can generate other colors. Keep exact-color and contrast claims limited to the pairs actually checked. [Modern themes](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/modern-controls/modern-theming)

**Preserve interaction and accessibility behavior.** Keep native buttons, accessible names, keyboard focus, non-color state cues, and motion controls. Retain classic Labels when they supply live announcements. Test the actual player before claiming accessible behavior. [Accessible apps](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/accessible-apps), [live regions](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/accessible-apps-live-regions)

**Preserve layout inputs.** Keep breakpoint, orientation, width, and layout choices. Disabling host Scale to fit does not make every internal layout responsive. [Responsive layout](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/create-responsive-layout)

**Verify import and distribution separately.** Control code view, extracted source YAML, theme YAML, and component libraries have different workflows. Retaining source does not establish a supported paste route or a library release. [Code view](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/code-view), [source formats](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/power-apps-yaml), [component libraries](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/component-library)

## Editable settings and remaining limits

Use [the palette file](../COLOR-PALETTE.txt) for hex values and names. Edit [App.Formulas.powerfx](../examples/theme/App.Formulas.powerfx) for shared defaults. Follow [the binding guide](THEMING.md) to connect each instance.

| Setting | Current behavior |
| --- | --- |
| `UiTheme.Accent` | Drives the original 12 components when their `AccentColor` inputs are bound |
| `UiTheme.Motion` | Controls the original 12 `Motion` inputs when bound; the shared starter uses `false` |
| `UiTheme.Mode` | Drives 11 component theme inputs; a coordinated host dark palette is still pending |
| `UiTheme.OnAccent` | Can bind FAB `ContentColor`; it does not recolor every legacy foreground |
| `UiTheme.ButtonShape` / `ButtonCornerRadius` | Selects pill or rounded Button corners when bound |
| Full `UiTheme` record | Supplies the three new components' `Design` inputs; supported fields are documented in their guides |

Legacy surfaces, status colors, typography, and most corner sizes remain internal. The original properties have been retained; a complete shared styling contract has not yet been implemented. See [the theme pilot](ROADMAP.md#2-implement-the-theme-pilot).

The navigation shell can override its `Theme` input after its toggle is used. Keep `ShowThemeToggle = false` on a fresh instance for the simple host-owned setup. Attachments uses shared app collections and still needs an isolation review. These inherited behaviors were preserved, not resolved by the documentation work.

The browser gallery demonstrates selected interactions with sample data. It is not a complete native demonstration of all 301 original properties. Use the local reference for advanced settings and verify them in Studio.

Host integration still matters: Data table emits sort requests; the host sorts its data. Kanban emits `OnMove`; the host updates `Cards`. Attachments prepares `StagedFilesData` during save; the host handles persistence and failure. Preserve these event contracts when adapting the samples.

## Repeat the checks

Install the parser described in [Validation](VALIDATION.md), then run these commands from the repository root:

1. Run `python scripts/check_compatibility.py` to compare the original public declarations with the fixed baseline.
2. Run `python scripts/component_reference.py --check` to detect an outdated property reference.
3. Run `python scripts/check_components.py` to check the three new definitions and gallery coverage.
4. Run `python scripts/check_theme.py` to check the 32 documented light-palette color pairs.

The compatibility check allows additive properties and configurable accent defaults. It rejects missing original properties and changes to their kinds, types, parameters, and other declared defaults. Review a deliberate breaking change and its migration before changing the frozen baseline.

These checks do not execute Power Fx, validate table data semantically, test event timing, or prove accessibility. Complete the [native validation checks](VALIDATION.md#native-release-checks) before publishing a validated component release.
