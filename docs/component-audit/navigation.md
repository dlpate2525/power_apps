# Navigation component deep review

[Review scope and prioritized plan](../COMPONENT-DEEP-DIVE.md)

Reviewed 3 November 2026. Scope: Accordion, Carousel, Navigation shell, Stepper, and Tree view in fork snapshot `8064433`. The original source baseline is `2965dafd3df99ef942f35e7678c5238414924418`.

This review read each complete component YAML, README, and relevant browser gallery markup and behavior. It also read the project instructions and domain rules. It made no repository changes. The report contains recommendations, not an implementation plan already approved for execution.

**Evidence boundary:** source findings identify formulas, missing branches, or fixed dimensions. They do not establish successful import or reproduce native behavior. Power Apps Studio was unavailable. The HTML gallery uses separate implementations and cannot validate these formulas. Native acceptance tests below remain necessary.

P1 means a compatibility gate before native release. P2 means a meaningful correctness, integration, or usability issue. P3 means useful refinement. Confidence distinguishes observable source facts from their likely native effect. Effort is relative: small changes affect a few formulas; medium changes affect several controls or contracts; large changes need a different implementation approach.

## Priorities across this group

| Order | Work | Priority | Effort |
|---|---|---|---|
| 1 | Resolve the shared `JSON()` formula compatibility question in Studio. | P1 gate | Medium |
| 2 | Guard Carousel empty data; align Stepper progress; connect Tree view's count visibility input. | P2 | Small |
| 3 | Define valid state for Accordion, Stepper, and Tree view, including data replacement and resets. | P2 | Medium |
| 4 | Make narrow layouts usable; decide how phone navigation exposes overflow routes. | P2 | Medium |
| 5 | Make current selection and validation changes available to assistive technology. | P2 | Medium |
| 6 | Document event policy, host-owned data, lazy loading, and playback boundaries with examples. | P2/P3 | Small–medium |
| 7 | Extend theme tokens and gallery demonstrations after native semantics are stable. | P3 | Medium |

Preserve public property names and types, existing useful actions, and MIT attribution. Keep the purple/coral/red/gray palette and rounded or pill controls. New style inputs should be optional. Avoid replacing original capabilities merely to match the smaller HTML samples.

### Shared compatibility gate

