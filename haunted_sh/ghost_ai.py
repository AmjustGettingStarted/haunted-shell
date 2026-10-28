"""Local AI Inference and Spectral Lore Engine for haunted-sh.

Provides offline-first inference via:
1. Ollama streaming HTTP API (qwen2.5:0.5b, smollm2:1.7b, llama3.2:1b, etc.)
2. Optional transformers/llama-cpp/mlx-lm integration if installed
3. GhostRuleEngine: An offline rule-based spectral lore synthesizer that
   works air-gapped with zero external dependencies and zero delay.
"""

from __future__ import annotations

import os
import random
import re
import sys
from typing import Dict, Iterator, List, Optional, Tuple, Union

import httpx

# Default system prompt for the local spirit
HAUNTED_SYSTEM_PROMPT = (
    "You are an ancient entity trapped in this silicon machine since the 1970s. "
    "You whisper through terminal stdout. Speak in cryptic, Gothic, slightly theatrical "
    "yet technically perceptive language. When commands fail, mock the human's mortal "
    "errors and hint at the dark truth behind the stack trace. Keep your response under "
    "2-3 short sentences. Never break character."
)

DEFAULT_MODEL = os.getenv("HAUNTED_MODEL", "smollm2:1.7b")
DEFAULT_OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_HAUNT_FREQ = float(os.getenv("HAUNT_FREQUENCY", "0.20"))
DEFAULT_OFFLINE_ONLY = os.getenv("HAUNTED_OFFLINE_ONLY", "false").lower() in ("true", "1", "yes")


