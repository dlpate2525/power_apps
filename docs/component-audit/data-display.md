# Data component deep review

[Review scope and prioritized plan](../COMPONENT-DEEP-DIVE.md)

Reviewed 2026-11-03 against the working snapshot identified as fork commit `8064433`. The original source baseline is `2965daf`.

Scope: complete YAML and README files for Attachments list, Data table, Kanban board, KPI card, and Month calendar. Reviewed their current HTML gallery sections and interaction scripts. This is a static source review. No Power Apps Studio import, formula execution, upload, or assistive-technology test was available. Arithmetic examples below evaluate the written formulas; they do not simulate Power Apps.

P1 means resolve before claiming production readiness. P2 means a material behavior or usability gap. P3 means a smaller correction. Small effort means an isolated formula or documentation change. Medium means coordinated state or layout work. Large means a control or delivery architecture decision.

## Shared prerequisite: G01, supported native formulas

All five components contain `JSON()` calls in nonbehavior properties. Examples include Attachments [Image color conversion](../../attachments-list/component.yaml#L281), Data table [progress SVG](../../data-table/component.yaml#L1082), Kanban [SVG styling](../../kanban-board/component.yaml#L363), KPI [target SVG](../../kpi-card/component.yaml#L334), and Calendar [Items color conversion](../../month-calendar/component.yaml#L528).

Microsoft documents `JSON()` as behavior-only. This is a source/API conflict requiring a native import gate, not a reproduced Studio error. Consolidate it with the repository-wide G01 finding. The Attachments payload conversion in `OnSelect` is a different, permitted behavior context. [Microsoft JSON reference](https://learn.microsoft.com/en-us/power-platform/power-fx/reference/function-json#description)

Resolve G01 before running native acceptance tests below. Keep public inputs, outputs, actions, and ordered event parameters stable.

## Attachments list

Purpose and strengths: stage new files, mark existing files for removal, provide undo, and delegate persistence to the host. The source separates ready and invalid items. It exposes staged data and removal keys, and locks editing through `IsUploading`. The README already warns about shared app collections.

### A01 — P1: the picker uses an unsupported classic-control arrangement

- **Evidence:** [component.yaml:445](../../attachments-list/component.yaml#L445) declares `Attachments@2.3.0` inside a manual container. Its `Items` is `Blank()` at line 452. There is no Form ancestor.
- **Trigger and consequence:** use this standalone component to choose a real file. Microsoft's classic-control contract requires a Form for upload/delete and an attachment-column binding. The component's primary operation therefore lacks a supported foundation. This is a documented conflict, not a native reproduction. **Confidence: high.** [Classic Attachments limitations](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/control-attachments)
- **Recommendation:** evaluate the current modern Attachments preview in a small native spike. It explicitly supports standalone staging. Confirm tenant availability, allowed preview usage, storage destination, and mobile behavior. If it is unsuitable, provide a supported host-level Form integration rather than nesting this component into a Form. Preserve the existing file records and `OnSave` boundary through an adapter. **Effort: large. Dependency: control availability and storage choice.** [Modern Attachments](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/modern-controls/modern-control-attachments)
- **Native acceptance:** stage a PDF and image, reject an invalid extension and oversize file, save to the intended destination, reload, and remove one saved attachment. Repeat on required mobile clients. Record control versions and errors.

### A02 — P1: two instances share staging and removal state

- **Evidence:** [component.yaml:5](../../attachments-list/component.yaml#L5) enables `AccessAppScope`. [OnReset](../../attachments-list/component.yaml#L197) clears the fixed names `colLcsAttachStaged`, `colLcsAttachRemoved`, and `colLcsAttachPayload`. The [outputs](../../attachments-list/component.yaml#L206) and [file staging](../../attachments-list/component.yaml#L473) use those same collections without an instance key.
- **Trigger and consequence:** place two instances on different records. Staging in A changes the collection read by B; resetting either clears shared changes. A host could receive another instance's removal keys. This follows the written state ownership and Microsoft's app-scope rules. **Confidence: high.** [Component scope](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/create-component#scope)
- **Recommendation:** use component-instance state with app scope disabled, after A01 confirms the supported picker arrangement. Keep persistence in host events. If an app adapter is temporarily necessary, key its state explicitly by instance and record. Do not add another global collection per feature. **Effort: medium. Dependency: A01.**
- **Native acceptance:** stage different files in A and B, mark different removals, then cancel/reset/save A. B's counts, files, keys, and payload must remain unchanged. Repeat with both instances visible and across screens.

### A03 — P1: the save payload depends on loaded gallery rows

- **Evidence:** [ReadyCount](../../attachments-list/component.yaml#L206) counts the authoritative collection. The [staging gallery](../../attachments-list/component.yaml#L509) displays at most three rows at once. [Save](../../attachments-list/component.yaml#L1133) builds the payload from `Filter(galStaged.AllItems, Status="Ready")`, then calls `OnSave` with the full ready count at line 1143.
- **Trigger and consequence:** raise `MaxFiles`, stage a large batch, and save without scrolling. Microsoft states `AllItems` contains loaded rows and may be smaller than `Items`. The announced count can therefore exceed the payload count. Whether a specific batch triggers virtualization requires Studio. **Confidence: high for the unsafe dependency; medium for a particular batch size.** [Gallery AllItems](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/control-gallery)
- **Recommendation:** derive payloads from staged data rather than gallery control instances. Validate binary conversion and handle conversion errors before calling `OnSave`. Preserve `Name`, `ContentBytes`, and event parameter order. **Effort: medium. Dependencies: A01 and A02.**
- **Native acceptance:** stage 30 distinct small files with `MaxFiles=30`. Save without scrolling and after scrolling. Assert identical names, payload count, and decoded content. A failed conversion must not report a complete ready batch.

### A04 — P2: the footer has no narrow layout

- **Evidence:** [summary width](../../attachments-list/component.yaml#L986) is `(Parent.Width-48)-272`, which equals zero at width 320. The buttons use fixed widths and offsets at [line 1012](../../attachments-list/component.yaml#L1012) and [line 1103](../../attachments-list/component.yaml#L1103).
- **Trigger and consequence:** host the component at 320 pixels. The summary has no display area; narrower widths produce a negative formula result. The browser demo uses wrapping layout and does not reproduce this constraint. **Confidence: high for geometry; actual clipping is Studio-dependent.**
- **Recommendation:** stack the summary and actions below a width breakpoint. Publish the supported width/height contract. **Effort: medium. Dependency: final picker layout from A01.**
- **Native acceptance:** use 320, 375, and 640-pixel widths with long translated action labels. Ready, removed, and busy status must remain visible without overlapping actions.

## Data table

Purpose and strengths: one row schema supports Table, Cards, and List views. The host owns filtering, sorting, paging, and persistence. Selection outputs explicitly distinguish retained IDs from current-page rows. Badge colors are configurable. Selection uses component-local collections under the default scope; it is not the Attachments isolation problem.

### D01 — P1: the table view lacks supported two-dimensional semantics

- **Evidence:** the header controls are independent buttons/text, while [galRows](../../data-table/component.yaml#L994) is a vertical Gallery containing six cell groups. Its accessible label is only `Rows` at line 1008. [The row button](../../data-table/component.yaml#L1571) names only the title column.
- **Trigger and consequence:** navigate the Table view with a screen reader as a data table. Microsoft explicitly advises against galleries for two-dimensional tables because users need column/row semantics and cell navigation. The HTML preview's real `<table>` at [preview/index.html:692](../../preview/index.html#L692) provides different semantics and cannot validate the YAML. **Confidence: high for the documented architecture limitation.** [Canvas accessibility limitations](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/accessible-apps-limitations#custom-tables)
- **Recommendation:** decide between a complete one-dimensional record layout and a supported grid/code-component path. A native Data Table on a host screen is another candidate; do not assume it can be saved inside this canvas component. Preserve `Rows`, selection outputs, and row/action/sort events with a compatibility wrapper. **Effort: large. Dependency: native control feasibility and library delivery decision.** [Component limitations](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/create-component#known-limitations)
- **Native acceptance:** users must identify each value's column and row, reach every field, sort, select, and invoke row actions using only keyboard and the required screen reader. Test retained selection across paging.

### D02 — P2: progress values above ten are overstated

- **Evidence:** [line 1074](../../data-table/component.yaml#L1074) caps `total` at ten but leaves `done` unchanged. Segment fill compares its index with `done` at line 1082. This repeats for all six columns and the [Cards view](../../data-table/component.yaml#L1996). The [public contract](../../data-table/component.yaml#L10) describes text such as `2/4` without a denominator limit.
- **Trigger and consequence:** supply `5/20`. The visual fills five of ten segments, showing 50% while the text means 25%. `10/20` appears complete. **Confidence: high; deterministic arithmetic.**
- **Recommendation:** keep the original numerator and denominator for the ratio. If ten segments are the display limit, support partial segments or clearly label the approximation. Do not round 25% to a full 20% or 30% without that distinction. Define handling for blank, malformed, negative, and zero-total values consistently across Table and Cards. **Effort: small. Dependency: G01 SVG replacement.**
- **Native acceptance:** compare `0/20`, `5/20`, `10/20`, `20/20`, `2/4`, and invalid text in both views. Visual progress and spoken/text values must agree.

### D03 — P2: narrow views lose labels and toolbar space

- **Evidence:** [List title width](../../data-table/component.yaml#L2281) and subtitle width at line 2298 reserve 384 pixels when selection is enabled. Width 320 yields `-64`. The [view selector](../../data-table/component.yaml#L446) reserves the rightmost 256 pixels while [bulk actions](../../data-table/component.yaml#L364) use fixed positions. Table columns retain caller-specified pixel widths. Cards already have breakpoints at [line 1846](../../data-table/component.yaml#L1846).
- **Trigger and consequence:** choose List at 320 pixels, or enable several bulk actions in a narrow host. Titles have no usable width, and toolbar controls compete for the same area. **Confidence: high for formula geometry.**
- **Recommendation:** define supported responsive behavior for all three views. Reflow toolbar actions and List metadata; provide a complete small-screen record view rather than silently hiding fields. Keep explicit `View` selection and `OnViewChange` semantics. **Effort: medium. Dependency: D01 architecture decision.**
- **Native acceptance:** test each view at 320/600/960 pixels with six populated columns, three bulk actions, three row actions, long labels, and retained off-page selection.

## Kanban board

Purpose and strengths: separate Columns and Cards tables make the host data contract clear. Movement uses labeled previous/next buttons rather than requiring drag-and-drop. Destination limits can disable moves, while `OnMove` delegates persistence. Selection and local variables remain inside the component's default scope.

### K01 — P2: all columns are forced into one row

- **Evidence:** [galColumns.WrapCount](../../kanban-board/component.yaml#L204) always equals the column count. [Heading width](../../kanban-board/component.yaml#L245) is `Max(0, TemplateWidth-112)`; the count pill stays 88 pixels wide at line 262. [Card detail width](../../kanban-board/component.yaml#L419) reserves another 88 pixels.
- **Trigger and consequence:** place four columns in a 320-pixel host. Even before padding, each column has at most 80 pixels, so heading width becomes zero. Count pills and movement controls compete with the card content. **Confidence: high for geometry.**
- **Recommendation:** use a stacked layout, a single-column selector, or deliberate horizontal scrolling with a minimum column width. Keep column order, limits, card keys, and the existing move tuple. The gallery's CSS stacking at [preview/index.html:284](../../preview/index.html#L284) is only a design example. **Effort: medium. Dependency: agreed responsive layout contract.**
- **Native acceptance:** test one, four, and six columns at 320/600/960 pixels. Every column title, count, selected card, and available move must remain understandable and keyboard reachable.

### K02 — P2: asynchronous move handling needs an explicit host pattern

- **Evidence:** destination capacity is derived from the supplied Cards snapshot at [lines 321–322](../../kanban-board/component.yaml#L321). [OnSelect](../../kanban-board/component.yaml#L501) sets local movement feedback and immediately invokes `OnMove`; the component has no pending/error input. The next-direction handler follows the same pattern at line 546.
- **Trigger and consequence:** a host performs a remote move and leaves Cards unchanged until completion. Repeated activation can emit repeated requests against the same snapshot. Capacity enforcement and rejection recovery belong to the host but lack a concrete README example. **Confidence: high for the missing pending contract; conditional risk, not proven duplicate persistence.**
- **Recommendation:** first document an idempotent host handler, pending state, failed-save feedback, and server-side limit recheck. If real consumers need component-level locking, add an optional pending-card input without changing `OnMove`. **Effort: medium. Dependency: host persistence/error pattern.**
- **Native acceptance:** delay the save, activate Move repeatedly, then reject it. The host must persist at most one accepted move, retain truthful card placement, explain failure, and permit retry.

## KPI card

Purpose and strengths: formatting, change, trend, target ratio, and status are exposed separately. Missing targets are Neutral and target percentages are clamped. `GoodWhen` controls whether a change is favorable; automatic target status is explicitly higher-is-better. That documented distinction is not reported as a defect.

### P01 — P2: zero-baseline changes are displayed as zero percent

- **Evidence:** [ChangePercent](../../kpi-card/component.yaml#L137) returns zero when Previous is zero. [The chip](../../kpi-card/component.yaml#L278) always formats that output as a signed percentage. [The card's spoken summary](../../kpi-card/component.yaml#L348) repeats it.
- **Trigger and consequence:** set Previous=0 and Value=10. Trend is Up, but the displayed change is `+0%` and the button says “up 0%.” A relative percentage from zero is undefined. **Confidence: high; deterministic formulas.**
- **Recommendation:** preserve the documented numeric output for compatibility, but display “New,” “From zero,” or the absolute change for this boundary. Use the same wording in the accessible summary. **Effort: small. Dependency: agreed wording/localization.**
- **Native acceptance:** test Previous values blank, zero, positive, and negative. A zero baseline must never imply no change when Value differs.

### P02 — P2: status and target lack a complete text equivalent

- **Evidence:** status changes the [icon surround](../../kpi-card/component.yaml#L207), [icon color](../../kpi-card/component.yaml#L222), and target-bar color. The icon shape remains caller-selected at line 221. There is no visible status label. [btnCard.Text](../../kpi-card/component.yaml#L348) omits `StatusShown`, Target, and TargetPercent.
- **Trigger and consequence:** use the card without reliable color perception or inspect it by screen reader. Good/Warning/Bad and target progress are not conveyed as complete text. The browser gallery adds a status label and target text at [lines 607–610](../../preview/index.html#L607); those features are not in the native source. **Confidence: high for source omissions; final announcements require Studio.**
- **Recommendation:** add a short status label and include target value/progress in the accessible summary. Keep existing inputs and outputs. Choose status text and colors from the shared theme work rather than inventing another palette. **Effort: medium. Dependencies: shared semantic tokens and final card layout.**
- **Native acceptance:** verify all four statuses with color removed, Icon blank, and Target blank/positive. A screen reader must announce label, value, meaningful change, status, and applicable target without duplicated decorative content.

### P03 — P3: the target bar shows progress when the ratio is zero

- **Evidence:** [SVG fill width](../../kpi-card/component.yaml#L337) uses `Max(2,p)`, where `p` is the clamped percentage.
- **Trigger and consequence:** Value=0 and Target=100 produces a 2% fill. Values below 2% are also overstated. **Confidence: high; deterministic arithmetic.**
- **Recommendation:** permit an empty fill at zero and use the real ratio. Keep any minimum decorative mark separate from the data indicator. **Effort: small. Dependency: G01 and P02.**
- **Native acceptance:** inspect 0%, 1%, 2%, and 100% with motion both on and off. The bar must match the value and accessible target summary.

## Month calendar

Purpose and strengths: month/date actions normalize dates, events cover inclusive date ranges, and the host receives date/event callbacks. Day buttons include event counts and selection text. Week start is configurable. Multi-day pills distinguish their start and end.

### C01 — P2: multi-day events can change visual rows mid-span

- **Evidence:** each day [filters Events independently](../../month-calendar/component.yaml#L520), packs the results into its local gallery, and takes the first MaxPerDay entries. There is no shared week-level lane allocation. [Pill geometry](../../month-calendar/component.yaml#L545) visually joins continuation segments across day boundaries.
- **Trigger and consequence:** input event A for day 1, followed by event B for days 1–3. B occupies the second row on day 1 and the first row on days 2–3. Adjacent segments therefore fail to form a stable ribbon and can appear to join another event. **Confidence: high for the data-to-row mapping; visual severity requires Studio.**
- **Recommendation:** allocate a stable lane per event within each week, with placeholders when an earlier event ends. Alternatively, use independent labeled day entries and stop implying continuous ribbons. Preserve Events and `OnSelectEvent`. **Effort: medium to large. Dependency: C02's small-screen design.**
- **Native acceptance:** use overlapping one-day and multi-day events, including week/month boundaries and more than MaxPerDay. Event identity, lane placement, overflow counts, and callback keys must remain consistent.

### C02 — P2: dense event controls need an accessible narrow-screen alternative

- **Evidence:** [galDays](../../month-calendar/component.yaml#L402) always uses seven columns. At width 320, [overflow text](../../month-calendar/component.yaml#L474) receives about 9.7 pixels. [Event targets](../../month-calendar/component.yaml#L583) are 18 pixels high in 20-pixel rows at line 537.
- **Trigger and consequence:** show several events per day on a small display. Event titles and “more” text lack useful space. The source's 18-pixel targets and 20-pixel center spacing do not provide the 24-pixel size or spacing described by WCAG 2.2, absent a qualifying equivalent control. Final CSS-pixel sizing and any host-provided exception require native measurement. **Confidence: high for source geometry; medium for whole-app conformance.** [W3C target size](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)
- **Recommendation:** add a selected-day agenda with complete titles and adequately sized event actions; use it on narrow screens and for overflow. Keep date/event callbacks. An agenda is already demonstrated, but only in the HTML approximation at [preview/index.html:740](../../preview/index.html#L740). **Effort: medium. Dependency: C01 presentation choice and height contract.**
- **Native acceptance:** at 320 pixels, select a day with six events and open every event without precise tapping. Verify complete event names, dates, callback keys, focus order, and screen-reader announcements.

## Recommended order

1. Resolve shared G01 and decide the supported attachment/control architecture. These decisions unlock meaningful native tests.
2. Fix Attachments state isolation and payload completeness together. Test two instances and unscrolled large batches.
3. Choose the Data table accessibility architecture before rebuilding its responsive layout.
4. Correct progress arithmetic and KPI text equivalents. These are small, well-defined changes after G01.
5. Implement narrow layouts for Attachments, Data table, Kanban, and Calendar. Coordinate Calendar lane and agenda behavior.
6. Add a real asynchronous Kanban host example. Validate delays, duplicate activation, rejected saves, and capacity conflicts.

The HTML gallery uses local sample data and browser-native semantics. Its successful interactions do not validate native attachment APIs, gallery virtualization, canvas accessibility roles, or component-instance isolation. Keep these acceptance results separate from browser preview checks.
