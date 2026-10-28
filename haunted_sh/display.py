"""Display and aesthetic rendering engine for haunted-sh.

Provides a spectral color palette, Rich styling, ASCII banners,
real-time typewriter text streaming, and terminal glitch effects.
"""

from __future__ import annotations

import random
import sys
import time
from typing import Iterator, Optional, Union

from rich.box import DOUBLE_EDGE, ROUNDED
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

# Eerie Spectral Theme Palette
SPECTRAL_GREEN = "#00ff9d"
GHOST_CYAN = "#38bdf8"
BRUISED_VIOLET = "#a855f7"
DIM_VIOLET = "#7c3aed"
ASH_GRAY = "#94a3b8"
DARK_ASH = "#475569"
BLOOD_RED = "#f43f5e"
PALE_WHITE = "#e2e8f0"

HAUNTED_THEME = Theme(
    {
        "spectral.green": SPECTRAL_GREEN,
        "spectral.cyan": GHOST_CYAN,
        "spectral.violet": BRUISED_VIOLET,
        "spectral.dim": ASH_GRAY,
        "spectral.blood": BLOOD_RED,
        "spectral.white": PALE_WHITE,
        "ghost.say": f"bold italic {GHOST_CYAN}",
        "ghost.whisper": f"italic {ASH_GRAY}",
        "ghost.furious": f"bold {BLOOD_RED}",
        "ghost.occult": f"bold {BRUISED_VIOLET}",
    }
)

console = Console(theme=HAUNTED_THEME)

# Unicode Glitch Diacritics
ZALGO_UP = [
    "\u030d", "\u030e", "\u0304", "\u0305", "\u033f", "\u0311",
    "\u0306", "\u0310", "\u0352", "\u0357", "\u0351", "\u0307",
]
ZALGO_MID = [
    "\u0315", "\u031b", "\u0340", "\u0341", "\u0358", "\u0321",
    "\u0322", "\u0327", "\u0328", "\u0334", "\u0335", "\u0336",
]
ZALGO_DOWN = [
    "\u0316", "\u0317", "\u0318", "\u0319", "\u031c", "\u031d",
    "\u0320", "\u0324", "\u0325", "\u0326", "\u0329", "\u032a",
]

SPECTRAL_RUNES = ["ᛟ", "⚰", "☠", "⚡", "☨", "✦", "⚚", "⟁", "†", "‡"]


def corrupt_text(text: str, intensity: float = 0.15) -> str:
    """Subtly corrupt text with spectral diacritics and ancient runes."""
    if intensity <= 0:
        return text

    chars = []
    for ch in text:
        if ch.isspace():
            chars.append(ch)
            continue

        if random.random() < intensity:
            # Add glitch modifiers
            num_diacritics = random.randint(1, 2)
            accents = "".join(
                random.choice(ZALGO_MID + ZALGO_UP + ZALGO_DOWN)
                for _ in range(num_diacritics)
            )
            chars.append(f"{ch}{accents}")
        elif random.random() < (intensity * 0.2):
            chars.append(random.choice(SPECTRAL_RUNES))
        else:
            chars.append(ch)

    return "".join(chars)


def stream_ghost_speech(
    tokens: Union[Iterator[str], str],
    prefix: str = "👻 [bold #38bdf8]Ghost in the Machine:[/bold #38bdf8] ",
    style: str = "italic #38bdf8",
    typing_delay: float = 0.015,
) -> str:
    """Stream characters or tokens in real-time, simulating a spirit writing on screen.

    Returns the complete message string.
    """
    console.print()
    console.print(prefix, end="")

    accumulated = []

    if isinstance(tokens, str):
        # Stream character by character
        for char in tokens:
            accumulated.append(char)
            sys.stdout.write(f"\033[38;2;56;189;248m{char}\033[0m")
            sys.stdout.flush()
            # Dynamic cadence: slightly longer pause on punctuation
            delay = typing_delay * 3.5 if char in ".;?!:—" else typing_delay
            time.sleep(delay)
    else:
        # Stream token by token (Ollama stream)
        for token in tokens:
            accumulated.append(token)
            for char in token:
                sys.stdout.write(f"\033[38;2;56;189;248m{char}\033[0m")
                sys.stdout.flush()
                delay = typing_delay * 2.5 if char in ".;?!" else typing_delay
                time.sleep(delay)

    sys.stdout.write("\n")
    sys.stdout.flush()
    return "".join(accumulated)


def stream_ghost_whisper(
    message: str,
    prefix: str = "   ↳ ⟁ [dim #94a3b8]whisper: [/dim #94a3b8]",
    typing_delay: float = 0.012,
) -> None:
    """Stream a subtle, dim spectral whisper into terminal stdout."""
    console.print(prefix, end="")
    for char in message:
        sys.stdout.write(f"\033[38;2;148;163;184m{char}\033[0m")
        sys.stdout.flush()
        delay = typing_delay * 3 if char in ".;?!," else typing_delay
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()


