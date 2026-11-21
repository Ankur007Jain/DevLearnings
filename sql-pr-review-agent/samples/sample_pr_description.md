DATA-123 Add procedure for members with recent paid claims

## What changed
Adds `dbo.usp_GetMembersWithRecentClaims` for the care-management outreach list.

## Story (pasted here so the agent can test without Jira)
As a care-management analyst, I need a stored procedure that returns active members
who had at least one **paid** claim in the **last 90 days** (by service date) as of a given date.

Acceptance criteria:
- One row per member: member id, first name, last name, plan code.
- Include the number of paid claims and the total paid amount in the window.
- Exclude members whose termination date is on or before the as-of date.
- `@AsOfDate` is optional and defaults to today.
