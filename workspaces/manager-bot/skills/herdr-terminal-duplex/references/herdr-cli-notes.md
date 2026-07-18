# Herdr CLI Notes

## Verified commands
- `herdr status client`
- `herdr api snapshot`
- `herdr pane list`
- `herdr pane current`
- `herdr pane read <pane_id>`
- `herdr pane run <pane_id> <command>`
- `herdr pane send-text <pane_id> <text>`
- `herdr pane send-keys <pane_id> <key>`
- `herdr agent list`
- `herdr agent read <target>`
- `herdr agent send <target> <text>`
- `herdr agent attach <target>`
- `herdr agent start <name> -- <argv...>`
- `herdr wait output <pane_id> --match <text>`
- `herdr wait agent-status <pane_id> --status <idle|working|blocked|done|unknown>`

## Observed local state
- Herdr version: `0.7.4`
- Client protocol: `16`
- Focused pane example: `w1:p1`
- Foreground shell in the current pane: `/bin/bash`
