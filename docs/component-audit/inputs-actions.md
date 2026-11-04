# Inputs and actions: deep review

[Review scope and prioritized plan](../COMPONENT-DEEP-DIVE.md)

Reviewed November 3, 2026. Scope: Button, Floating action button, Form field, Search and filter bar, and Message banner at source snapshot `8064433`.

I read each complete YAML definition and README, the repository instructions, and relevant gallery code. This report makes no source changes. Power Apps Studio and its player were unavailable.

**Evidence labels:** Static means directly visible in the source. Inference means an expected consequence, not an observed native failure. Studio unknown means the player must establish the result. P1 blocks a native release; P2 affects common use; P3 is a useful extension or clarification.

The current palette and Button pill/rounded preferences should remain. Existing names, property types, event parameters, and default behavior should remain unless a documented defect requires an internal correction. The repository currently has 335 public properties, including the additions; retaining these declarations does not prove runtime behavior.

## Button — `lcsButton`

**Purpose and strengths.** A native action control adds appearances, busy feedback, optional confirmation, and a click event. The radius calculation clamps both shapes correctly. The busy SVG uses the same dimensions and radius. `FormatLabel(Text)` and `IsValidLabel(Text)` use explicit arguments rather than hidden host state. Microsoft documents the modern Button properties used for shape, appearance, keyboard activation, and disabled behavior. [Modern Button](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/modern-controls/modern-control-button)

### B1 — Accessible name can disagree with the visible action

