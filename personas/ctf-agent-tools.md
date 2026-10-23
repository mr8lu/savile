---
name: ctf-agent-tools
version: 1.0.0
category: persona
description: Autonomous CTF challenge analysis and problem-solving tools including
  Model Context Protocol (MCP) server, A2A/ACP routing, Docker Compose sandboxing,
  flag scanner, crypto/pwn/web/rev/forensics helpers, and contest scoreboard tracking.
---

# CTF Agent Tools

Autonomous CTF challenge solver and agentic toolkit integrating Model Context Protocol (MCP), Agent-to-Agent (A2A) protocol, Agent Client Protocol (ACP) compatibility, Docker Compose sandboxing, SQLite contest score tracking, and a modular competition solving harness.

## When to Use

Activate or invoke this skill when:
- Analyzing, triaging, or solving CTF challenges across crypto, pwn, rev, web, forensics, or misc.
- Initializing or scaffolding challenge workspaces for live competitions (CTFd, MetaCTF, Local).
- Running Tier-0 automated triage diagnostics (signatures, strings, binary checks, web scanners).
- Deciphering ambiguous byte sequences or raw tokens with the universal representation detective (`deduce`).
- Scanning files, memory dumps, or directories for CTF flags.
- Tracking solved challenges, competitor standings, and team scores during competitions.
- Pruning hypothesis spaces using the Category Technique Elimination Matrix (`matrix`).
- Routing complex CTF sub-tasks to specialized domain agents (agent-crypto, agent-pwn, agent-rev, etc.) via ACP.
- Delegating high-risk tasks (malware analysis, heavy cracking) across boundaries to specialized sandbox clones using the file-based message bus.
- Executing suspicious binaries or payloads within the isolated Docker Compose sandbox.
- Connecting an LLM agent harness to CTF tools via Model Context Protocol (MCP).

## 1. Modular Competition Harness (`ctf`)

The `ctf` harness coordinates competition platforms, challenge workspaces, and triage. Advanced configuration (custom category tiers, pacing) is supported via `ctf.example.yaml`.

```bash
# Initialize competition workspace (CTFd, MetaCTF, Skillbit, or local directory)
uv run ctf init --adapter ctfd --url "https://ctf.example.com" --token "<token>"
uv run ctf init --platform skillbit --url "https://flashctf.example.com"
uv run ctf init --adapter local

# List challenges and fetch details (uses Dynamic Tiering to prioritize highly solved challenges)
uv run ctf list [--category crypto|pwn|rev|web|forensics]
uv run ctf info <chal_id>

# Scaffold challenge directory with template solver and automated Tier-0 triage
# Includes --adversary for an isolated secondary workspace. 'web'/'webex' challenges auto-generate an oracle_solve.py template using AsyncOracle.
uv run ctf scaffold <chal_id> [--adversary]

# Run Tier-0 automated triage diagnostics
uv run ctf triage [target_path_or_chal_id]

# Universal type-punning & representation detective (auto-decodes hex, bases, endianness)
uv run ctf deduce <token1> <token2> ...
uv run ctf deduce -f <artifact_file>

# Guarded flag submission with pacing and verification
uv run ctf submit <chal_id> "flag{...}"

# View Category Technique Elimination Matrix (prune dead ends)
uv run ctf matrix [category]

# Rebuild post-mortem knowledge index
uv run ctf index

# Develop publication-ready write-ups (.md and .pdf) with exploit lifecycle diagrams
uv run ctf writeup <chal_id>
uv run ctf writeup --all

# Free up filesystem space and archive lessons learned
uv run ctf cleanup [--dry-run] [--min-size-mb 10] [--docker]
uv run ctf archive [-o <output_dir>]
```

## 2. Specialized Domain Utilities (`ctf-agent-tools`)

All domain commands adhere to AXI standards with token-efficient TOON output:

### Challenge & Score Tracking
```bash
uv run ctf-agent-tools chal list [--category <cat>] [--status unsolved|solved]
uv run ctf-agent-tools chal add "<name>" --category <cat> [--points 100] [--flag "<flag>"]
uv run ctf-agent-tools chal solve "<name_or_id>" "<flag>" [--solver <agent>]
uv run ctf-agent-tools score board
uv run ctf-agent-tools score record "<team>" <score> [--solves <count>] [--our-team]
```

### Autonomous Flag Hunting
```bash
# Recursively scan files, directories, or raw strings for flags
uv run ctf-agent-tools flag scan <path_or_string> [--pattern "<custom_regex>"]
```

