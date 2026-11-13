# Phinite Plugin

Build, ship, run and debug your **Phinite** agent graphs straight from Claude.

[Phinite](https://app.phinite.ai/) is where you build and publish AI agents. This plugin connects Claude to the
hosted **Phinite MCP server**, so you can design a use case, deploy its tools and graphs, test it, read the run logs
and take it live in plain language, right inside your conversation. Claude acts as you: it can do exactly what your
Phinite account can do in the app, and nothing more.

---

The Phinite plugin lives in this GitHub marketplace:

> **https://github.com/Auto-AI-Labs/phinite-claudecode-plugin**

## Install in Cowork (desktop) (Paid version of Claude) - For Free version of Claude, see below

1. Open **Customize → Plugins → Personal**.
2. Click on **+** sign.
3. Click on **Add marketplace → Add from a repository**.
4. Add a marketplace using the GitHub link above.
5. Install the **phinite** plugin.
6. Click on **Manage**
7. Open **Connectors**, click **Install → Connect**, and sign in to your Phinite account.
8. Your plugin is now ready to use — just ask Claude to build, test or ship a Phinite use case.

## Install in Claude Code (CLI / terminal)

```
/plugin marketplace add Auto-AI-Labs/phinite-claudecode-plugin
/plugin install phinite@phinite
/reload-plugins
```

Now run **`/phinite:login`** (or `/mcp` → **phinite** → **Authenticate**) and sign in to Phinite when prompted.

> It's OAuth; you just sign in to your Phinite account and pick the workspace to build in.
> Now your plugin is ready to use — just ask Claude to build, test or ship a Phinite use case.

You need Python 3.9+ on your machine for the project script (deploying folders, sending files). Nothing else is
installed, and no Phinite token is stored on your machine.

## Use it in Claude web (claude.ai) or Free version of Claude

On claude.ai or free version of Claude there's no plugin marketplace — add Phinite as a **custom connector**
instead:

1. Go to **Settings → Connectors → Add custom connector**.
2. Paste the Phinite MCP server URL:
   ```
   https://mcp.dev.phinite.ai/mcp
   ```
3. Click **Add**, then **Connect**, and sign in to your Phinite account.

The connector gives Claude the Phinite tools. The plugin's skills, commands and project script need Cowork or
Claude Code.

---

## How to use it

Once connected, just talk to Claude — it designs the graphs, deploys them, runs them and explains what happened:

```
"Build a support assistant that answers billing questions from our invoices API"
"Make an autonomous graph that reads uploaded receipts and posts the totals to Slack"
"Test my onboarding graph and explain the last run"
"Ship it to development behind an API trigger"
```

**Commands** (Cowork and Claude Code):

- **`/phinite:login`** — sign in, check the sign-in, or switch workspace.
- **`/phinite:new`** — scaffold a use-case project and design its graphs with you.
- **`/phinite:deploy`** — dry run, then deploy: tools upserted and published when they changed, graphs created or
  updated by name.
- **`/phinite:test`** — chat with the graph or run it autonomously, read the run log, diagnose.
- **`/phinite:ship`** — publish → build → environment → trigger or Chat API → API key → call it from outside.
- **`/phinite:logs`** — explain a run: tool calls, inputs, outputs, variables, errors.
- **`/phinite:eval`** — evaluate a graph with LLM judges and get the failures with fixes.

The **`phinite-builder`** agent takes a whole use case end to end, and the skills (`phinite-design`, `phinite-ship`,
`phinite-debug`, `phinite-api`, `phinite-project`, `phinite-quality`) carry the design rules learned building real
use cases.

**Your files stay on your machine.** The server is hosted and can't read your disk. When a step needs a local file
(a project folder, knowledge documents, media, a `.env`), Claude gets a short-lived upload link and sends the file
from your machine. Env values never pass through the chat.

---

*You'll need a Phinite account. Build and publish your agents at [phinite.ai](https://app.phinite.ai/sign-up).*
