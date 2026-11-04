# Component expansion checklist

Scope: add Form field, Search and filter bar, and Message banner to the existing 12-component catalog.

- [x] Confirm the current catalog and Microsoft guidance.
- [x] Define component ownership and small public interfaces.
- [x] Build Form field source and setup guide.
- [x] Build Search and filter bar source and setup guide.
- [x] Build Message banner source and setup guide.
- [x] Extend shared color variables and contrast checks.
- [x] Add three interactive gallery previews.
- [x] Record three GIFs and static posters.
- [x] Check behavior, keyboard use, narrow layouts, and local links.
- [x] Review the final changes and prepare a pull request.

Native release checks, requiring Power Apps Studio:

- [ ] Import each definition and resolve any schema or formula errors.
- [ ] Check events, reset behavior, screen-reader announcements, and two-instance isolation in the player.
- [ ] Validate component-library import and updates in a consumer app.

Browser previews illustrate behavior. They do not execute Power Fx or establish native compatibility.

## Validation record

Checked November 3, 2026, against the local review snapshot.

- Three new YAML definitions parse and match the 28-field shared theme.
- All 32 declared light-palette contrast pairs pass.
- Three new interaction suites and the original component regression checks pass.
- All 15 previews fit 1440, 390, and 320 pixel page widths.
- All 15 GIFs load; playback is explicit, exclusive, and stoppable.
- Gallery and Markdown local references resolve.
- No JavaScript errors or external network requests occurred during the preview checks.
- Matt Pocock's Standards and Spec review found no actionable issues in the changed source. A separate visual review found and fixed banner icon crowding at doubled text size; a regression check now covers it.
- The original 12 component definitions and media, plus LICENSE, are unchanged from merged PR #1.

Read [Local validation](VALIDATION.md) in the repository for repeatable checks. Modern Dropdown is a preview dependency. Native checks above remain open.
