# Modern component roadmap

The goal is a reusable Power Apps library with shared design settings and evidence that each published component works.

The library contains 15 samples, shared theme settings, and pill/rounded Button options. Broader component styling and packaged library delivery remain planned work.

The [component deep dive](COMPONENT-DEEP-DIVE.md) supplies the detailed findings, priorities, dependencies, and acceptance tests. Follow its work order below. The review found compatibility and behavior gaps that precede the earlier theme pilot.

The [local gallery](../preview/index.html) provides interactive HTML previews of all 15 components. Use it to review the design before Studio validation. It does not execute the component definitions.

The [component expansion checklist](COMPONENT-EXPANSION.md) tracks Form field, Search and filter bar, and Message banner. These new patterns accept a shared `Design` record; their native Studio checks remain pending.

## 1. Validate the baseline

Create a small native validation app for all 15 components. Use Button and KPI card as initial examples, then cover every affected definition.

1. Import the samples into a clean development app.
2. Record the Studio version and enabled features.
3. Verify the shared theme setup in [THEMING.md](THEMING.md).
4. Capture any import failures and unsupported properties.
5. Resolve behavior-only JSON usage in declarative properties before native release.
6. Choose a supported attachment workflow and an accessible Data table implementation.
7. Record expected events, outputs, layout limits, and two-instance results.

**Exit condition:** another maker can reproduce each recorded result. Components with unresolved import or upload behavior remain explicitly unvalidated. See work items W00–W02T in the deep dive.

## 2. Correct behavior and state

1. Correct Data table, KPI, and Stepper progress calculations.
2. Handle empty data, invalid keys, disabled actions, and input changes.
3. Define action/event policy before changing callback counts.
4. Verify attachment save completeness and state isolation.
5. Test timers, resets, loaded-row counts, and Calendar event placement.

**Exit condition:** outputs, visible results, and event arguments agree with the documented behavior. See W03–W05.

## 3. Complete accessibility and responsive layouts

1. Align accessible names with visible labels.
2. Verify live announcements, selected-state labels, focus, and reduced motion.
3. Implement the chosen Data table accessibility approach.
4. Fix narrow layouts and provide access to overflow content.
5. Test keyboard use and screen-reader output in the native player.

**Exit condition:** each demonstrated task remains usable at supported widths and with the required assistive technology. See W06–W07.

## 4. Implement and extend the theme pilot

Use one explicit style input where it reduces repeated configuration. Keep inputs small enough that an app maker can understand them without inspecting child controls.

1. Define the proposed `Design` record's fields and defaults.
2. Define precedence for existing `AccentColor`, `Theme`, and `Motion` inputs.
3. Connect internal colors, typography, spacing, and corners to the agreed fields.
4. Preserve native modern-control behavior where it meets the requirement.
5. Remove duplicate styling decisions from the two implementations.
6. Test existing consumers and the new theme input.
7. Extend the proven pattern to small groups of components.
8. Refresh browser previews after the native behavior is verified.

**Exit condition:** one host-app change updates Button and KPI card for each supported shared setting. Existing behavior follows a documented compatibility policy. See W08–W09.

Do not introduce a generic rendering engine, external configuration service, or code-component dependency without a demonstrated requirement.

## 5. Package a reusable library

Microsoft recommends [component libraries](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/component-library) for reuse across apps.

1. Move validated definitions into a component library.
2. Pass host data and style values through explicit inputs.
3. Keep connector calls and persistence in the consuming app.
4. Create a sample app that uses the published library.
5. Package the library and sample through the applicable solution workflow.
6. Document versions, dependencies, imports, and consumer updates.

**Exit condition:** a second development environment can import the package, run the sample, and accept a library update. See W10 and Microsoft's [component library ALM guidance](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/component-library-alm).

The Attachments list must remain an app-level sample or be redesigned before library distribution. It enables app scope and uses shared collections. Library readiness cannot be inferred from a standalone app demo.

## Later catalog expansion

Add further components only after the relevant native pattern is established. Select each addition by user need and implementation risk.

| Group | Main checks |
| --- | --- |
| Navigation patterns | Focus order, state ownership, resizing, and events |
| Data patterns | Data contracts, empty states, selection, and multiple instances |
| Actions and feedback | Keyboard interaction, motion, announcements, and narrow layouts |
| File workflows | Supported upload behavior, state isolation, save errors, and library constraints |

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

Retain copyright and license notices in LICENSE. Keep component documentation focused on this fork's implementation and validation status.
