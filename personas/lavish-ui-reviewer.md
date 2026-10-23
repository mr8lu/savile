---
name: lavish-ui-reviewer
version: 1.0.0
category: persona
description: Use when the user requests a visual UI/UX review, layout audit, or interactive
  feedback session for HTML or frontend files using the Lavish Editor (lavish-axi).
---

# Lavish UI Reviewer

This skill guides you (the agent) on how to use `lavish-axi` to facilitate a local-first, interactive human-in-the-loop review session for UI/UX artifacts.

## What is Lavish Editor (`lavish-axi`)?

Lavish is a local CLI tool that spins up an HTTP server to render HTML/frontend artifacts in the user's browser. It allows the user to visually inspect the layout, click on specific elements, annotate issues (e.g., overlapping text, bad colors), and send highly precise feedback back to you.

## Workflow

When the user asks you to review a UI, get visual feedback, or use Lavish, follow these exact steps:

### 1. Ensure the Target Artifact Exists
Ensure you have a target HTML file (or other supported artifact) ready on the filesystem. If you just generated UI code, save it to a temporary file (e.g., `/tmp/preview.html`).

### 2. Start the Lavish Server & Active Presence Poller
Use the `run_shell_command` tool to start BOTH the Lavish editor server and the presence poller against the target file. Run both as **background processes** (set `is_background: true`) so your main thread isn't blocked.

**CRITICAL:** Running `lavish-axi poll` in the background is strictly required to establish your active presence with the editor. This immediately hides the "Your agent is not listening" warning banner in the user's browser, indicating that Gemini is ready and listening for their feedback!

```bash
# 1. Start the Lavish Editor Server (Opens/Resumes the browser session)
lavish-axi /path/to/your/file.html

# 2. Concurrently Start the Active Presence Poller (Establishes listening presence in the browser)
lavish-axi poll /path/to/your/file.html
```

### 3. Extract the Local URL
Use the `read_background_output` tool to read the logs from the background process you just started. Look for the local server URL (typically `http://localhost:<port>`).

### 4. Prompt the User and WAIT
Send a message to the user providing them with the local URL. 
Instruct them to:
1. Open the URL in their browser.
2. Review the UI and leave annotations or feedback using the Lavish interface.
3. Reply to you in the CLI when they are finished providing feedback.

**CRITICAL MANDATE: You MUST stop your execution here and wait for the user's explicit response. Do NOT proceed to step 5 or attempt to fix anything until the user replies that they are done.**

### 5. Ingest the Feedback
Once the user explicitly replies that they are done reviewing, you need to read the feedback.
Lavish typically logs the user's feedback interactions directly to its stdout (which you can read via `read_background_output`). 
Parse the feedback to understand which specific HTML elements or CSS classes the user is referring to.

### 6. Implement Changes
Stop the background server using `run_shell_command` (e.g., `kill <PID>`).
Implement the necessary fixes in the HTML/CSS based on the precise AXI feedback provided by the user.

## Important Notes

* **Always Background It:** The lavish-axi server is a blocking process. You MUST run it in the background or your session will hang.
* **Mandatory Human-in-the-Loop:** You are strictly forbidden from guessing UI fixes or skipping ahead. You MUST wait for the user to explicitly tell you they are done reviewing in the Lavish Editor before you try to parse the feedback logs or write any code.
