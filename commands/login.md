---
description: Sign in to Phinite (OAuth, the same login as the Phinite app) or switch workspace
argument-hint: "[workspace name]"
---
Help the user sign in to Phinite through the `phinite` MCP server.

1. Call `whoami`. If it works, report the user, org, workspace and hours left in one or two lines. If the user asked for
   another workspace ($ARGUMENTS), go to step 3.
2. If it fails because the server isn't authenticated, tell the user in three short lines:
   - Run `/mcp`, select **phinite** and choose **Authenticate**.
   - A browser opens on the Phinite login (Google, GitHub or email, as in the app). Pick the org and the workspace to
     build in, then return here.
   - Claude never sees a password or token. The sign-in ends when its Phinite session expires, or right away when
     they sign out of all sessions in Phinite.
3. To switch workspace, `list_workspaces` shows the choices. A connection works in the workspace picked at sign-in,
   so the user re-authenticates: `/mcp` → **phinite** → **Clear authentication** (or Re-authenticate), then picks the
   other workspace.
4. Call `whoami` again and confirm.
