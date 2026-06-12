# Project AGENTS

This file defines how to work on the monday.com Gantt clone in this folder.

## Mission
- Build a polished, functional Gantt chart app using `NextJS`, `FastAPI`, and `SQLite`.
- Optimize for product quality, not just code volume.
- Ship a believable workflow for planning and managing work, not a toy chart.

## Product Shape
- The UI should feel like a serious planning tool: dense, structured, and visually intentional.
- The timeline is the centerpiece, but it must work together with a task list, filters, and a details editor.
- The app must support persistence and round-trip editing through the backend.

## Design Rules
- Use the provided color tokens as the source of truth.
- Prefer `brand-navy` and `surface-light` for structure.
- Use accent colors sparingly to encode semantics:
  - `brand-blue` for primary actions
  - `brand-teal` for collaboration/status highlights
  - `brand-green` for success/completion
  - `brand-orange` for warnings or due-soon states
  - `brand-purple` for secondary accents or grouping
- Avoid generic purple-first dashboard styling.
- Avoid flat, lifeless layouts; use spacing, layering, and subtle motion.
- Keep contrast strong and text readable at dense spreadsheet-like scale.

## Architecture Conventions

### Frontend
- Prefer small, composable React components.
- Keep timeline math isolated from view code.
- Put date and display helpers in `lib/`.
- Keep feature-specific state in feature folders, not scattered globally.
- Make loading, empty, and error states first-class.

### Backend
- Use explicit request and response schemas.
- Keep business rules in services, not in route handlers.
- Keep raw SQL or SQLite access in repositories or data-access helpers.
- Validate on the server even if the frontend already validates.

### Deployment
- Assume `Docker` is the deployment/runtime target unless a different target is later specified.
- Keep service startup, ports, and environment variables container-friendly.
- Treat local parity as important: what works in dev should be close to what runs in deploy.
- If deployment assumptions change, update this file so future work stays aligned.

### Data
- Use stable IDs everywhere.
- Keep one canonical date representation.
- Avoid hidden implicit ordering rules.
- Make dependencies, hierarchy, and sort order explicit in the schema.

## Testing Rules

Do not chase 100% coverage at the expense of product value.

Test the things that matter most:
- Frontend rendering of the shell, task list, timeline, and editor
- Frontend interactions for selection, drag, resize, and filter state
- Backend validation and persistence
- Frontend/backend integration through the real API
- Persistence across reloads
- Error and empty state handling

Recommended test mix:
- Unit tests for utilities and pure business logic
- Component tests for key UI states
- API tests for FastAPI endpoints and validation
- Integration tests for SQLite round-trips
- A few end-to-end smoke tests for the critical path

High-value smoke path:
- Open app
- Create project
- Create task
- Edit task dates
- Move or resize task
- Refresh page
- Confirm the saved state returns correctly

## Quality Bar
- Make the app feel stable before making it feel fancy.
- If a feature changes task dates or dependencies, it must be tested.
- If a feature affects persistence, it must be tested.
- If a feature affects the timeline canvas, it must be visually checked.
- Prefer simple, debuggable implementations over clever abstractions.

## Working Process
1. Confirm scope and data model before coding.
2. Build backend schema and API first when the data model is still in flux.
3. Implement the read-only UI next so the shape of the product is visible early.
4. Add editing interactions after the rendering path is stable.
5. Add tests while the behavior is fresh, especially for regressions.
6. Polish only after the core flows are dependable.

## Review Checklist
Before marking work complete:
- The app starts cleanly.
- The timeline renders real data.
- CRUD persists through SQLite.
- Validation errors are understandable.
- The key frontend, integration, and backend tests pass.
- The layout works on desktop and narrower screens.
- The visual design matches the intended brand palette.

## Notes for Future Agents
- If a change touches date math, dependency resolution, or task ordering, assume it is high risk.
- If a change affects the timeline interaction model, inspect the whole flow, not just the component.
- If a change adds a new view or panel, keep the design system consistent.
- Document new assumptions in this file if they will matter later.