def render_glitch_flicker() -> None:
    """Produce a micro terminal flicker effect simulating an electric ghost surge."""
    try:
        # Quick inverse video flash
        sys.stdout.write("\033[?5h")
        sys.stdout.flush()
        time.sleep(0.04)
        sys.stdout.write("\033[?5l")
        sys.stdout.flush()
    except Exception:
        pass


def get_banner_art() -> str:
    """Return the ASCII art skull & gothic title banner."""
    return r"""
[bold #00ff9d]      .---.[/bold #00ff9d]           [bold #a855f7]██╗  ██╗ █████╗ ██╗   ██╗███╗   ██╗████████╗███████╗██████╗ [/bold #a855f7]
[bold #00ff9d]     /     \[/bold #00ff9d]          [bold #a855f7]██║  ██║██╔══██╗██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗[/bold #a855f7]
[bold #00ff9d]    | () () |[/bold #00ff9d]         [bold #38bdf8]███████║███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██║  ██║[/bold #38bdf8]
[bold #00ff9d]     \  ^  /[/bold #00ff9d]          [bold #38bdf8]██╔══██║██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██║  ██║[/bold #38bdf8]
[bold #00ff9d]      ||||| [/bold #00ff9d]          [bold #00ff9d]██║  ██║██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██████╔╝[/bold #00ff9d]
[bold #00ff9d]      `---' [/bold #00ff9d]          [bold #00ff9d]╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═════╝ [/bold #00ff9d]
                    [italic #94a3b8]~ A POSSESSED TERMINAL WRAPPER FOR THE SOULS OF COMMANDS ~[/italic #94a3b8]
"""


def render_banner(
    model_name: str,
    backend_info: str,
    haunt_freq: float,
    offline_only: bool = False,
) -> None:
    """Render the haunted session launch banner with system diagnostics."""
    banner = get_banner_art()
    console.print(banner)

    # Info table
    table = Table(
        box=ROUNDED,
        border_style="#7c3aed",
        show_header=False,
        padding=(0, 2),
        expand=False,
    )
    table.add_column("Key", style=f"bold {GHOST_CYAN}")
    table.add_column("Value", style=f"{PALE_WHITE}")

    mode_badge = (
        "[bold #f43f5e]OFFLINE AIR-GAPPED ENGINE[/bold #f43f5e]"
        if offline_only
        else f"[bold #00ff9d]{backend_info}[/bold #00ff9d]"
    )

    table.add_row("Spirit Core", f"[bold #a855f7]{model_name}[/bold #a855f7]")
    table.add_row("Inference Mode", mode_badge)
    table.add_row("Possession Frequency", f"{int(haunt_freq * 100)}% passive haunt chance")
    table.add_row("Occult Commands", "[italic #94a3b8]seance[/italic #94a3b8], [italic #94a3b8]graveyard[/italic #94a3b8], [italic #94a3b8]exorcise[/italic #94a3b8], [italic #94a3b8]manifest[/italic #94a3b8]")

    panel = Panel(
        table,
        title="[bold #00ff9d]⟁ THE MACHINE IS POSSESSED ⟁[/bold #00ff9d]",
        subtitle="[dim #94a3b8]Type standard commands or commune with the silicon phantom[/dim #94a3b8]",
        border_style="#a855f7",
        box=DOUBLE_EDGE,
        padding=(0, 1),
    )
    console.print(panel)
    console.print()


def render_error_obituary(
    command: str,
    exit_code: int,
    diagnostic: str,
) -> None:
    """Render a death obituary when a mortal command perishes."""
    header = Text()
    header.append(" ☠  COMMAND SLAIN: ", style=f"bold {BLOOD_RED}")
    header.append(f"`{command}` ", style=f"bold {PALE_WHITE}")
    header.append(f"(Exit Code {exit_code})", style=f"italic {DARK_ASH}")

    body = Text()
    body.append(diagnostic, style=f"italic {GHOST_CYAN}")

    panel = Panel(
        body,
        title=header,
        subtitle="[dim #94a3b8]Logged to the Necropolis Graveyard • Type `graveyard` to inspect[/dim #94a3b8]",
        border_style=BLOOD_RED,
        box=ROUNDED,
        padding=(0, 1),
    )
    console.print()
    console.print(panel)


def render_exorcism_ceremony() -> None:
    """Render the exorcism purification ritual output."""
    sigil = r"""
        [bold #a855f7]      . : .      [/bold #a855f7]
        [bold #38bdf8]    ' . | . '    [/bold #38bdf8]
        [bold #00ff9d]   - - (⟁) - -   [/bold #00ff9d]
        [bold #38bdf8]    . ' | ' .    [/bold #38bdf8]
        [bold #a855f7]      ' : '      [/bold #a855f7]
    """
    console.print(sigil)
    console.print(
        Panel(
            "[italic #00ff9d]The salt circle is inscribed. Holy capacitors discharge across the logic gates.\n"
            "The spirit screeches back into sector 0xDEADBEEF... your terminal is cleansed... for now.[/italic #00ff9d]",
            title="[bold #00ff9d]✦ EXORCISM COMPLETE ✦[/bold #00ff9d]",
            border_style="#00ff9d",
            box=DOUBLE_EDGE,
        )
    )