- **P2; high confidence; static defect; small effort.** [component.yaml:196](../../button/component.yaml#L196) derives `AccessibleLabel` from the unformatted `Label` or `ConfirmLabel`. The visible `Text` at line 163 also uses `FormatLabel` and the busy state.
- **Trigger and consequence.** Set `Label = "Save"` and make `FormatLabel` return `"Submit request"`. The visible action and accessible name differ. Busy mode also shows `Working…` while retaining another name. The first case directly conflicts with the requirement that the accessible name contain the visible label. Actual speech-control behavior remains untested. [W3C Label in Name](https://www.w3.org/WAI/WCAG22/Understanding/label-in-name.html)
- **Recommendation.** Derive the name from the same effective text as the native button. Preserve `FormatLabel` and the confirmation interface. Use a separate stable live message if busy or confirmation transitions need announcements.
- **Native acceptance.** Test a formatter that changes every word, an icon, busy mode, and confirmation. Inspect the accessible name and activate the action by its visible label. Confirm one `OnClick` per completed action.

### B2 — Confirmation timing has no explicit reset between attempts

- **P2 investigation; high confidence in the source gap, medium confidence in the consequence; small effort.** [component.yaml:129](../../button/component.yaml#L129), line 135, and line 197 only change `locArmed`. No path resets `tmrConfirm`.
- **Trigger and consequence.** Confirm near the end of a four-second window, then immediately arm again. A stopped timer may resume elapsed time rather than grant a full new window. Re-arming after expiry and resetting mid-window also need testing. This is a native hypothesis, not a reproduced failure. The HTML gallery creates a fresh `setTimeout` at [preview/index.html:1020](../../preview/index.html#L1020), so its success cannot settle this question. Microsoft treats `Start`, `Reset`, and `Repeat` as separate timer controls. [Timer reference](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/control-timer)
- **Recommendation.** Establish an explicit timer lifecycle when arming and resetting. Keep `ConfirmSeconds`, `IsArmed`, and click-count semantics. Do not silently make `Reset(instance)` reset `ClickCount`; the separate `ResetCount()` action owns that behavior.
- **Native acceptance.** Run three successive confirmation cycles, including timeout, early success, and component reset. Each new arm must receive the configured full interval. Test busy-state changes while armed and navigation away/back. Log event counts and elapsed time.

### B3 — No ordinary disabled state for an unavailable action

- **P2 design gap; high confidence; small effort.** [component.yaml:195](../../button/component.yaml#L195) disables only when `IsBusy` is true. Busy mode also replaces the text with `Working…`.
- **Trigger and consequence.** A host wants to disable Save until a required field is valid. Using `IsBusy` falsely says work is running; guarding only `OnClick` leaves an apparently enabled button that does nothing.
- **Recommendation.** Add an optional `Disabled` Boolean with default `false`. Combine it with `IsBusy` for `DisplayMode`, while keeping busy text exclusive to `IsBusy`. This is additive; all existing inputs and defaults stay valid.
- **Native acceptance.** Bind the new input to an invalid form state. Verify the original label remains, selection emits no event, and re-enabling restores keyboard activation. Test both appearances and both shapes.

**Theme boundary.** Primary text remains hardcoded white at line 184. `AccentColor` seeds a generated native palette; it does not guarantee an exact fill. The default purple/white pair is suitable, but accepting arbitrary accent colors requires checking native states. A later additive theme contract should keep the existing accent input and default foreground.

## Floating action button — `lcsFab`

**Purpose and strengths.** A main action can expand into a short list of related actions. Key/label event arguments, hidden and disabled keys, placement, and explicit open/close actions form a useful interface. Selection state is updated and the menu closes before `OnItemSelect` runs. Reset clears local open and selection state.

### F1 — SVG color conversion conflicts with the documented JSON API

- **P1; high confidence in the source/API conflict; medium effort.** [component.yaml:288](../../floating-action-button/component.yaml#L288) and [component.yaml:354](../../floating-action-button/component.yaml#L354) call `JSON(Color)` inside declarative `Image` formulas. Microsoft documents `JSON` as available only in behavior formulas. Native import or formula rejection is therefore a release risk, although no Studio error was observed here. [JSON reference](https://learn.microsoft.com/en-us/power-platform/power-fx/reference/function-json)
- **Additional static issue.** `Mid(..., 2, 7)` removes the alpha channel from JSON's eight-digit color representation. A translucent `ContentColor` would affect label opacity but not SVG icon opacity.
- **Recommendation.** Replace the internal conversion with a supported rendering path. A native icon bound directly to the color is one candidate. Preserve the public `IconSvg(Name, Stroke)` helper, icon choices, and motion preference. If conversion is cached in behavior instead, handle both initialization and later color changes explicitly.
- **Native acceptance.** Import without formula errors. Exercise every supported icon, two independent instances, and live changes to accent/content colors. Include opaque and translucent colors, menu selection, reset, and `Motion = false`.

### F2 — Disabling an open FAB does not disable its menu actions

- **P2; high confidence; static inconsistency; small effort.** [component.yaml:235](../../floating-action-button/component.yaml#L235) keeps the menu visible based only on open state and `SpeedDial`. Item `DisplayMode` at line 299 checks only `DisabledKeys`. Only the main button checks `Disabled` at line 389.
- **Trigger and consequence.** Open the menu, then set `Disabled = true` during a host operation. Its main button becomes unavailable, but enabled menu items can still emit `OnItemSelect`. Host `Open()` also opens the list while disabled.
- **Recommendation.** Define the component-wide disabled policy. At minimum, combine `Disabled` with each item predicate and guard selection. Keep `DisabledKeys` for individual exceptions. Decide explicitly whether disabling closes the menu or preserves its visual state.
- **Native acceptance.** Disable before and after opening. Test pointer and keyboard selection, all public open/close actions, and re-enabling. Neither click event may run while disabled. Disabled items must remain inactive after re-enabling the component.

### F3 — Menu height depends on loaded gallery rows

- **P2; high confidence in the dependency, medium confidence in visible failure; small effort.** [component.yaml:234](../../floating-action-button/component.yaml#L234) calculates gallery height from `Self.AllItems`. The outer component uses the full filtered input count at line 176. Microsoft states that `AllItems` contains loaded rows and can be smaller than `Items`. [Gallery reference](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/control-gallery)
- **Trigger and consequence.** Change items or hidden keys while the menu is hidden, then open it. Loaded-row count can temporarily disagree with the available actions. Larger tables increase the risk of incomplete height or unexpected scrolling; the guide recommends three to six items but does not enforce that limit.
- **Recommendation.** Use one filtered input table for both height calculations. Document the short-menu constraint. Bound `ItemHeight` before deriving row height and radius; values below eight currently produce negative child geometry at line 246. Do not add a full navigation system to this component.
- **Native acceptance.** Test 0, 1, 3, 6, and more than six items; change hidden keys while open and closed. Test both directions and narrow screens. Check long labels and `ItemHeight` values 0, 8, 24, 44, and 48. Every displayed action must remain reachable.

**Keyboard and theme checks tied to this design.** The transparent classic button overlays do not declare focus colors or thickness. Inspect focus on the main action, items, and invisible scrim at line 208; do not infer invisibility solely from omitted defaults. The HTML gallery moves focus into the list and back, and supports Escape at lines 1045–1059; the YAML implements none of those explicit steps. Microsoft does not support `SetFocus` targeting a control inside a component, so any focus plan must respect that limit. [SetFocus](https://learn.microsoft.com/en-us/power-platform/power-fx/reference/function-setfocus)

The menu retains white surfaces and blue hover/pressed overlays at lines 311 and 314. This is a documented theme limitation, not a reason to change the current purple/coral palette.

## Form field — `uiFormField`

**Purpose and strengths.** The single-line scope is useful and small. Live `Text` output, blur-based `OnChange`, independent `IsValid`, host-owned errors, and deferred required feedback are explicit. The error Label remains visible with constant `Live.Polite`. `AccessAppScope = false` protects instance isolation. The modern input's `Default`, `Text`, `TriggerOutput`, and `OnChange` usage matches current guidance. [Modern Text Input](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/modern-controls/modern-control-text-input)

### FF1 — Changing the starting value does not clear the interaction flag

- **P2 integration gap; high confidence in the state separation; small effort.** [component.yaml:110](../../form-field/component.yaml#L110) clears `ffTouched` only on component reset. The native input binds `Default` directly to `DefaultText` at line 136. Microsoft states that input controls reset when `Default` changes. [Reset reference](https://learn.microsoft.com/en-us/power-platform/power-fx/reference/function-reset)
- **Trigger and consequence.** Edit record A and blur, then rebind `DefaultText` to an empty field on record B without `Reset(instance)`. The input can reset to B while the component still considers it touched, showing B's required error immediately. This expected sequence needs native confirmation. The README explains manual reset but not record-switch ordering.
- **Recommendation.** Document a host record-switch sequence: update the host record/default, clear host error and validation-attempt state, then reset the instance. Keep `DefaultText` as a default input rather than redefining it as a continuously controlled value.
- **Native acceptance.** Switch between two records after editing, including identical defaults and empty defaults. Check text, error visibility, output validity, event count, and two instances. Verify reset does not create a user-change event.

### FF2 — No input-length boundary for common data fields

- **P3 optional gap; high confidence; small effort.** The input at [component.yaml:129](../../form-field/component.yaml#L129) exposes no `MaxLength`. The native control supports that property.
- **Trigger and consequence.** A project-name column has a fixed storage limit. The host cannot configure that limit through this interface and must validate the returned text. This is not a violation of the present contract.
- **Recommendation.** Add one optional maximum-length input if the consuming app needs it. Preserve the verified native default when no limit is supplied. Retain host `ErrorText` for business rules. Do not turn this into a generic form engine.
- **Native acceptance.** Test typing and pasting at the limit, a longer `DefaultText`, reset, and the emitted value. Verify how the native control counts non-ASCII characters before documenting a precise rule.

**Additional focused check.** The contract says “whitespace-only,” while validation uses `Trim` at lines 114 and 189 and the HTML uses JavaScript `trim()`. Microsoft's description specifies spaces. Test pasted tabs and nonbreaking spaces before claiming the same blank-text behavior on every player; this audit does not assert a mismatch. [Trim reference](https://learn.microsoft.com/en-us/power-platform/power-fx/reference/function-trim)

## Search and filter bar — `uiSearchFilter`

**Purpose and strengths.** The host owns data, delegation, and filtering; controls own input state. The AND-filter example is clear. The README correctly separates live query output from blur events, warns about count feedback cycles, and identifies the preview Dropdown dependency. Reset and disabled rules cover all three inputs. The 680-pixel breakpoint and calculated height have no evident static overflow at the documented 320-pixel minimum. Current Dropdown documentation supports `Selected.Value` and its serialized record default example. [Dropdown reference](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/modern-controls/modern-control-dropdown), [control status index](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/modern-controls/modern-controls-reference)

### S1 — Clear all's accessible name omits its complete visible phrase

- **P2; high confidence; static defect; small effort.** [component.yaml:262](../../search-filter-bar/component.yaml#L262) displays `Clear all`; line 271 names it `Clear search and all filters`. The visible phrase is split by additional words, which can obstruct activation by its visible name. [W3C Label in Name](https://www.w3.org/WAI/WCAG22/Understanding/label-in-name.html)
- **Recommendation.** Begin the accessible name with the complete visible phrase, such as `Clear all search and filters`, or use the visible text unchanged. Preserve reset order and `OnClear`.
- **Native acceptance.** Activate by voice using “Clear all,” and by keyboard. Confirm all outputs are empty before `OnClear` observes them. The action must remain disabled with the component.

**Targeted integration risks, not confirmed defects.** The source delegates selection behavior to the native dropdown when option tables change. Test removing the currently selected status/owner before documenting whether selection clears or remains stale. Options must keep the documented distinct, nonempty `Value` schema. With connector data, measure requests from the existing per-keystroke `Query` before adding debounce; preserve the current live-output contract by default. The complete `Design` record is broader than the fields consumed, but removing fields now would break its schema contract. Document consumed fields rather than replacing the interface.

## Message banner — `uiMessageBanner`

**Purpose and strengths.** The host owns resolution and dismissal. The banner uses text plus an icon for status, wraps content, exposes measured height, and avoids automatic dismissal. No local state or reset choreography is needed. The four semantic color pairs remain independent from the brand accent, which supports palette changes without changing status meaning.

### M1 — Announcement configuration changes with message severity

- **P2; high confidence in the source/guidance conflict; medium effort.** [component.yaml:141](../../message-banner/component.yaml#L141) changes `Live` between Assertive and Polite when `Intent` changes. The README's Error-to-Success example changes both message and live configuration together. Microsoft recommends stable `Live` values and persistent visible live regions. Actual missed announcements remain a screen-reader/player question. [Live-region guidance](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/accessible-apps-live-regions)
- **Recommendation.** Keep a stable announcement channel. If both urgency levels remain required, use separately mounted Labels with constant live settings and route text to the appropriate channel. Keep `Intent` and its visual mapping. Account for host hiding the whole banner; an important new message may need a persistent host announcement channel outside the hidden component.
- **Native acceptance.** With a screen reader, test Info→Warning, Error→Success, message updates without intent changes, repeated messages, dismissal, and updates while hidden. Each important new message must be announced once with appropriate urgency. Do not treat a DOM check of `aria-live` as a screen-reader test.

### M2 — The host example removes the focused action without selecting a next target

- **P2 example gap; high confidence in the source sequence, medium confidence in player focus behavior; small effort.** In [README.md:72](https://github.com/dlpate2525/power_apps/blob/8064433cbe98a6db0f1db8388d43e8c4f735e353/message-banner/README.md?plain=1#L72), `ActionLabel` becomes empty after line 73 sets the sample name. The action then hides through [component.yaml:159](../../message-banner/component.yaml#L159). Only dismissal restores focus explicitly.
- **Trigger and consequence.** Activate “Add sample name” with the keyboard. Its button disappears; the example provides no next focus target. The gallery does not exercise this exact transition: it changes the action to “View sample details” at [preview/index.html:1783](../../preview/index.html#L1783).
- **Recommendation.** Extend the host example to move focus to a suitable visible host control after an action removes itself. Keep focus ownership in the host; do not introduce app scope or an unsupported `SetFocus` call into component children.
- **Native acceptance.** Run the documented Error→Success example with keyboard only, then continue with Tab and Shift+Tab. Verify focus remains visible and logical. Repeat with Dismiss hidden, and with the host navigating after `OnAction`.

## Suggested order

1. Resolve F1 within the repository-wide JSON compatibility gate. Preserve public color and icon contracts.
2. Address F2 and the accessible-name defects B1/S1. These are small changes with concrete triggers.
3. Establish reliable announcements and focus in M1/M2. Test the native player with a screen reader.
4. Run the specific timer and gallery-size experiments B2/F3. Correct behavior only from the observed results.
5. Document FF1's host reset sequence. Add B3's ordinary disabled state when the host form uses it.
6. Consider FF2 only when a real data field supplies the length requirement.

Keep the purple/coral palette, supported pill/rounded settings, and the original event names. Do not use the successful HTML tests as evidence that these native edge cases passed.
