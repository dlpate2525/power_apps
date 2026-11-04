# Fork evaluation

Reviewed November 2, 2026. **Status: static source review; no Power Apps Studio run.**

The fork is a useful starting collection for reusable Power Apps canvas components. It already supports shared accent-color and motion settings. It needs a wider theme contract, documented integration limits, and Studio validation before this fork can claim a verified component release.

## Baseline and scope

The review covers all 12 component definitions and all 13 README files at commit `2965dafd3df99ef942f35e7678c5238414924418`. GitHub returned that same commit for the [fork](https://github.com/dlpate2525/power_apps/commit/2965dafd3df99ef942f35e7678c5238414924418) and [upstream](https://github.com/posiauday/power-apps-components/commit/2965dafd3df99ef942f35e7678c5238414924418) default branches before this documentation change. There was no fork-specific implementation difference to review.

This evaluation describes the baseline above. On November 3, the fork added purple accent defaults, editable host colors, and pill/rounded Button shapes. Promotional references and obsolete preview assets were removed; required copyright notices remain in LICENSE. New GIFs record the browser gallery with sample data. They do not establish native Power Apps behavior. The findings below describe the inherited baseline. A broader styling migration and Studio validation remain pending.

## What already works at the design level

- All 12 definitions expose `AccentColor` and `Motion` inputs.
- Eleven expose a `Theme` input. The floating action button exposes `ContentColor` instead.
- Custom properties have declared data types, defaults, and descriptions.
- Data inputs and events provide useful separation between presentation and host-app behavior.
- Source includes accessible labels, focus styling, and reduced-motion expressions. Their runtime behavior still needs verification.
- Each component includes source, paste instructions, a preview, and upstream attribution under the MIT license.

For example, [Button's configuration](https://github.com/dlpate2525/power_apps/blob/2965dafd3df99ef942f35e7678c5238414924418/button/component.yaml#L30) and [FAB's color inputs](https://github.com/dlpate2525/power_apps/blob/2965dafd3df99ef942f35e7678c5238414924418/floating-action-button/component.yaml#L30) already support common brand-color changes.

## Prioritized findings

### 1. Shared accent color is not a complete theme

**Observed:** neutral colors, status colors, radii, and text sizes remain embedded in individual implementations. The [KPI card's surface and radius](https://github.com/dlpate2525/power_apps/blob/2965dafd3df99ef942f35e7678c5238414924418/kpi-card/component.yaml#L173) are fixed. Its [status palette](https://github.com/dlpate2525/power_apps/blob/2965dafd3df99ef942f35e7678c5238414924418/kpi-card/component.yaml#L207) repeats across several controls. No current component definition references `App.Theme`.

**Effect:** a brand accent can change through one shared app setting. Other visual changes still require edits across implementations.

**Next change:** document the existing input bindings first. Then introduce a small theme record for the colors and dimensions that must change together. Preserve defaults and existing input names while consumers migrate. Do not claim that the existing accent input changes every color.

### 2. Attachments require separate reuse validation

**Observed:** [Attachments enables app-scope access](https://github.com/dlpate2525/power_apps/blob/2965dafd3df99ef942f35e7678c5238414924418/attachments-list/component.yaml#L5). Its [reset and outputs](https://github.com/dlpate2525/power_apps/blob/2965dafd3df99ef942f35e7678c5238414924418/attachments-list/component.yaml#L197) use the shared names `colLcsAttachStaged`, `colLcsAttachRemoved`, and `colLcsAttachPayload`. Its [OnSave contract](https://github.com/dlpate2525/power_apps/blob/2965dafd3df99ef942f35e7678c5238414924418/attachments-list/component.yaml#L166) requires the host app to save files and process removals.

**Inference:** two instances can share staging and removal state. This requires a two-instance test before reuse claims. The source alone does not establish supported component-library packaging or a complete upload integration.

**Next change:** document the shared state and host responsibilities. Isolate state through a supported interface before promoting this component for unrestricted reuse. Verify save, failure, cancellation, reset, and two simultaneous instances.

### 3. The navigation shell can take ownership of theme state

**Observed:** [CurrentTheme](https://github.com/dlpate2525/power_apps/blob/2965dafd3df99ef942f35e7678c5238414924418/navigation-shell/component.yaml#L284) uses `Coalesce(locTheme, lcsNavShell.Theme)`. The [toggle handler](https://github.com/dlpate2525/power_apps/blob/2965dafd3df99ef942f35e7678c5238414924418/navigation-shell/component.yaml#L705) sets `locTheme` and emits `OnThemeChange`.

**Effect:** after a toggle, the local value takes precedence over the external `Theme` input. Binding all components to an app setting does not by itself establish one owner for theme state.

**Next change:** disable `ShowThemeToggle` in the simple shared-setting example. Alternatively, explicitly bind other components to the shell's `CurrentTheme` output. A future controlled design should choose one owner for theme state.

### 4. Modern styling uses mixed controls

**Observed:** all 12 definitions contain modern controls. Eleven also contain classic controls. Across the files, 126 declarations start with `Modern` and 57 start with `Classic/`. Gallery, Image, Timer, and GroupContainer declarations are excluded from those counts. For example, Accordion combines [ModernText](https://github.com/dlpate2525/power_apps/blob/2965dafd3df99ef942f35e7678c5238414924418/accordion/component.yaml#L178) with a [Classic/Button](https://github.com/dlpate2525/power_apps/blob/2965dafd3df99ef942f35e7678c5238414924418/accordion/component.yaml#L204).

**Next change:** describe the current implementation accurately. Prefer supported modern controls for new work. Retain a classic control when its required behavior has no validated replacement. Record each exception and verify keyboard behavior before changing it.

### 5. Documentation and evidence do not yet support a verified release

**Observed:** component READMEs provide paste steps and external guides, but no local property reference, host wiring example, or dated compatibility record. [Button's README](https://github.com/dlpate2525/power_apps/blob/2965dafd3df99ef942f35e7678c5238414924418/button/README.md#L18) is representative. The tracked baseline contains no Studio test record, test suite, CI workflow, `.msapp`, solution package, or component-library export.

The [original root README](https://github.com/dlpate2525/power_apps/blob/2965dafd3df99ef942f35e7678c5238414924418/README.md#L31) claims paste testing and no premium license requirement. Those are upstream statements. This review did not reproduce them. Host-app data, connectors, and deployment choices must be assessed separately.

**Next change:** keep the upstream attribution. Record the Studio version, environment, exact artifact, scenarios, and results before labeling a fork release verified. Describe the YAML import instructions as an upstream workflow until tested in the target environment.

## Applying Matt Pocock's design principles

Matt's [codebase-design guidance](https://github.com/mattpocock/skills/blob/main/docs/engineering/codebase-design.md) treats a module as implementation behind an interface. An interface includes configuration, constraints, and failure behavior, not only property names.

For this fork, keep the common interface small: shared style inputs, component-specific data, and explicit events. Centralize settings that change together so one design change does not require scattered edits. Pass dependencies through inputs instead of requiring hidden app state. Verify behavior through the same properties and events that consumers use. Add abstractions only when a real variation requires them.

These principles guide the design. They do not certify Microsoft compatibility or require TypeScript tooling for Power Fx definitions.

## Acceptance gates for a verified component

| Gate | Required evidence | Current blocker |
| --- | --- | --- |
| Supported import | Import the exact artifact into the target Studio version without errors | No fork-specific Studio run |
| Common appearance | Change the shared accent, mode, and motion setting across two instances | Binding example can use existing inputs; runtime results are absent |
| Full design settings | Change surface, text, status, spacing, and radius through a documented contract | Shared contract is not implemented |
| Instance isolation | Change or reset one instance without changing the other | Attachments uses shared app collections; all instances need testing |
| Accessible interaction | Verify keyboard order, visible focus, screen-reader names, and contrast in relevant states | Source properties exist; no recorded accessibility run |
| Responsive layout | Verify documented minimum widths and phone, tablet, and desktop layouts | No recorded size matrix |
| Host integration | Verify documented event arguments, data shapes, empty states, and failure recovery | No integration record; attachments requires host persistence |
| Release traceability | Record artifact version, control versions, import method, test date, and known limits | No fork release package or validation record |

Start with Button and KPI card to prove shared styling. Expand to navigation after theme ownership is explicit. Validate attachments separately before advertising broad library reuse. These are proposed next steps, not completed implementation or test results.
