---
name: "herdr-terminal-duplex"
description: "Use Herdr to inspect, drive, and duplex with terminal panes/sessions from the assistant."
---

# Herdr Terminal Duplex

Use this skill when you need to read from or write to a live Herdr-managed terminal, wait for terminal output, or move between panes, tabs, sessions, and agent targets.

## Core model

Herdr exposes two useful target types:
- `pane_id` for terminal panes, e.g. `w1:p1`
- `target` for agent-oriented commands, which can be a terminal id, agent name, label, or legacy pane id

Prefer the narrowest target you can reliably identify.

## First check

Confirm the client is available before doing anything else:

```bash
herdr status client
```

If you need to understand the current layout:

```bash
herdr api snapshot
herdr pane list
herdr tab list
herdr session list
```

## Reading output

Use read-only commands before sending anything:

```bash
herdr pane read <pane_id>
herdr pane read <pane_id> --source visible
herdr pane read <pane_id> --source recent
herdr agent read <target>
```

Use `herdr wait` when you want to block until a specific output or state appears:

```bash
herdr wait output <pane_id> --match <text>
herdr wait agent-status <pane_id> --status idle
```

## Sending input

Use `pane run` when you want the command text plus Enter:

```bash
herdr pane run <pane_id> '<command>'
```

Use `pane send-text` when you only want to type text into the terminal:

```bash
herdr pane send-text <pane_id> '<text>'
herdr pane send-keys <pane_id> Enter
```

For agent targets, use literal-text delivery or direct agent control as appropriate:

```bash
herdr agent send <target> <text>
herdr agent attach <target>
herdr agent wait <target> --status idle --timeout 30000
```

## Finding a good target

If you do not already know the target:
- use `herdr pane current` or `herdr api snapshot` for the focused pane
- use `herdr pane list` to find active panes and their IDs
- use `herdr agent list` when working with named agents
- use `herdr pane process-info --pane <pane_id>` if you need to confirm the foreground process

## Common workflow

1. Identify the target pane or agent.
2. Read the current visible output.
3. Send the command or text.
4. Wait for the expected response.
5. Read back the result.
6. Clean up by closing any temporary pane or detaching if needed.

## Practical rules

- Use a temporary pane/tab for exploratory or long-running commands when possible.
- Prefer `read` and `wait` over guessing whether a command finished.
- Do not use Herdr for destructive commands without normal confirmation discipline.
- If a command is ambiguous, prefer `pane run` in a disposable pane over typing into the user's main shell.
- Keep commands short and explicit so the resulting output is easy to verify.

## Handy commands

```bash
herdr pane focus --direction left|right|up|down
herdr pane split --direction right|down
herdr pane close <pane_id>
herdr session attach <name>
herdr agent start <name> -- <argv...>
```
