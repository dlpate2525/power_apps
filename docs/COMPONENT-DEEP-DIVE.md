# Component deep dive and prioritized plan

Reviewed November 3–4, 2026. This is a source review and proposed work plan. It does not mark the components as natively validated.

**Main conclusion:** retain the existing public interface and design direction. Address compatibility, data correctness, and state handling before extending styling or packaging a reusable library.

## Scope and evidence

The review covers all **15 repository components and 335 public properties** at source snapshot [`8064433`](https://github.com/dlpate2525/power_apps/tree/8064433cbe98a6db0f1db8388d43e8c4f735e353). Reviewers read each complete component definition, setup guide, and relevant HTML gallery behavior. They compared implementation choices with Microsoft and W3C guidance.

The [preservation review](COMPONENT-PRESERVATION.md) separately compares the original 12 components with their source baseline. All **301 original public properties** remain. Retaining those declarations does not prove their implementation works.

| Evidence label | Meaning |
| --- | --- |
| Source defect | A formula or branch contradicts its declared behavior or produces an incorrect result for a concrete input. |
| Guidance conflict | The implementation conflicts with an official API rule or recommendation. Native impact is still unverified. |
| Integration or design gap | A useful scenario needs an explicit policy, host example, or additional capability. |
| Native check | Studio or the Power Apps player must establish the result. Source inspection alone cannot settle it. |

Power Apps Studio, native imports, screen-reader behavior, connector operations, and library updates were not tested. The HTML gallery and GIFs run separate demonstrations. Their passing checks do not validate Power Fx formulas.

The [original website](https://lowcodestacks.com/components) also lists released components outside this repository baseline: Breadcrumbs, Chat thread, Tag picker, and Toast. They are optional catalog additions, outside this 15-component audit.

## Priority and effort

- **P1:** resolve before calling the affected component ready for native reuse. A P1 investigation is not a confirmed runtime failure.
- **P2:** correct common behavior, accessibility, or integration problems before broader adoption.
- **P3:** useful extensions or polish after the required behavior is stable.

**Small** means a few formulas or examples. **Medium** means coordinated control or state changes. **Large** means a delivery or rendering decision. These are relative sizes, not time estimates.

## Shared findings

### G01 — Verify and replace unsupported JSON usage

**P1 guidance conflict.** Ten components call `JSON()` in **32 declarative properties: 30 Image formulas and two Items formulas**. Microsoft documents JSON as behavior-only. This is a source/API conflict; the audit did not reproduce a Studio error. [Microsoft JSON reference](https://learn.microsoft.com/en-us/power-platform/power-fx/reference/function-json)

| Component | Image properties | Items properties | First source occurrence |
| --- | ---: | ---: | --- |
| Accordion | 1 | 0 | [173](../accordion/component.yaml#L173) |
| Attachments list | 9 | 1 | [236](../attachments-list/component.yaml#L236) |
| Data table | 7 | 0 | [1082](../data-table/component.yaml#L1082) |
| Floating action button | 2 | 0 | [288](../floating-action-button/component.yaml#L288) |
| Kanban board | 2 | 0 | [363](../kanban-board/component.yaml#L363) |
| KPI card | 2 | 0 | [266](../kpi-card/component.yaml#L266) |
| Month calendar | 2 | 1 | [432](../month-calendar/component.yaml#L432) |
| Navigation shell | 2 | 0 | [468](../navigation-shell/component.yaml#L468) |
| Stepper | 2 | 0 | [346](../stepper/component.yaml#L346) |
| Tree view | 1 | 0 | [417](../tree-view/component.yaml#L417) |

Do not remove Attachments list's behavior-side JSON conversion from its save action merely because it uses the same function.

**Recommended change:** choose a supported native rendering or color-conversion path. Keep existing Color inputs and icon helpers. A behavior-produced cache must initialize and refresh after theme changes. Avoid a one-time cache that leaves stale colors. Preserve alpha when a Color input allows transparency.

**Acceptance:** import every affected component without formula errors. Change colors after initialization, reset instances, and exercise both motion settings. Record the Studio version and required features.

### G02 — Choose a supported attachment delivery path

**P1 guidance conflict and isolation risk.** The current component places a classic Attachments control outside a form. Microsoft's supported upload/delete workflow requires a form. Its modern standalone alternative is currently preview. [Classic Attachments](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/control-attachments), [modern Attachments preview](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/modern-controls/modern-control-attachments)

The definition also enables app scope and uses shared collections. Keep it labeled as an app-level sample until supported upload, instance isolation, and library delivery are established. See the [data review](component-audit/data-display.md) for save-payload and native acceptance details.

**Decision required during implementation:** retain a supported host-form workflow, or evaluate a separate standalone implementation with its dependency clearly declared. Do not silently replace the classic control with a preview control.

### G03 — Treat the gallery as design evidence

The browser gallery is useful for reviewing shape, color, motion, and representative interactions. Several demonstrations add behavior absent from the YAML. Examples include Stepper focus handling, FAB keyboard handling, and Accordion single-open reconciliation.

**Recommended change:** maintain separate evidence for native behavior and browser presentation. Add small native scenarios for empty data, live input changes, resets, event counts, and multiple instances. Keep gallery captions explicit about what they demonstrate.

### G04 — Expand theme coverage after correctness

The original components retain useful `AccentColor`, `Theme`, and `Motion` inputs. They also contain fixed surfaces, text colors, radii, and status colors. The three newer patterns consume selected fields from `Design`. The [property reference](COMPONENT-PROPERTIES.md) and [theme guide](THEMING.md) document the current boundary.

**Recommended change:** pilot optional style inputs in Button and KPI card after their behavior checks. Define precedence before introducing another theme input. Keep existing consumers working with their existing bindings. Avoid a generic rendering engine or a large record whose unused fields obscure the actual interface.

Preserve the purple, coral, red, and gray palette. Keep pill and rounded Button shapes. Use semantic names for status colors, text, borders, and surfaces. Retain text and icons that communicate status without color.

The documented light palette has 32 checked opaque pairs. White on purple is 9.86:1; ink on coral is 5.41:1. Coral on white is 2.74:1. Use the latter for decoration, not normal text or a required standalone indicator. Native generated palettes, alpha, images, dark mode, and interaction states need separate measurements. [Theme validation](THEMING.md), [W3C non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)

## Review of every component

Each linked report contains source lines, retained capabilities, findings, recommendations, and native acceptance tests. Finding labels are local to each component.

| Component | Retain | Main gap and next action | Priority / effort | Detailed evidence |
| --- | --- | --- | --- | --- |
| Button | Pill/rounded shapes, appearances, confirmation, label functions, click event | Align visible and accessible labels. Test repeated confirmation timers. Add ordinary Disabled only as an additive input. | P2 / Small | [Button](component-audit/inputs-actions.md#button--lcsbutton) |
| Floating action button | Item keys, disabled/hidden keys, placement, open/close actions | Resolve G01. Gate open-menu actions with component Disabled. Derive menu size from input data. | P1 then P2 / Medium | [FAB](component-audit/inputs-actions.md#floating-action-button--lcsfab) |
| KPI card | Value formats, comparison direction, target and trend outputs | Resolve G01. Define zero-baseline percentage policy. Render true zero target progress and textual status. | P1 then P2 / Small–medium | [KPI](component-audit/data-display.md#kpi-card) |
| Data table | Rows/Columns schema, three layouts, actions, selection | Resolve G01 and the P1 table-accessibility architecture. Correct progress ratios and narrow list geometry. | P1 then P2 / Medium–large | [Data table](component-audit/data-display.md#data-table) |
| Kanban board | Host-owned moves, card keys, columns, selection/events | Resolve G01. Make narrow columns usable and document pending/failed host moves. | P1 then P2 / Medium | [Kanban](component-audit/data-display.md#kanban-board) |
| Month calendar | Date/event inputs, host selection and navigation events | Resolve G01. Assign stable event lanes and provide accessible narrow-screen event access. | P1 then P2 / Medium | [Calendar](component-audit/data-display.md#month-calendar) |
| Attachments list | File metadata, staged actions, host-owned persistence | Resolve G02 and G01. Test shared-state isolation and save completeness before reuse. | P1 / Large | [Attachments](component-audit/data-display.md#attachments-list) |
| Accordion | Key-based open state, multiple-open mode, actions/events | Resolve G01. Normalize open keys. Clarify event policy and long-title behavior. | P1 then P2 / Medium | [Accordion](component-audit/navigation.md#accordion) |
| Carousel | Slide schema, manual controls, playback actions, host events | Guard empty data. Stop terminal playback. Bound dots and make image captions readable. | P2 / Medium | [Carousel](component-audit/navigation.md#carousel) |
| Navigation shell | Responsive modes, routes, badges, hidden/disabled keys | Resolve G01. Honor Motion for the theme icon. Clarify reset, phone overflow, and current-state labels. | P1 then P2 / Medium | [Navigation](component-audit/navigation.md#navigation-shell) |
| Stepper | Validation function, localized labels, types, public actions | Resolve G01. Align visual progress with its output. Handle empty steps and narrow validation messages. | P1 then P2 / Medium | [Stepper](component-audit/navigation.md#stepper) |
| Tree view | Flat node schema, selection, expansion, lazy-load event | Resolve G01. Wire ShowCounts. Explain the five-level limit and reconcile expansion/count state. | P1 then P2 / Medium | [Tree view](component-audit/navigation.md#tree-view) |
| Form field | Live text, blur event, host errors, deferred required feedback | Document reset on record changes. Test touched-state behavior. Add MaxLength only when a host needs it. | P2 then P3 / Small | [Form field](component-audit/inputs-actions.md#form-field--uiformfield) |
| Search and filter bar | Host-owned filtering, live query, AND example, reset order | Align the Clear all accessible name. Test option removal and retain the preview dependency notice. | P2 / Small | [Search and filters](component-audit/inputs-actions.md#search-and-filter-bar--uisearchfilter) |
| Message banner | Host-owned action/dismissal, semantic pairs, wrapping, measured height | Use stable announcement channels. Restore host focus when an action removes itself. | P2 / Medium | [Message banner](component-audit/inputs-actions.md#message-banner--uimessagebanner) |

## Prioritized work plan

This checklist is the proposed execution order. Work items are not yet implemented or filed as GitHub issues. The detailed reports define each component's acceptance cases.

### Wave 0 — Establish a reliable native baseline

- [ ] **W00: Create a native validation app.** Add all 15 samples, two-instance scenarios, host event logs, empty-data switches, and theme controls. Record supported import steps and Studio version. **P1 / Medium.**
- [ ] **W01: Resolve G01 across ten components.** Select one supported rendering pattern, then validate dynamic colors, motion, and resets. **P1 / Medium. Depends on W00.**
- [ ] **W02: Decide Attachments delivery.** Prove supported upload, complete save payloads, and isolated state. Keep the current sample's limitation visible until resolved. **P1 / Large. Depends on W00; rendering depends on W01.**
- [ ] **W02T: Decide accessible Data table delivery.** Choose a complete one-dimensional record layout or a supported table implementation. Preserve row, selection, and action contracts. **P1 / Large. Depends on W00.**

**Exit:** every sample has an observed native result. A component with unresolved import or upload behavior remains explicitly unvalidated.

### Wave 1 — Correct results and state transitions

- [ ] **W03: Fix data and progress calculations.** Preserve the true Data table numerator/denominator. Correct KPI zero-baseline display wording while preserving ChangePercent. Remove artificial zero-progress fill. Align Stepper visuals with Progress. **P2 / Small–medium. Native sign-off depends on W01.**
- [ ] **W04: Normalize state boundaries.** Guard empty Carousel/Stepper data, reject invalid keys/ordinals, honor FAB Disabled, and connect Tree ShowCounts. Stop terminal Carousel playback and define unchanged-selection event behavior. Clarify Accordion, Stepper, and Tree action/event policies before changing callback counts. **P2 / Medium.**
- [ ] **W05: Make updates predictable.** Verify Button timer restart, Form field record reset, Navigation theme reset, Gallery-derived counts, and Calendar event lanes. Document host ownership and retry behavior. **P2 / Medium.**

**Exit:** outputs agree with visuals and actual data. No action targets a nonexistent item. Reset, no-op, and callback behavior match the guide.

### Wave 2 — Complete accessibility and responsive behavior

- [ ] **W06: Repair labels, announcements, and motion.** Align Button/Search names, announce banner updates reliably, expose current/selected state, and honor Navigation Motion. Add KPI status and target text equivalents. Test with a screen reader. **P2 / Medium.**
- [ ] **W07: Resolve narrow layouts and data semantics.** Fix Stepper validation width, Data table list width, Kanban columns, Carousel dots/captions, Calendar agenda access, Attachments footer reflow, and long Accordion/Tree labels. Implement the selected table delivery. Choose and document a phone navigation pattern before adding overflow behavior. **P1 table gate; P2 other layouts / Medium–large. Table work depends on W02T.**

At 320 CSS pixels, preserve usable content and controls. Where a true two-dimensional table needs horizontal scrolling, document the reason and keep its controls reachable. Do not claim every data layout must eliminate horizontal scrolling. [W3C Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html)

**Exit:** keyboard users can complete every demonstrated task. Focus, status, and validation are perceivable. Text remains readable at narrow widths and increased text size.

### Wave 3 — Extend shared styling without losing capabilities

- [ ] **W08: Implement the Button/KPI theme pilot.** Add only required optional style inputs. Define precedence, bind the shared palette, and preserve the existing public contract. **P3 / Medium. Depends on relevant W03–W07 checks.**
- [ ] **W09: Apply the proven pattern and update previews.** Extend small groups of components. Demonstrate supported states and settings. Refresh gallery/GIFs after native behavior is verified. **P3 / Medium per group. Depends on W08.**

**Exit:** one host theme change updates every declared setting. Existing apps retain their bindings. Native and HTML evidence are clearly identified.

### Wave 4 — Package and release verified components

- [ ] **W10: Package the validated subset in a component library.** Keep persistence in the host. Test consumer imports and updates in another development environment. Publish compatibility records and known limits. **P2 release gate / Large. Depends on the relevant earlier work.**

Release components independently when their gates pass. Do not let Attachments' delivery decision hide the readiness of unrelated components. Microsoft recommends component libraries for cross-app reuse. [Component libraries](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/component-library)

## Required evidence for each completed work item

1. Record the concrete input and expected visible behavior.
2. Verify outputs and event arguments through the public interface.
3. Test empty, changed, disabled, and error states where applicable.
4. Test reset and two instances without shared-state interference.
5. Record native results separately from HTML results.
6. Run the existing compatibility and reference checks.
7. Update the setup guide with supported limits and dependency changes.

The frozen compatibility baseline protects names, types, ordered parameters, and original fixed defaults. It does not protect every behavior. Review any deliberate semantic change, such as KPI's zero-baseline output, before implementation.

## Review completion

- [x] Read all 15 component definitions and guides.
- [x] Compare original public properties with the frozen baseline.
- [x] Identify concrete gaps and preserve useful original capabilities.
- [x] Separate source evidence from native uncertainty.
- [x] Define priorities, dependencies, effort, and acceptance tests.
- [ ] Implement the proposed changes.
- [ ] Complete native validation and release evidence.