### Cryptography Domain
```bash
# Auto-detect and decode base encodings (base64, hex, base32, base85, url, binary)
uv run ctf-agent-tools crypto base "<payload>" [--scheme auto|hex|base64|base32|base85|url|binary]

# Single-byte XOR key cracker (frequency analysis) or keyed XOR
uv run ctf-agent-tools crypto xor "<hex_or_string>" --crack
uv run ctf-agent-tools crypto xor "<hex_or_string>" --key "<key>"

# Caesar / ROT cipher brute-force or shift
uv run ctf-agent-tools crypto rot "<text>" [--shift 1-25]

# RSA small public exponent or factorized solver
uv run ctf-agent-tools crypto rsa --n <n> --e <e> --c <c> [--p <p>] [--q <q>]

# Decode DTMF audio touch tones from WAV files (auto-detects dial sequences, octal/decimal ASCII, flags)
uv run ctf-agent-tools crypto dtmf <audio_file.wav> [--pattern "<custom_regex>"]
```

### Binary Exploitation (PWN) Domain
```bash
# De Bruijn cyclic pattern creation and offset finder
uv run ctf-agent-tools pwn pattern-create 200
uv run ctf-agent-tools pwn pattern-offset "<needle>"

# Architecture-aware integer packing and unpacking
uv run ctf-agent-tools pwn pack <int_val> [--bits 32|64] [--endian little|big]
uv run ctf-agent-tools pwn unpack "<hex_val>" [--bits 32|64] [--endian little|big]
```

### Reverse Engineering Domain
```bash
# Extract printable strings with regex filter and length threshold
uv run ctf-agent-tools rev strings <file_or_text> [--min-len 4] [--filter "<regex>"]

# Shannon entropy analysis for packed sections or encryption detection
uv run ctf-agent-tools rev entropy <file_or_text>

# Inspect binary architecture, headers, and security mitigations
uv run ctf-agent-tools rev inspect <file_path>
```

### Web & Forensics Domain
```bash
# Decode and inspect JWT structure, claims, and signature header
uv run ctf-agent-tools web jwt "<token>"

# Extract hidden inputs, comments, links, and scripts from HTML
uv run ctf-agent-tools web extract <file_or_html>

# Inspect file magic bytes and MIME types
uv run ctf-agent-tools forensics magic <file_path>

# Carve embedded files (PNG, JPG, ZIP, ELF, PDF) from binary blobs
uv run ctf-agent-tools forensics carve <file_path>

# Generate formatted hexdump
uv run ctf-agent-tools forensics hexdump <file_path> [--length 256] [--offset 0]
```

### A2A / ACP Routing & Ephemeral Sandbox
```bash
# List available specialized sub-agents
uv run ctf-agent-tools a2a agents

# Dispatch sub-task to domain agent (agent-crypto, agent-pwn, agent-rev, etc.)
# Use --adversary to route the task to a Devil's Advocate persona to prevent correlated bias
uv run ctf-agent-tools a2a route <category> "<task_description>" [--data-json "<json>"] [--adversary]

# Check Docker sandbox status
uv run ctf-agent-tools sandbox status

# Verify container has access to ctf, ctf-agent-tools, and gemini
uv run ctf-agent-tools sandbox check

# Run untrusted commands or exploits inside the Docker Compose sandbox
# Note: Sandbox uses split profiles. Base (triage), pwn (pwntools, gcc-aarch64), and forensics (wireshark, mitmproxy, baked-in mitm_deploy.sh for ARP spoofing).
uv run ctf-agent-tools sandbox run "<command>"

# Delegate task across Docker boundary using the File-Based Message Bus (.a2a_inbox.json / .a2a_outbox.json)
# Safely delegates malware analysis or heavy cracking to a specialized sandbox clone
uv run ctf-agent-tools sandbox delegate <problem_id> "<task>" [--profile ctf-sandbox-pwn]
```

### Skill Management & Synchronization
```bash
# Check synchronization status across agent environments
uv run ctf-agent-tools skill status

# Sync latest SKILL.md to user home directories (~/.gemini/skills, ~/.claude/skills)
uv run ctf-agent-tools skill sync
```

## 3. Model Context Protocol (MCP) Server

Launch the native MCP server over stdio to expose all tools to Gemini CLI or Claude:

```bash
uv run ctf-agent-tools mcp serve
```

Exposed MCP tools:
- `help`, `ctf_help`: Interactive tool help, category schemas, and multi-agent swarm/delegation guides (`help(topic="swarm")`, `help(topic="delegation")`, `help(topic="a2a")`).
- `crypto_base_decode`, `crypto_xor_crack`, `crypto_rot_solve`, `crypto_rsa_solve`, `crypto_dtmf_decode`
- `pwn_pattern_create`, `pwn_pattern_offset`, `pwn_pack`, `pwn_unpack`
- `rev_strings`, `rev_entropy`, `rev_inspect_binary`
- `web_jwt_inspect`, `web_extract_html`, `forensics_magic`, `forensics_carve`
- `flag_scan`, `chals_list`, `chals_add`, `chals_solve`, `score_leaderboard`, `a2a_route_task`

For in-depth swarm architecture, agent roles, message schemas, and cross-boundary container bus specifications, refer to `docs/MULTI_AGENT_SWARM.md`.
