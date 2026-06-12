# monday.com Gantt Clone Plan

## Goal
Build a polished monday.com-style Gantt chart application with:
- `NextJS` for the frontend
- `FastAPI` for the backend
- `SQLite` for persistence
- A strong visual system based on the provided brand palette

This plan prioritizes a reliable product path over exhaustive test coverage. The goal is not "100% tests"; the goal is to thoroughly cover the paths most likely to break or affect users.

## Product Critique

Before building, the plan should explicitly account for these gaps and risks:
- A pure Gantt view is not enough; users need project/task CRUD, dependency editing, and a usable task list or side panel.
- Drag-and-drop timeline interactions are usually where bugs hide, especially around date math, zoom levels, and snapping behavior.
- Timezone and date handling can quietly break schedules if the frontend and backend do not share one canonical representation.
- A clone feels fake if there is no responsive layout, keyboard support, loading/error states, and persistence.
- The app needs a clear interaction model for zoom, expand/collapse groups, filtering, and selection.
- SQLite is fine for an MVP, but schema design should leave room for future migration to Postgres.
- Tests should focus on critical flows, regressions, and integration boundaries rather than chasing exhaustive unit coverage.

## Product Scope

### Core user stories
- Create, edit, duplicate, and delete projects
- Create, edit, and delete tasks
- Set start/end dates, progress, assignee, status, and dependencies
- Render tasks on a Gantt timeline with group hierarchy
- Drag tasks on the timeline to move them
- Resize tasks to adjust duration
- Expand and collapse groups
- Filter by status, assignee, and date range
- Persist all changes in the backend
- Handle validation and conflict errors gracefully

### Nice-to-have later
- Comments/activity feed
- Saved views
- Critical path
- Baselines
- Milestones
- Resource workload view
- Sharing/permissions

## Architecture

### Frontend
Use `NextJS` with a component-first structure:
- App shell with sidebar, top bar, and timeline workspace
- Timeline grid with date headers and task bars
- Task drawer or panel for editing selected items
- Shared design tokens driven by CSS variables
- Accessible controls for keyboard and screen-reader users

Recommended frontend modules:
- `app/` for routes and server components where useful
- `components/` for shell, table, timeline, dialogs, forms
- `features/gantt/` for timeline rendering and interactions
- `features/tasks/` for task state, mutation forms, and validation
- `lib/` for date math, API client, and helpers
- `styles/` for global tokens and utility classes

### Backend
Use `FastAPI` with a small, explicit API surface:
- REST endpoints for projects, tasks, dependencies, and views
- Pydantic schemas for validation and response shaping
- Service layer for business rules
- Repository/data access layer for SQLite operations
- Migration strategy or schema bootstrap for local dev and tests

Suggested backend modules:
- `api/` routers
- `schemas/` request/response models
- `services/` domain logic
- `db/` engine/session/connection helpers
- `repositories/` SQL access
- `tests/` API and service tests

### Deployment
Use `Docker` as the expected deployment and runtime packaging path:
- Keep frontend and backend container-friendly from the start
- Make local development runnable in containers or a close equivalent
- Prefer environment-based configuration so the same image can run in dev and deploy contexts
- Document any port, volume, and SQLite persistence assumptions explicitly

### Data model
Keep the schema normalized enough to avoid future pain:
- `projects`
- `tasks`
- `task_dependencies`
- `task_groups` or `sections` if grouping is separate from projects
- Optional `activity_log`

Key fields to plan for:
- stable IDs
- parent/child task relationships
- start date, end date, duration
- progress
- status
- assignee
- order/index for sort and manual placement
- timestamps for created/updated

### Date handling
- Store dates in one canonical format, ideally UTC timestamps or date-only values with clear semantics
- Keep frontend display formatting separate from storage format
- Decide early whether tasks are date-only or datetime-based
- Treat timezone conversion as a deliberate product choice, not an implementation accident

## Design System

Use the supplied palette as the visual foundation:

```css
:root {
 --brand-navy: #101828;
 --brand-blue: #005EB8;
 --brand-sky: #EAF4FF;
 --brand-teal: #00A6A6;
 --brand-green: #64A70B;
 --brand-purple: #5B3FD9;
 --brand-orange: #F28C28;

 --text-primary: #101828;
 --text-secondary: #475467;
 --text-muted: #667085;

 --surface-white: #FFFFFF;
 --surface-light: #F7F9FC;
 --surface-blue: #EEF6FF;

 --border-light: #D0D5DD;
}
```

Visual direction:
- Use a crisp, editorial layout with depth and spacing, not a generic admin dashboard
- Prefer white and soft blue surfaces with strong navy text
- Reserve teal, green, purple, and orange for semantic accents and status
- Use purposeful motion for timeline hover, selection, and drag feedback
- Keep contrast high enough for dense spreadsheet-like usage

