# Modern component roadmap

The goal is a reusable Power Apps library with shared design settings and evidence that each published component works.

The current change provides documentation, a host-app theme starter, and purple accent defaults in all 12 component definitions. Broader component styling and packaged library delivery remain planned work.

## 1. Validate the baseline

Start with Button and KPI card. They provide a small action pattern and a richer data-display pattern.

1. Import both samples into a clean development app.
2. Record the Studio version and enabled features.
3. Verify the shared theme setup in [THEMING.md](THEMING.md).
4. Capture any import failures and unsupported properties.
5. Record expected events, outputs, and layout limits.

**Exit condition:** another maker can follow the documented steps and reproduce the observed behavior.

## 2. Implement the theme pilot

Use one explicit style input where it reduces repeated configuration. Keep inputs small enough that an app maker can understand them without inspecting child controls.

1. Define the proposed `Design` record's fields and defaults.
2. Define precedence for existing `AccentColor`, `Theme`, and `Motion` inputs.
3. Connect internal colors, typography, spacing, and corners to the agreed fields.
4. Preserve native modern-control behavior where it meets the requirement.
5. Remove duplicate styling decisions from the two implementations.
6. Test existing consumers and the new theme input.

**Exit condition:** one host-app change updates both components for each supported shared setting. Existing behavior follows a documented compatibility policy.

Do not introduce a generic rendering engine, external configuration service, or code-component dependency without a demonstrated requirement.

## 3. Package a reusable library

Microsoft recommends [component libraries](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/component-library) for reuse across apps.

1. Move validated definitions into a component library.
2. Pass host data and style values through explicit inputs.
3. Keep connector calls and persistence in the consuming app.
4. Create a sample app that uses the published library.
5. Package the library and sample through the applicable solution workflow.
6. Document versions, dependencies, imports, and consumer updates.

**Exit condition:** a second development environment can import the package, run the sample, and accept a library update. Follow Microsoft's [component library ALM guidance](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/component-library-alm).

The Attachments list must remain an app-level sample or be redesigned before library distribution. It enables app scope and uses shared collections. Library readiness cannot be inferred from a standalone app demo.

## 4. Expand the catalog

Apply the validated pattern to the remaining components in small groups. Select each group by user need and implementation risk.

| Group | Main checks |
| --- | --- |
| Navigation shell, Stepper, Accordion | Focus order, state ownership, resizing, and events |
| Data table, Kanban board, Tree view | Data contracts, empty states, selection, and multiple instances |
| Floating action button, Carousel, Month calendar | Keyboard interaction, motion, overlays, and narrow layouts |
| Attachments list | Supported upload behavior, state isolation, save errors, and library constraints |

Modern control replacement requires behavior checks. A newer control name alone does not prove equivalent behavior or accessibility.

Built-in canvas overlay dialogs have documented focus and screen-reader limitations. Prefer a supported alternative or demonstrate an accessible implementation before release. See [Microsoft's accessibility limitations](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/accessible-apps-limitations).

## Release checks

Each component needs a short compatibility record before it receives a fork-specific validated release.

| Area | Required evidence |
| --- | --- |
| Import | Clean Studio import using the documented method |
| Environment | Validation date, Studio version, required settings, and preview dependencies |
| Interface | Input types, defaults, table schemas, outputs, events, and known limits |
| Theme | Brand change plus light/dark checks where supported |
| Accessibility | Keyboard, focus, labels, screen-reader checks, contrast, and non-color status cues |
| Layout | Narrow and wide widths, long labels, zoom, and documented minimum dimensions |
| Behavior | Success, empty, loading, disabled, and error states where applicable |
| Isolation | Two instances do not overwrite each other's state |
| Distribution | Library import and update behavior verified in a consumer app |
| Documentation | Setup steps, version notes, attribution, and reproducible examples |

Useful behavioral checks include Button busy/confirmation events and KPI empty, zero, negative, and target values. Test the public interface used by the app.

Repository checks can catch broken links and inconsistent metadata. They cannot replace Studio import or player validation.

## Contribution workflow

1. Describe the user-visible problem in a pull request.
2. Make the smallest complete change that addresses it.
3. Update the affected setup guide and compatibility record.
4. Include before-and-after behavior and verification evidence.
5. Identify any breaking changes or preview dependencies.

Retain upstream copyright and license notices. Label upstream demo links clearly when the fork's implementation differs.