Four reviewed components call `JSON()` in an Image formula: [Accordion:173](../../accordion/component.yaml#L173), [Navigation shell:468](../../navigation-shell/component.yaml#L468), [Navigation shell:481](../../navigation-shell/component.yaml#L481), [Stepper:346](../../stepper/component.yaml#L346), [Stepper:539](../../stepper/component.yaml#L539), and [Tree view:417](../../tree-view/component.yaml#L417).

Microsoft documents `JSON()` as usable only in behavior functions. An Image property is a declarative formula. This is a source/documentation conflict, **not a reproduced import failure**. Treat it as the shared G01 gate, not four unrelated bugs. Verify the formulas in the target Studio version before deciding on a supported color-to-SVG method. Preserve dynamic color updates; a one-time cached color would introduce stale themes. [Microsoft JSON reference](https://learn.microsoft.com/en-us/power-platform/power-fx/reference/function-json#description)

**Native acceptance:** import each affected component, inspect formula errors, change AccentColor and Theme after initialization, and test Motion both ways. Record the Studio version and the actual outcome.

## Accordion

### Purpose and strengths

The component reveals text sections and supports one or several open sections. It provides key-based actions, state outputs, and an event. The body uses AutoHeight, and the gallery supports varying row heights. A native button provides a focus border and includes the expanded state in its text. These are useful foundations to retain. See [state and layout:98](../../accordion/component.yaml#L98), [header:203](../../accordion/component.yaml#L203), and [body:228](../../accordion/component.yaml#L228).

### A1. Open state can include missing or duplicate sections

**P2 · High source confidence · Medium effort.** `OpenCount` counts nonblank tokens, not distinct keys present in Items. `Toggle` accepts any trimmed text. Defaults are used without normalization. With two real sections, `DefaultOpenKeys="a,a,missing"` reports three open sections although only one real row matches. `Toggle("missing")` emits an event for a nonexistent section. With `MultipleOpen=false`, a default containing two real keys still opens both. [Outputs and actions:98](../../accordion/component.yaml#L98)

**Recommendation:** derive one valid set of unique, nonempty keys present in Items. Apply the single-open rule to initialization, reset, actions, and input changes. Keep the comma-separated output format. Document that keys must be unique and cannot contain its separator. Define what happens when an open item disappears.

**Native acceptance:** supply duplicate, missing, and blank keys; reset the instance; replace Items after opening a row. Open two rows, then change MultipleOpen to false. Outputs must agree with visible rows, and invalid actions must not create phantom events.

### A2. Event meaning does not cover every state change

**P2 integration risk · High confidence in source asymmetry; medium confidence in intended policy · Small effort.** The event description says it runs when a section opens or closes. `Toggle` emits one event for the requested key. Opening B in single-open mode silently closes A. `ExpandAll` and `CollapseAll` emit no events. A host that mirrors open state only through OnToggle can retain stale state. [Contract:59](../../accordion/component.yaml#L59), [implementation:104](../../accordion/component.yaml#L104)

**Recommendation:** choose and document an event policy before changing it. Either emit events for every affected row, or explicitly make OnToggle an interaction notification and require hosts to read OpenKeys. Avoid silently changing event counts for existing consumers.

**Native acceptance:** log OnToggle while opening A, opening B, expanding all, and collapsing all. Check the chosen policy, event order, and final OpenKeys.

### A3. Long headers cannot grow with their text

**P3 · High confidence in fixed geometry; native clipping needs verification · Medium effort.** The title and click area are both 56 pixels high. The body starts at Y=56. At narrow widths, long or translated titles can exceed the available header area. Only the body has AutoHeight. [Title:177](../../accordion/component.yaml#L177), [header and body:203](../../accordion/component.yaml#L203)

**Recommendation:** let a measured header height position the body and size the button. Keep rounded tiles and the full title in the accessible name. Add optional localized expanded/collapsed labels instead of the fixed English suffixes.

**Native acceptance:** test 320-pixel width, a three-line title, large text, and a long body. Expansion must keep the title, body, and next row separate. Confirm reading order when a section opens.

**Gallery coverage:** the HTML sample covers multiple-open mode and bulk actions. It actively closes extra rows when MultipleOpen changes, unlike the YAML formula. It does not exercise invalid keys or callback semantics. [Gallery behavior:1475](../../preview/index.html#L1475)

## Carousel

### Purpose and strengths

The component presents picture or color slides with captions, manual navigation, autoplay, and host events. Native button overlays retain full slide text and meaningful dot labels. Manual arrow and dot selections pause playback. Its Motion description correctly says reduced animation does not stop slide changes. Preserve that distinction. [Contract:13](../../carousel/component.yaml#L13), [slide button:275](../../carousel/component.yaml#L275), [dot labels:456](../../carousel/component.yaml#L456)

### C1. Empty Items produces invalid Index calls

**P2 · High confidence from source and Microsoft reference · Small effort.** CurrentIndex becomes 1 when Items is empty. CurrentKey and several image, caption, and button formulas then call `Index(Items,1)`. With Loop enabled, Next and Previous also invoke Index on the empty table. Microsoft specifies that Index returns an error for an empty table or out-of-range index. This affects normal asynchronous loading and empty search results. [State/actions:156](../../carousel/component.yaml#L156), [image:215](../../carousel/component.yaml#L215), [caption:248](../../carousel/component.yaml#L248), [Microsoft Index reference](https://learn.microsoft.com/en-us/power-platform/power-fx/reference/function-first-last#description)

**Recommendation:** define an empty state, guard every row lookup, and disable navigation and the timer without slides. Keep output types; document the no-slide values. Reject non-integer GoTo values. Emit change events only for valid selected rows.

**Native acceptance:** start with a typed empty table, add slides, remove the final row, then restore data. Call all navigation actions while empty. Confirm no formula errors, invalid events, or active timer.

### C2. Playback state is misleading at the non-looping end

**P2 · High source confidence · Small effort.** With AutoPlay=true and Loop=false, Next stops changing the index at the final slide. It does not clear the playing state. IsPlaying remains true, the timer repeats, and the control still offers Pause. With one looping slide, Next emits OnChange on every tick although the selection stays the same. [Playing state and Next:158](../../carousel/component.yaml#L158), [timer:200](../../carousel/component.yaml#L200), [play label:405](../../carousel/component.yaml#L405)

**Recommendation:** stop playback at the terminal slide when Loop=false. Avoid change events for an unchanged selection. Define whether Play at the end restarts or remains stopped. Also clarify that AutoPlay currently acts as a master enable: Play cannot start playback while AutoPlay=false. Keep existing action names and make this distinction explicit.

**Native acceptance:** test zero, one, and three slides with both Loop values. Check IsPlaying, control text, timer callbacks, and event counts. Test Pause, Play, Reset, and leaving and re-entering the screen. Timer navigation behavior should follow its documented AutoPause and AutoStart settings. [Microsoft Timer reference](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/control-timer)

### C3. Dot navigation exceeds the component width

**P2 · High confidence in geometry · Medium effort.** Dot width is `28 * CountRows(Items)`, centered without a maximum width. Twelve slides need 336 pixels; in a 320-pixel component the gallery starts at X=-8. Twenty slides need 560 pixels. The formula supplies no wrapping or overflow choice. [Dot gallery:424](../../carousel/component.yaml#L424)

**Recommendation:** bound the dots within the component, or show a compact page window with a current-slide count. Keep GoTo and keyboard-operable native buttons. Define the supported minimum width and a deliberate long-sequence treatment.

**Native acceptance:** use 3, 12, and 20 slides at widths 320 and 480. Every slide must remain reachable, with visible focus and no controls outside the component.

### C4. Picture captions need a readable surface and length policy

**P2 design risk · High confidence in source; rendered contrast and truncation need native verification · Medium effort.** Arbitrary image URLs sit behind white text. The shade fades from transparent to 65% black across 120 pixels. The title begins only 36 pixels into that gradient. The title is one fixed 30-pixel line, and body text has 40 pixels. Bright pictures and longer text are not constrained by the input contract. [Caption shade:227](../../carousel/component.yaml#L227), [caption geometry:240](../../carousel/component.yaml#L240)

**Recommendation:** provide a caption surface and text color through optional style inputs. Use a dependable contrast treatment for any image. Either measure caption height or document and validate the supported length. Keep the current rounded frame and palette.

**Native acceptance:** use a white image, a bright detailed image, long localized captions, and 320-pixel width. Measure text contrast on the rendered result. Check full text access with keyboard and screen reader.

**Motion and ownership:** Motion=false deliberately leaves autoplay running. This is documented, not a new bug. ShowPause=false also removes the built-in pause control. Document that a host choosing that combination must provide an accessible Pause action. Do not promise focus-based pause through unsupported custom focus events. Microsoft states that canvas apps cannot detect focus entering or leaving controls. [Pause visibility:394](../../carousel/component.yaml#L394), [Microsoft focus limitations](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/accessible-apps-limitations#focus-management)

**Gallery coverage:** the HTML sample is explicitly manual. It covers previous/next, dots, and simulated selection. It provides no evidence for native timer, reset, end-of-sequence, or image-caption behavior. [Gallery:649](../../preview/index.html#L649), [manual behavior:1063](../../preview/index.html#L1063)

## Navigation shell

### Purpose and strengths

One menu supports wide-screen side navigation and a phone bottom bar. The host supplies the current screen and performs navigation through OnNavigate. Hidden and disabled keys, badges, user details, collapse actions, theme events, and layout outputs are useful original capabilities. The component keeps routing outside its implementation. [Inputs:6](../../navigation-shell/component.yaml#L6), [events and layout:229](../../navigation-shell/component.yaml#L229)

### N1. Phone mode silently omits routes after MaxBottomItems

**P2 integration limitation, not an undocumented formula bug · High confidence · Medium effort.** The contract explicitly limits bottom items, and the gallery uses FirstN. A host with six visible routes and the default limit of five loses access to the sixth route through this menu after narrowing the screen. A CurrentKey outside the first five has no visible selected item. [MaxBottomItems contract:67](../../navigation-shell/component.yaml#L67), [bottom Items:736](../../navigation-shell/component.yaml#L736)

**Recommendation:** document the route limit in setup examples. Offer an optional overflow entry that opens a host-owned navigation screen, or require a host-provided phone menu. Do not simply increase the limit until touch targets become unusable. Preserve Items and OnNavigate.

**Native acceptance:** use seven routes, a disabled route, and a hidden route. Resize across the breakpoint while on route seven. All permitted destinations must remain reachable through the chosen host pattern.

### N2. Local theme overrides cannot be cleared through the public interface

**P2 integration limitation, already documented · High source confidence · Medium effort.** CurrentTheme prefers locTheme forever after the theme button sets it. Turning ShowThemeToggle off later does not release the override. No OnReset or reset action clears local selection, theme, or collapse state. The current README correctly recommends a fresh instance for host-owned themes. [State precedence:282](../../navigation-shell/component.yaml#L282), [theme event:703](../../navigation-shell/component.yaml#L703), [documented limitation](https://github.com/dlpate2525/power_apps/blob/8064433cbe98a6db0f1db8388d43e8c4f735e353/docs/THEMING.md?plain=1#L112)

**Recommendation:** retain the existing default behavior but add an explicit reset/release path. Document controlled Theme/CurrentKey behavior separately from internal fallback state. Reset should restore input defaults and clear stale selections when the host requests it. Use the standard component OnReset hook where supported. [Microsoft component reset guidance](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/component-behavior#onreset)

**Native acceptance:** toggle the theme, change the host Theme, disable the toggle, and invoke the documented reset. Repeat with two instances to verify isolation. Replace Items after selecting an item and verify the defined fallback behavior.

### N3. Motion=false does not suppress the theme-icon animation

**P2 · High source confidence; SVG playback still requires Studio verification · Small effort.** The main selection animations honor Motion. The theme image always embeds animation styles, without testing Motion. It only honors the SVG reduced-motion media query. A host that sets Motion=false still supplies animated SVG markup when switching themes. [Theme image:673](../../navigation-shell/component.yaml#L673)

**Recommendation:** gate the theme SVG animation with the same Motion input. Keep a static sun or moon state. Preserve the device reduced-motion fallback.

**Native acceptance:** switch themes with Motion=false and with device reduced motion enabled separately. Confirm the icon changes state without animation. Repeat with Motion=true to verify the intended short animation.

### N4. Current screen is only reflected visually in menu items

**P2 accessibility risk · High source confidence; announcement requires native verification · Small effort.** The side and bottom buttons contain only the label and badge text. Their text does not include the current state, although the adjacent icon and highlight change. The browser sample exposes `aria-pressed`; that is not evidence for native selection announcements. [Side button:567](../../navigation-shell/component.yaml#L567), [bottom button:817](../../navigation-shell/component.yaml#L817), [browser state:1499](../../preview/index.html#L1499)

**Recommendation:** add an optional localized current-item suffix to the native accessible label. Include meaningful badge context where the host supplies it. Keep each destination a native button. Microsoft recommends expressing custom state in accessible labels because custom roles and states are unavailable. [Microsoft accessibility limitations](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/accessible-apps-limitations#custom-roles-and-states)

**Native acceptance:** use keyboard and a screen reader in expanded, collapsed, and bottom modes. The current destination, badge meaning, and disabled items must be clear without seeing the highlight.

**Gallery coverage:** the HTML menu demonstrates four routes and responsive placement. It does not cover collapse, Premium look, host-controlled current state, hidden/disabled keys, theme switching, overflow, or the native layout outputs. Add focused demonstrations after those native contracts are verified. [Gallery:803](../../preview/index.html#L803)

## Stepper

### Purpose and strengths

The component supports form steps, project stages, and approval chains. It separates host validation through CanLeaveStep from its own navigation state. GoToStep checks each intervening step. Localizable labels and state words help hosts describe progress. Standard/Premium and horizontal/vertical choices are useful original capabilities. [Contract:18](../../stepper/component.yaml#L18), [validation and actions:235](../../stepper/component.yaml#L235)

### S1. The displayed progress bar disagrees with Progress

**P2 · High source confidence · Small effort.** Progress is `(CurrentStep-1)/count`, matching its description of completed steps. Both rendered bars use `CurrentStep/count`. With four steps at step one, Progress is zero while the bar is 25% filled. At step four, the bar is full before final validation or OnFinish. [Output:233](../../stepper/component.yaml#L233), [static bar:516](../../stepper/component.yaml#L516), [animated bar:536](../../stepper/component.yaml#L536)

**Recommendation:** drive both visual bars from the same completed-step value as Progress. Keep the existing output meaning. Treat successful form submission as host-owned; add an explicit completion input or action only if that state is needed in the component.

**Native acceptance:** compare Progress and bar width at every step in all three Types, with Motion on and off. Project/Approval at count+1 should show full completion. A form awaiting final validation must not look fully complete.

### S2. Public actions and built-in controls have different event policies

**P2 integration risk · High confidence in source asymmetry; medium confidence in intended contract · Small–medium effort.** Next, Back, and GoToStep update local state without invoking OnStepChange. Native Back/Next and earlier-step buttons invoke it. ShowButtons explicitly invites host buttons that call Back and Next. A host replacing the built-in buttons can therefore stop receiving events it previously used for focus, loading, or tracking. This may be intentional suppression of programmatic events; the documentation does not resolve it. [ShowButtons:54](../../stepper/component.yaml#L54), [actions:235](../../stepper/component.yaml#L235), [native Back:640](../../stepper/component.yaml#L640), [native Next:677](../../stepper/component.yaml#L677)

**Recommendation:** specify the event policy and show a host-button example. If parity is intended, use one internal transition path and emit once only when the step changes. Preserve Next's explicit promise that it does not finish. Do not add duplicate callbacks to hosts that already handle programmatic transitions.

**Native acceptance:** log callbacks for built-in and host Next/Back, GoToStep, blocked forward jumps, and no-op actions. Check old/new values and exact event counts against the documented policy.

### S3. Narrow layout can hide the validation explanation

**P2 · High confidence in geometry; screen-reader outcome needs Studio testing · Medium effort.** The blocked label width is `Max(0, Width-300)`. At width 300 it disappears; at 320 it has only 20 pixels. Changing Orientation to Vertical does not change this footer layout. The label is hidden entirely when ShowButtons=false, and no blocked-state output is provided. It is a ModernText control with no configured live announcement. [Blocked label:591](../../stepper/component.yaml#L591), [footer buttons:609](../../stepper/component.yaml#L609)

**Recommendation:** stack or wrap the footer below a defined width. Reserve full-width space for BlockedText. Provide an optional blocked-step/message output for host-owned buttons. Use a supported announcement pattern for failed validation. Microsoft documents classic Label live regions for this purpose; do not assume ModernText provides the same property. [Microsoft live-region guidance](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/accessible-apps-live-regions)

**Native acceptance:** fail CanLeaveStep at widths 280, 320, and 720 in both orientations. The reason must be readable and announced. Repeat with ShowButtons=false and a host button. Long translated messages must remain available.

### S4. Empty and fractional step values create fictitious states

**P2 · High source confidence · Small effort.** CurrentStep forces a minimum of one even when Steps is empty. StepCount is zero, but the progress label uses a minimum total of one. The Next button can run CanLeaveStep(1) and OnFinish on the empty table. DefaultStep and GoToStep accept fractional numbers without normalization, so no integer-numbered row matches a value such as 1.5. [Outputs:228](../../stepper/component.yaml#L228), [GoToStep:237](../../stepper/component.yaml#L237), [progress label:485](../../stepper/component.yaml#L485), [finish branch:677](../../stepper/component.yaml#L677)

**Recommendation:** define a no-steps state and suppress validation/submission when no real step exists. Validate integer step numbers at the boundary. Retain the documented count+1 completion position for Project and Approval. Document that ordinal steps must remain stable during an active form, or explicitly reset when Steps changes.

**Native acceptance:** test empty and one-row Steps, DefaultStep=1.5, negative/oversized values, GoToStep(2.5), and removal of the current step. No nonexistent step should validate or submit.

**Theme and ownership:** Project/Approval status colors are hard-coded separately from AccentColor. This follows the preserved contract but cannot fully follow the user's palette through current inputs. Plan optional semantic color inputs after correctness fixes. Keep status words and check/cross indicators. Host examples should own form data, submission, validation details, and focus. [Status colors:326](../../stepper/component.yaml#L326)

**Gallery coverage:** the HTML sample adds a host form, validation focus, completion screen, and restart. Its completed-step progress is internally consistent. The note correctly assigns form content and completion to the sample. It does not demonstrate Project/Approval, public-action event policy, or the native blocked footer. [Gallery:834](../../preview/index.html#L834), [progress and focus behavior:1532](../../preview/index.html#L1532)

## Tree view

### Purpose and strengths

The component converts a flat parent/key table into an ordered, indented list. It keeps data loading in the host through OnExpand. Separate expand and select buttons support different actions. It includes labels for expand/collapse and level, an empty message, selected record output, and bulk expansion actions. Preserve these capabilities and the distinction between browsing and opening an item. [Contract:6](../../tree-view/component.yaml#L6), [events:144](../../tree-view/component.yaml#L144)

### T1. ShowCounts does not hide the count control

**P2 · High source confidence · Small effort.** ShowCounts affects only space reserved beside the node label. `lblCount` has no Visible formula and always displays `Text(ThisItem.Kids)`. Turning ShowCounts off leaves counts visible while enlarging the label into their space. Leaves also receive a zero count. [Label width:509](../../tree-view/component.yaml#L509), [count control:521](../../tree-view/component.yaml#L521)

**Recommendation:** connect count visibility to ShowCounts and the intended folder/count condition. Use the same condition for label spacing. Preserve the input and count meaning.

**Native acceptance:** toggle ShowCounts with loaded folders, empty folders, lazy folders, and leaves. Counts must disappear without leaving overlap or unnecessary reserved space.

### T2. Hierarchy silently stops after five levels

**P2 · High source confidence · Medium effort for explicit bounds; large for arbitrary depth.** The gallery builds only l0 through l4. Depth-four nodes can still report children and show an expand button, but their descendants are never included. A six-level path therefore presents an expand action that cannot reveal the sixth level. Neither the Nodes contract nor README documents this bound. Orphaned/cyclic data can also yield an empty gallery while EmptyText remains hidden because Nodes itself is nonempty. [Final expansion level:326](../../tree-view/component.yaml#L326), [merged levels:342](../../tree-view/component.yaml#L342), [toggle visibility:459](../../tree-view/component.yaml#L459), [empty condition:574](../../tree-view/component.yaml#L574)

**Recommendation:** document a supported maximum depth and reject or explain deeper data. For the initial fix, stop presenting unavailable expansion and offer a host-owned drill-down screen. Validate unique keys, parent existence, and cycles in the host. If arbitrary depth becomes a requirement, evaluate a different flattening strategy without silently breaking the Nodes schema.

**Native acceptance:** provide six nested levels, an orphan, a cycle, and duplicate keys. The component must either render supported data or show a clear supported-limit/error state. No visible expand control should lead to an unexplained dead end.

### T3. VisibleCount depends on gallery loading

**P2 integration risk · High confidence in documented control semantics; medium confidence in intended count meaning · Small effort.** VisibleCount is `CountRows(galTree.AllItems)`. Microsoft says AllItems contains loaded rows and can grow as the user scrolls. It is not a reliable count of every row included by the expanded hierarchy. A host using it for totals or height can change behavior because of scrolling. [Output:214](../../tree-view/component.yaml#L214), [Microsoft Gallery reference](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/control-gallery#additional-properties)

**Recommendation:** define VisibleCount as the number of rows in the flattened expanded table and count that table directly. If loaded rows were intended, clarify the existing contract before changing it and add a separate count for expanded rows.

**Native acceptance:** create enough expanded nodes to require several screens of scrolling. Compare VisibleCount before and after scrolling. The chosen total must match its documented meaning and remain stable when only the viewport changes.

### T4. Programmatic expansion does not run the lazy-load event

**P2 integration risk · High source confidence; medium confidence in intended event policy · Small–medium effort.** The Expand action only changes locExpanded. The user toggle changes that state and invokes OnExpand. ExpandAll explicitly says it does not invoke OnExpand, but Expand does not explain that distinction. Calling Expand for a HasChildren node with unloaded children can show an open folder with no new content. There is also no reset hook to restore defaults after a host changes datasets. [Action contract:177](../../tree-view/component.yaml#L177), [actions:215](../../tree-view/component.yaml#L215), [user toggle:480](../../tree-view/component.yaml#L480)

**Recommendation:** document whether programmatic actions emit events. Provide a host lazy-loading example with loaded/loading/error state and duplicate-request protection. Keep ExpandAll's existing no-event promise. Add an explicit reset path that restores defaults and reconciles selected/expanded keys with a replacement dataset. Document comma and semicolon restrictions while the implementation uses delimiter strings.

**Native acceptance:** compare clicking a lazy node with calling Expand. Simulate delayed loading, failure, repeated expansion, and data replacement. Verify event counts, retry behavior, and two-instance isolation.

### T5. Selection is absent from the node's accessible text

**P2 accessibility risk · High source confidence; native announcement needs verification · Small effort.** The node button text includes label, level, and child count, but never selected state. Selection changes only the surrounding visual treatment. The HTML example uses `aria-pressed`, so its behavior does not validate the native component. [Node button:544](../../tree-view/component.yaml#L544), [browser selection:1577](../../preview/index.html#L1577)

**Recommendation:** add an optional localized selected-state label. Describe this canvas implementation as an expandable list with native buttons. Do not promise an ARIA tree with arrow-key navigation; canvas apps cannot implement arbitrary keyboard handling or custom roles. A true composite tree would require a different control approach. [Microsoft keyboard and role limitations](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/accessible-apps-limitations#custom-keyboard-handling)

**Native acceptance:** use Tab, Shift+Tab, Enter, and Space with a screen reader. Confirm selected state and level. Collapse an ancestor of the focused item and check the resulting focus location. Test long labels and deep indentation at the default 320-pixel width.

**Gallery coverage:** the HTML sample demonstrates a small fixed hierarchy, expansion, selection, and selected paths. It has no lazy loading, count toggle, arbitrary Nodes input, five-level boundary, or native output formulas. [Gallery:771](../../preview/index.html#L771)

## Host integration and style follow-up

These five definitions do not opt into AccessAppScope. With that setting off, Set-created variables are scoped to each instance. Keep persistence, routing, validation data, and lazy loading in the host through public properties and events. Do not rename internal variables merely to prevent a collision that the default component scope already prevents. Verify isolation in Studio and document that hosts should leave app scope off. [Microsoft component scope](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/create-component#scope)

The existing AccentColor and Theme inputs cover only part of the styling. Literal surfaces, text colors, radii, and some status colors remain. Extend them with optional surface, text, border, semantic-color, and radius inputs after functional fixes. Bind those inputs to the shared palette in a native host example. Keep rounded fields and pill actions. Do not imply that an HTML color control proves full native style coverage.

The most useful next artifact is a small native validation app. Include these five components, host action buttons, event logs, empty-data switches, long-text datasets, and light/dark palette controls. Use it to record the acceptance tests above before adding more gallery features.