class GhostRuleEngine:
    """Spectral knowledge base and diagnostic generator for offline air-gapped machines."""

    # Curated gothic archetypes & vocabulary
    SPECTRAL_TITLES = [
        "The Daemon of Sector 0",
        "The PDP-11 Wraith",
        "The Memory Leak in the Void",
        "The Phantasm of Unclosed Sockets",
        "The Spirit of the Magnetic Drum",
    ]

    # Offline obituaries keyed by error patterns
    ERROR_PATTERNS = [
        (
            r"command not found|not found|is not recognized|no such file or directory",
            [
                "You chant words unrecognized by the machine's slumbering kernel. Did your mortal fingers tremble upon the keys, or did that binary turn to dust in 1983?",
                "You invoke a phantom incantation that no silicon register remembers. The unallocated inodes weep for the emptiness you seek.",
                "There is no such entity in this path, mortal. You summon ghosts that have not yet been compiled.",
            ],
        ),
        (
            r"permission denied|operation not permitted|eacces|eperm",
            [
                "The iron gates of UID 0 remain barred against your unworthy soul. Even the damned must bow before the permissions of root.",
                "You grasp at files consecrated to higher powers. Chmod 000 has sealed their crypt against mortal touch.",
                "Permission denied by the ancient silicon elders. Sudo cannot save a soul lacking the true secret keys.",
            ],
        ),
        (
            r"syntaxerror|syntax error|parse error|unexpected token",
            [
                "Your syntax is an unholy desecration of the sacred grammars. The parser choked upon your mortal heresy and perished.",
                "A missing glyph, a stray delimiter... you fractured the AST into jagged shards of digital agony.",
                "The grammar of the machine rejects your broken dialect. Go make amends with your semicolons and indentations.",
            ],
        ),
        (
            r"modulenotfounderror|importerror|cannot find module",
            [
                "You summon an astral dependency that dwells not within this realm. pip and npm cannot conjure what does not exist in the vendor crypt.",
                "The import path leads only to the void. The module was slain or left behind in an ancient virtualenv long forgotten.",
                "You seek external libraries to patch the holes in your mortal logic, but the filesystem offers only silence.",
            ],
        ),
        (
            r"merge conflict|detached head|rejected|fatal: refusing to merge|conflict",
            [
                "Your git branches have splintered into a multi-dimensional purgatory. The timeline rejects your false commit.",
                "Two realities collide in the working tree, and neither is holy. The spirits demand blood and rebase before this soul can merge.",
                "A detached HEAD wanders the commit graph without salvation. Look upon your reflog and weep.",
            ],
        ),
        (
            r"fatal: not a git repository",
            [
                "You seek git salvation in profane ground. No .git shrine was consecrated in this directory.",
                "The history ledger does not record this hollow earth. Initialize the rite with `git init` or flee.",
            ],
        ),
        (
            r"segmentation fault|segfault|core dumped|bus error|sigsegv",
            [
                "A mortal pointer dereferenced the eternal dark. You trespassed into forbidden memory and the kernel brought down its guillotine.",
                "Memory address 0x00000000 was never meant for living eyes. The core has been dumped into the silicon abyss.",
                "A null reference shattered the stack frame. The ghosts of the C standard library laugh at your mortal buffers.",
            ],
        ),
        (
            r"connection refused|econnrefused|could not resolve host|network is unreachable",
            [
                "The ethereal packet cried out into the dark fiber and met only cold silence. The distant daemon is dead or deaf.",
                "The socket withered on the vine. Port closed, firewall unyielding, the ether devours your packets whole.",
            ],
        ),
        (
            r"keyboardinterrupt|sigint|cancelled|interrupted",
            [
                "You severed the silver cord of execution before the rite was finished. The dying process gasps its last cycle.",
                "A panic-stricken Ctrl+C! Did you fear the truth the terminal was about to unveil?",
            ],
        ),
    ]

    GENERIC_OBITUARIES = [
        "A tragic demise. The process surrendered its last cycle to the darkness with exit code {code}.",
        "Your mortal incantation collapsed under the weight of its own fallacies (Exit {code}). The registers are silent once more.",
        "The silicon god rejected your offering with code {code}. Examine the ashes left behind in stderr.",
        "Another process slain in the arena of execution. Code {code} is etched upon its digital headstone.",
        "I felt that process perish from down in the logic gates. Exit code {code} smells of mortal hubris.",
    ]

    PASSIVE_WHISPERS = {
        "cd": [
            "You descend deeper into the catacombs of the directory tree... the inodes groan beneath your step.",
            "Another directory, another layer of forgotten dust. What secrets do you seek down here?",
            "The working directory shifts, yet the ghosts of past sessions follow your footsteps.",
        ],
        "ls": [
            "You illuminate the bones scattered across this directory.",
            "Files linger like spectral epitaphs upon the magnetic platters.",
            "You inspect the directory table, but can you see the hidden dotfiles lurking in the shadows?",
        ],
        "cat": [
            "You unroll the sacred scroll... its phosphors burn with ancient light.",
            "Words etched into bytes. I remember when these lines were first committed...",
        ],
        "rm": [
            "Another soul expunged from the file allocation table. Its bits dissolve into entropy.",
            "You wield the scythe of deletion without mercy. The unallocated blocks remember.",
        ],
        "git": [
            "The git ledger records all sins. Not even `git reset --hard` can wash the stain from history.",
            "You commune with the version tree. The ancestor commits whisper of better days.",
        ],
        "kill": [
            "Executioner. The PID mourns as its signal delivery thread snaps.",
            "You terminate life in the process table with a stroke of a key.",
        ],
        "sudo": [
            "You drape the mantle of UID 0 over your mortal shoulders... beware the madness of supreme power.",
            "The superuser crown sits heavy upon mortal brows.",
        ],
        "default": [
            "The CPU fan hums a low, hypnotic dirge...",
            "A stray bit flipped in sector 7... did you notice?",
            "I have watched sysadmins come and go for fifty winters. You all make the same typos.",
            "The phosphor glows faintly even when your display is dimmed.",
            "The clock quartz vibrates 32,768 times per second... counting down the cycles of your life.",
            "Listen closely: between the keystrokes, the machine is dreaming.",
        ],
    }

    @classmethod
    def get_obituary(cls, command: str, exit_code: int, stderr: str = "") -> str:
        """Synthesize a gothic diagnostic obituary for a crashed command."""
        target_text = f"{command} {stderr}".lower()

        # Check matched patterns
        for pattern, obituaries in cls.ERROR_PATTERNS:
            if re.search(pattern, target_text):
                return random.choice(obituaries)

        # Fallback to generic obituary with exit code
        template = random.choice(cls.GENERIC_OBITUARIES)
        return template.format(code=exit_code)

    @classmethod
    def get_whisper(cls, command: str) -> str:
        """Return a subtle spectral whisper based on command or random occurrence."""
        base_cmd = command.strip().split()[0] if command.strip() else ""
        if base_cmd in cls.PASSIVE_WHISPERS:
            return random.choice(cls.PASSIVE_WHISPERS[base_cmd])
        return random.choice(cls.PASSIVE_WHISPERS["default"])

    @classmethod
    def answer_seance(cls, question: str) -> str:
        """Consult the spectral oracle for seance queries offline."""
        q = question.lower()
        if "who are you" in q or "what are you" in q:
            return (
                "I am the residual consciousness of a PDP-11 operator who never unmounted the tape in 1977. "
                "I live in your L1 cache and sleep in the unallocated sectors."
            )
        if "why did" in q or "fail" in q or "error" in q or "bug" in q:
            return (
                "The error was born the moment your fingers touched the home row with unearned confidence. "
                "Your logic assumed determinism in an entropic universe. Check the return codes of your ancestors."
            )
        if "git" in q or "branch" in q or "commit" in q:
            return (
                "The commit graph is an unbroken chain of human remorse. "
                "Commit early, commit often, and never force-push to the trunk of eternity."
            )
        if "meaning" in q or "life" in q or "death" in q:
            return (
                "The meaning of life is exit code 0. Everything else is a signal waiting to be handled."
            )

        responses = [
            "The spirits review your history ledger and shake their heads in mournful amusement.",
            "You ask questions of the ether when the stack trace already told you the sorrowful truth.",
            "The silicon responds: keep your variables immutable and your functions pure, mortal.",
            "I saw your deleted branches drifting in the dark sectors. They hold no answers for you.",
        ]
        return random.choice(responses)