## Development Steps

Each step below should be small enough to complete, verify, and build on without guesswork.

### Step 1: Lock the product contract
Do:
- Define the core entities: project, task, dependency, group/section
- Choose date semantics: date-only or datetime-based
- Decide dependency rules and hierarchy rules
- Define the standard API error shape
- Decide whether Docker is the deployment/runtime target

Done when:
- The data model can be described in one pass
- The date/storage rules are unambiguous
- The endpoint and error conventions are written down

### Step 2: Create the project foundation
Do:
- Set up the repo structure
- Configure frontend and backend boot commands
- Add linting, formatting, and environment config
- Initialize SQLite schema/bootstrap for local dev and tests
- Make the app runnable in Docker or close container parity

Done when:
- Frontend and backend both start locally
- SQLite can create and read sample data
- A fresh checkout has a repeatable boot path

### Step 3: Build the backend contract first
Do:
- Implement CRUD endpoints for projects and tasks
- Add dependency create/delete endpoints
- Add validation for ranges, cycles, and hierarchy
- Add request/response schemas and clear error messages
- Add seed data and test fixtures

Done when:
- The backend can create, update, and delete records reliably
- Invalid payloads are rejected predictably
- SQLite state survives a restart

### Step 4: Build the app shell and design system
Do:
- Create the main layout, navigation, and workspace regions
- Apply the brand palette and typography tokens
- Add loading, empty, and error states
- Build reusable buttons, dialogs, inputs, and dropdowns
- Make the layout responsive at desktop and tablet widths

Done when:
- The app already looks intentional before the Gantt logic exists
- The shell is usable at common screen widths
- Core states exist for loading, empty, and failure

### Step 5: Render a read-only Gantt view
Do:
- Render the timeline header and date grid
- Show task bars, milestones, and hierarchy
- Add expand/collapse for groups
- Add selection state
- Add zoom levels with clear visible ranges

Done when:
- A user can understand project structure and scheduling from the view alone
- Different date ranges still render correctly
- The data shown on screen matches the backend state

### Step 6: Add editing interactions
Do:
- Add create/edit/delete task flows
- Add dependency editing
- Add drag-to-move behavior
- Add resize-to-change-duration behavior
- Add a task details drawer or panel

Done when:
- A user can change a task and see the correct result immediately
- Edits survive refresh and come back from SQLite
- Broken or invalid edits are blocked with useful errors

### Step 7: Add filtering and workspace behavior
Do:
- Add filters for status, assignee, and date range
- Add sort/order handling
- Add keyboard and pointer affordances for selection and focus
- Add narrow-screen behavior or a fallback layout

Done when:
- The view stays usable as the dataset grows
- The controls work with keyboard and mouse
- The app degrades gracefully on smaller screens

### Step 8: Add tests for the critical flows
Focus on the highest-value tests:

Frontend tests:
- Render the shell, timeline, and edit forms
- Verify drag/resize affordances and interaction state where practical
- Confirm loading, error, and empty states
- Verify responsive behavior for key breakpoints

Integration tests:
- Frontend talks to the backend through the real API client
- Create/edit/delete task flow round-trips through SQLite
- Refresh/reload preserves state
- Validation errors surface correctly in the UI

Backend tests:
- Service-layer rules
- API request/response validation
- SQLite persistence paths
- Dependency rules and cycle checks
- Date handling and serialization

E2E smoke tests:
- Open app
- Create a project
- Create a task
- Move or resize the task
- Refresh and confirm persistence

Testing principle:
- Prioritize coverage of critical flows, regression-prone logic, and integration boundaries
- Avoid spending disproportionate time chasing theoretical 100% coverage

Exit criteria:
- The most important flows are covered by repeatable tests
- Bugs can be reproduced and diagnosed quickly

### Step 9: Polish and harden
Do:
- Pass a keyboard accessibility check
- Tune motion and micro-interactions
- Improve performance for larger task sets
- Tighten error messages
- Document operational assumptions

Done when:
- The app feels stable and intentional
- The UI is accessible enough for daily use
- The key interaction paths remain fast and predictable

## Definition of Done

The MVP is done when:
- Projects and tasks persist in SQLite
- The Gantt timeline renders correctly
- Core interactions work end to end
- Backend validation prevents corrupt states
- Critical frontend, integration, and backend tests exist
- The UI feels intentionally designed and not template-driven
- The app behaves well on desktop and smaller screens
- The development steps above can be followed in order without hidden implementation guesses

## Open Questions

- Are tasks date-only or timestamp-based?
- Do we need multi-project support in the first release?
- Should dependencies be finish-to-start only, or should other types exist later?
- Do we want guest/demo data, or only authenticated/private data?
- Is offline support in scope?
