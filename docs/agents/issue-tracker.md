# Issue tracker: GitHub

Use `dlpate2525/power_apps` on GitHub for tickets and specifications. Use its existing pull-request workflow for code changes and reviews.

## Current availability

The repository README states that GitHub Issues are disabled. Verify availability before an issue operation.

If Issues remain disabled, report the blocker and keep the proposed ticket in the current task's output. Enabling Issues is a separate repository setting change.

Pull-request review remains available. Resolve a supplied issue or pull-request reference before choosing the relevant workflow.

## Tool choice

Prefer connected GitHub tools when they support the required operation. Use structured arguments for titles, bodies, labels, and comments.

Use the `gh` CLI when connected tools cannot perform the operation. Target this repository explicitly with `--repo dlpate2525/power_apps`.

For multiline text, write the exact content to a temporary UTF-8 file. Pass that file with `--body-file`.

## Issue operations

1. Read the issue body, labels, state, and comments before changing an existing ticket.
2. Search existing tickets before creating a new ticket.
3. Apply the label strings in `triage-labels.md` when a task calls for triage.
4. Preserve unrelated body text and labels during updates.
5. Return the ticket link and the result after a completed change.

When a skill says **publish to the issue tracker**, create a GitHub issue once Issues are available.

When a skill says **fetch the relevant ticket**, read the specified issue and its comments. GitHub issues and pull requests share a number space.

CLI fallback examples:

```sh
gh issue view <number> --repo dlpate2525/power_apps --comments
gh issue list --repo dlpate2525/power_apps --state open --json number,title,body,labels,assignees
gh issue create --repo dlpate2525/power_apps --title "<title>" --body-file <body-file>
gh issue edit <number> --repo dlpate2525/power_apps --body-file <body-file>
gh issue comment <number> --repo dlpate2525/power_apps --body-file <comment-file>
gh issue edit <number> --repo dlpate2525/power_apps --add-label "<label>"
gh issue edit <number> --repo dlpate2525/power_apps --remove-label "<label>"
gh issue close <number> --repo dlpate2525/power_apps
```

Fetch comments separately when a listing does not include them. To explain closure, post the prepared comment before closing the issue.

## Pull requests as a triage surface

**PRs as a request surface: no.**

Use pull requests for code review and integration. External pull requests do not enter the issue-triage queue under this configuration.

For a requested review, read the pull-request body, comments, commits, and current diff. Keep the base and head fixed during the review.

CLI fallbacks are `gh pr view <number> --comments` and `gh pr diff <number>`, each with `--repo dlpate2525/power_apps`.

## Wayfinding operations

Use these conventions when the wayfinder workflow is invoked and GitHub Issues are available.

- **Map:** one issue labeled `wayfinder:map`, with Notes, Decisions-so-far, and Fog sections.
- **Child ticket:** a linked GitHub sub-issue labeled `wayfinder:research`, `wayfinder:prototype`, `wayfinder:grilling`, or `wayfinder:task`.
- **Fallback links:** if sub-issues are unavailable, list children in the map's task list and add `Part of #<map>` to each child.
- **Blocking:** use native issue dependencies where supported. These operations require numeric issue database IDs, not issue numbers or node IDs.
- **Fallback blockers:** if dependencies are unavailable, add `Blocked by: #<number>` lines to the child. All blockers must be closed before work starts.
- **Next ticket:** select the first open child in map order that has no assignee and no open blocker.
- **Claim:** assign the selected ticket to the driving developer when the invoked workflow authorizes assignment.
- **Resolve:** post the result, close the child, then add its conclusion and link to the map's Decisions-so-far section.

Prefer connected tools for these operations. Use `gh api` only for capabilities they do not expose.