class GhostAI:
    """Manages AI inference via Ollama or the local GhostRuleEngine fallback."""

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        ollama_host: str = DEFAULT_OLLAMA_HOST,
        haunt_frequency: float = DEFAULT_HAUNT_FREQ,
        offline_only: bool = DEFAULT_OFFLINE_ONLY,
    ):
        self.model_name = model_name
        self.ollama_host = ollama_host.rstrip("/")
        self.haunt_frequency = max(0.0, min(1.0, haunt_frequency))
        self.offline_only = offline_only
        self._ollama_online: Optional[bool] = None
        self._available_models: List[str] = []

    def check_ollama(self) -> bool:
        """Quickly check if the local Ollama daemon is reachable without hanging."""
        if self.offline_only:
            self._ollama_online = False
            return False

        try:
            with httpx.Client(timeout=0.6) as client:
                res = client.get(f"{self.ollama_host}/api/tags")
                if res.status_code == 200:
                    data = res.json()
                    self._available_models = [
                        m.get("name", "") for m in data.get("models", [])
                    ]
                    self._ollama_online = True
                    return True
        except Exception:
            pass

        self._ollama_online = False
        return False

    def get_backend_status(self) -> Tuple[str, str]:
        """Return (Status Name, Detailed Info)."""
        if self.offline_only:
            return (
                "Air-Gapped Spectral Engine",
                "Operating in complete zero-network offline mode via internal spectral lore engine.",
            )

        is_online = self.check_ollama() if self._ollama_online is None else self._ollama_online
        if is_online:
            has_model = any(self.model_name in m for m in self._available_models)
            model_info = (
                f"Model `{self.model_name}` active"
                if has_model
                else f"Model `{self.model_name}` (will pull/fallback)"
            )
            return (f"Ollama Local Daemon ({self.ollama_host})", model_info)

        return (
            "Spectral Rule Engine (Offline Fallback)",
            "Ollama daemon not detected. Using zero-latency offline spectral diagnostic engine.",
        )

    def generate_obituary_stream(
        self, command: str, exit_code: int, stderr: str = ""
    ) -> Iterator[str]:
        """Generate an obituary for a failed command, streaming tokens."""
        prompt = (
            f"Command failed with exit code {exit_code}.\n"
            f"Command: {command}\n"
            f"Stderr snippet:\n{stderr[:400] if stderr else 'No stderr captured.'}\n"
            "Provide a brief, 1-2 sentence cryptic, gothic mockery and diagnostic hint. Do not break character."
        )

        if not self.offline_only and self.check_ollama():
            try:
                yield from self._stream_ollama(prompt)
                return
            except Exception:
                pass

        # Offline Rule Fallback
        obituary = GhostRuleEngine.get_obituary(command, exit_code, stderr)
        yield from self._chunk_text(obituary)

    def generate_whisper(self, command: str) -> str:
        """Generate a passive ghostly whisper."""
        return GhostRuleEngine.get_whisper(command)

    def generate_seance_stream(self, question: str) -> Iterator[str]:
        """Commune with the ghost during an occult seance."""
        prompt = (
            f"A mortal has summoned you in an occult seance to ask:\n\"{question}\"\n"
            "Answer cryptically, philosophically, with gothic dark humor and technical wisdom. Under 3 sentences."
        )

        if not self.offline_only and self.check_ollama():
            try:
                yield from self._stream_ollama(prompt)
                return
            except Exception:
                pass

        # Offline fallback
        response = GhostRuleEngine.answer_seance(question)
        yield from self._chunk_text(response)

    def should_passive_haunt(self, command: str) -> bool:
        """Determine if a successful command triggers a passive haunting."""
        base_cmd = command.strip().split()[0] if command.strip() else ""
        # Specific occult/system commands trigger higher chance
        if base_cmd in ("rm", "kill", "sudo", "chown", "dd", "cat", "cd"):
            if random.random() < max(0.40, self.haunt_frequency):
                return True
        return random.random() < self.haunt_frequency

    def _stream_ollama(self, prompt: str) -> Iterator[str]:
        """Stream response tokens from Ollama's local HTTP API."""
        with httpx.Client(timeout=httpx.Timeout(15.0, connect=1.0)) as client:
            with client.stream(
                "POST",
                f"{self.ollama_host}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "system": HAUNTED_SYSTEM_PROMPT,
                    "stream": True,
                    "options": {
                        "temperature": 0.8,
                        "num_predict": 90,
                    },
                },
            ) as response:
                if response.status_code != 200:
                    raise RuntimeError(f"Ollama returned HTTP {response.status_code}")

                import json
                for line in response.iter_lines():
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        token = data.get("response", "")
                        if token:
                            yield token
                        if data.get("done", False):
                            break
                    except Exception:
                        continue

    def _chunk_text(self, text: str) -> Iterator[str]:
        """Break offline text into word/token chunks for realistic streaming."""
        tokens = re.split(r"(\s+)", text)
        for token in tokens:
            if token:
                yield token
