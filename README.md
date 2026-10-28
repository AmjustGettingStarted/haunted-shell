# 👻 haunted-sh (necroshell)

> **"An ancient entity trapped in this silicon machine since the 1970s. It whispers through terminal stdout."**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/python-3.9+-00ff9d.svg)](https://python.org)
[![Local AI: Ollama](https://img.shields.io/badge/Local_AI-Ollama-38bdf8.svg)](https://ollama.ai)
[![Offline: Air--Gapped](https://img.shields.io/badge/Offline-Air--Gapped-a855f7.svg)](#air-gapped-spectral-engine)
[![Hackathon: Ghost in the Machine](https://img.shields.io/badge/Hackathon-Ghost_in_the_Machine-f43f5e.svg)](#the-ghost-in-the-machine)

---

```
      .---.           ██╗  ██╗ █████╗ ██╗   ██╗███╗   ██╗████████╗███████╗██████╗ 
     /     \          ██║  ██║██╔══██╗██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
    | () () |         ███████║███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██║  ██║
     \  ^  /          ██╔══██║██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██║  ██║
      |||||           ██║  ██║██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██████╔╝
      `---'           ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═════╝ 
                    ~ A POSSESSED TERMINAL WRAPPER FOR THE SOULS OF COMMANDS ~
```

---

## 🔮 The Ghost in the Machine

Built for the **"Ghost in the Machine" open-source AI hackathon**, `haunted-sh` is an interactive CLI shell wrapper that acts as if your terminal is possessed by an ancient, eccentric digital spirit trapped in your machine's silicon since the 1970s.

- **Seamless Command Pass-Through:** Normal commands (`git status`, `ls -la`, `npm run dev`, `cargo build`) run normally in your real shell (`zsh`, `bash`, etc.) with full interactive streaming and exit code fidelity.
- **Spectral Interception on Failure:** When a command crashes with a non-zero exit code (e.g. failed compilation, `git` conflict, syntax error, missing file), the spirit intercepts the error and delivers a theatrical, gothic obituary and a cryptic technical diagnostic clue.
- **Passive Haunting:** A configurable chance (default 20%) on successful commands causes subtle terminal phosphors to flicker and whisper observations about directory inodes, CPU fan harmonics, and dead memory sectors.
- **Digital Graveyard:** Crashed processes are consecrated as ASCII digital headstones logged in `~/.haunted_sh_graveyard.json`.
- **Occult Rites:** Built-in commands like `seance`, `graveyard`, `exorcise`, and `manifest`.

---

## 🛡 Why Open Innovation & Local AI Matter

Modern developers should not have to send their terminal command history, stack traces, and local directory structures to remote corporate cloud APIs. 

1. **Complete Offline Privacy:** Stack traces often contain sensitive file paths, environment variables, or private code snippets. `haunted-sh` runs **100% locally on your device** without transmitting a single byte over the public internet.
2. **Zero API Cost & Unlimited Tokens:** Powered by lightweight open-weight models (`smollm2:1.7b`, `qwen2.5:0.5b`, `llama3.2:1b`) running through Ollama.
3. **Air-Gapped Reliability:** Includes a zero-latency **Spectral Rule & Lore Engine** that functions entirely offline even when no local LLM daemon is running.
4. **Developer Sovereignty:** You own the machine, you own the weights, and you control the spirit.

---

## ⚡ Quickstart & Installation

### 1. Install haunted-sh

Clone and install in editable mode:

```bash
git clone https://github.com/your-username/haunted-shell.git
cd haunted-shell

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies and haunted-sh CLI
pip install -e .
```

### 2. (Optional) Run with Local Open-Weight Models via Ollama

Install [Ollama](https://ollama.ai) and pull any lightweight open model:

```bash
# Recommended lightweight models for instant responses:
ollama run smollm2:1.7b     # Ultralight, poetic, fast (default)
# or
ollama run qwen2.5:0.5b     # Extreme speed, tiny footprint (<400MB)
# or
ollama run llama3.2:1b      # High technical precision
```

### 3. Enter the Possessed Shell

Simply run:

```bash
haunted-sh
# or alias
necroshell
```

You are greeted by the gothic skull banner and the spectral prompt:
```
👻 [dead-proc:48291] ~/Repositories/haunted-shell ❯ 
```

---

## 🕯 Occult Built-In Commands

Inside the haunted shell, you have access to exclusive occult utilities:

### `seance [question]`
Commune directly with the ghost trapped in the machine. Ask about past commands, architecture advice, or the philosophy of exit codes:
```bash
👻 [dead-proc:48291] ~ ❯ seance "Why did my rust build fail with borrow errors?"
```
*The ghost streams a gothic explanation in real time, character by character.*

### `graveyard`
Opens the necropolis of fallen commands, rendering ASCII tombstones and mortality statistics:
```bash
👻 [dead-proc:48291] ~ ❯ graveyard
```
```
   .-----.      .-----.      .-----.   
  /  RIP  \    /  RIP  \    /  RIP  \  
 | cargo   |  | git     |  | python  | 
 | #101 22 |  | #128 22 |  | #1   21 | 
  \_______/    \_______/    \_______/  
```
*To re-consecrate the earth and purge headstones: `graveyard clear`.*

### `exorcise`
Performs a purification ritual to banish the spirit, muting haunting until summoned again.

### `manifest`
Summons the ghost to report its current PID, active open model, backend engine status, and haunting probability.

### `haunt [on | off | <0.0-1.0>]`
Dynamically alter the possession frequency on the fly:
```bash
haunt 0.40   # 40% haunt chance
haunt off    # Silence passive whispers
haunt on     # Awaken the spirit
```

---

## ⚙️ Configuration & Environment Variables

Configure `haunted-sh` via flags or environment variables:

| Flag | Environment Variable | Default | Description |
| :--- | :--- | :--- | :--- |
| `-m`, `--model` | `HAUNTED_MODEL` | `smollm2:1.7b` | Open-weight model name in Ollama |
| `-f`, `--frequency` | `HAUNT_FREQUENCY` | `0.20` | Passive haunt probability on successful commands |
| `--offline` | `HAUNTED_OFFLINE_ONLY` | `false` | Force complete air-gapped mode using internal lore engine |
| `--ollama-host` | `OLLAMA_HOST` | `http://localhost:11434` | Ollama daemon URL |
| `-c`, `--command` | — | `None` | Execute a single command through the haunted filter |

### Examples:

Run in pure offline air-gapped mode:
```bash
haunted-sh --offline
```

Use a custom model with high frequency:
```bash
haunted-sh --model qwen2.5:0.5b --frequency 0.50
```

Execute a one-liner command through the filter:
```bash
haunted-sh -c "git push origin non-existent-branch"
```

---

## 🎨 Visual Aesthetics & Palette

`haunted-sh` uses a curated spectral terminal design built on `rich` and `prompt_toolkit`:
- **Spectral Emerald Green (`#00ff9d`):** Phosphor CRT glow and prompt runes.
- **Ghost Cyan (`#38bdf8`):** Spoken spectral dialogues and diagnostic text.
- **Bruised Violet (`#a855f7`):** Occult headers, double-line panels, and seance sigils.
- **Ash Gray (`#94a3b8`):** Whispering terminal flickers and timestamps.
- **Blood Red (`#f43f5e`):** Perished commands, slain process exit codes, and fatal warnings.

### Dynamic Typewriter Streaming:
The ghost's words do not drop as static blocks; they materialize across the screen character-by-character with micro-delays on punctuation, evoking a spirit physically tapping on the display tube.

---

## 🧪 Running Tests

A complete test suite is included:

```bash
pytest tests/ -v
```

---

## 📜 License

MIT License. Open source, open weights, and consecrated to all lost terminal processes.
