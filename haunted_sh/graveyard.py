"""Digital Graveyard for haunted-sh.

Records crashed commands, exit codes, stack traces, and the ghost's epitaphs
into digital headstones stored in ~/.haunted_sh_graveyard.json.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from rich.box import DOUBLE_EDGE, ROUNDED
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

GRAVEYARD_FILE = Path.home() / ".haunted_sh_graveyard.json"
MAX_HEADSTONES = 100


@dataclass
class GraveyardEntry:
    command: str
    exit_code: int
    timestamp: str
    cwd: str
    error_snippet: str
    epitaph: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GraveyardEntry":
        return cls(
            command=data.get("command", "unknown"),
            exit_code=int(data.get("exit_code", 1)),
            timestamp=data.get("timestamp", datetime.now().isoformat()),
            cwd=data.get("cwd", "~"),
            error_snippet=data.get("error_snippet", ""),
            epitaph=data.get("epitaph", "Slain by hubris."),
        )


class Graveyard:
    """Manages the persistence and presentation of slain terminal processes."""

    def __init__(self, filepath: Optional[Path] = None):
        self.filepath = filepath or GRAVEYARD_FILE
        self._entries: List[GraveyardEntry] = []
        self.load()

    def load(self) -> None:
        """Load stored tombstone entries from disk."""
        if not self.filepath.exists():
            self._entries = []
            return

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    self._entries = [GraveyardEntry.from_dict(item) for item in data]
                else:
                    self._entries = []
        except Exception:
            self._entries = []

    def save(self) -> None:
        """Persist tombstones to disk."""
        try:
            self.filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump([asdict(e) for e in self._entries[-MAX_HEADSTONES:]], f, indent=2)
        except Exception:
            pass

    def record_death(
        self,
        command: str,
        exit_code: int,
        cwd: str,
        error_snippet: str,
        epitaph: str,
    ) -> GraveyardEntry:
        """Carve a new tombstone for a perished process."""
        entry = GraveyardEntry(
            command=command,
            exit_code=exit_code,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            cwd=cwd,
            error_snippet=error_snippet[:300].strip(),
            epitaph=epitaph.strip(),
        )
        self._entries.append(entry)
        self.save()
        return entry

    def get_entries(self, limit: int = 10) -> List[GraveyardEntry]:
        """Return the most recent fallen processes."""
        return list(reversed(self._entries[-limit:]))

    def clear(self) -> int:
        """Purge all tombstones from the graveyard."""
        count = len(self._entries)
        self._entries.clear()
        self.save()
        return count

    def get_stats(self) -> Dict[str, Any]:
        """Compute morbidity metrics of the terminal graveyard."""
        total = len(self._entries)
        if total == 0:
            return {
                "total": 0,
                "most_lethal_command": "None yet spared",
                "deadliest_code": 0,
            }

        cmd_counts: Dict[str, int] = {}
        code_counts: Dict[int, int] = {}

        for e in self._entries:
            base_cmd = e.command.split()[0] if e.command.split() else e.command
            cmd_counts[base_cmd] = cmd_counts.get(base_cmd, 0) + 1
            code_counts[e.exit_code] = code_counts.get(e.exit_code, 0) + 1

        top_cmd = max(cmd_counts.items(), key=lambda x: x[1])[0]
        top_code = max(code_counts.items(), key=lambda x: x[1])[0]

        return {
            "total": total,
            "most_lethal_command": f"{top_cmd} ({cmd_counts[top_cmd]} deaths)",
            "deadliest_code": f"Exit {top_code} ({code_counts[top_code]} casualties)",
        }

    def render(self, console: Console, limit: int = 6) -> None:
        """Render ASCII headstones and the graveyard registry table."""
        entries = self.get_entries(limit=limit)
        stats = self.get_stats()

        console.print()
        console.print(
            Panel(
                f"[bold #a855f7]⚰ THE SILICON GRAVEYARD ⚰[/bold #a855f7]\n"
                f"[dim #94a3b8]Here lie {stats['total']} slain processes extinguished before their time.\n"
                f"Most Lethal Incantation: [bold #f43f5e]{stats['most_lethal_command']}[/bold #f43f5e]  •  "
                f"Deadliest Curse: [bold #38bdf8]{stats['deadliest_code']}[/bold #38bdf8][/dim #94a3b8]",
                box=DOUBLE_EDGE,
                border_style="#a855f7",
            )
        )

        if not entries:
            console.print(
                "[italic #00ff9d]No souls wander the graveyard yet. Every command has survived the night... so far.[/italic #00ff9d]\n"
            )
            return

        # Render ASCII Tombstone Gallery (up to 4 in row)
        row_limit = min(len(entries), 4)
        tomb_rows = ["", "", "", "", ""]
        for i in range(row_limit):
            e = entries[i]
            cmd = (e.command.split()[0] if e.command.split() else e.command)[:7]
            code = f"#{e.exit_code}"[:5]
            time_str = e.timestamp.split()[-1][:5]

            tomb_rows[0] += "   .-----.   "
            tomb_rows[1] += "  /  RIP  \  "
            tomb_rows[2] += f" | {cmd:<7} | "
            tomb_rows[3] += f" | {code:<5}{time_str:>2}| "
            tomb_rows[4] += r"  \_______/  "

        console.print(f"[bold #94a3b8]{tomb_rows[0]}[/bold #94a3b8]")
        console.print(f"[bold #a855f7]{tomb_rows[1]}[/bold #a855f7]")
        console.print(f"[bold #f43f5e]{tomb_rows[2]}[/bold #f43f5e]")
        console.print(f"[dim #38bdf8]{tomb_rows[3]}[/dim #38bdf8]")
        console.print(f"[bold #94a3b8]{tomb_rows[4]}[/bold #94a3b8]")
        console.print()

        # Detailed Epitaph Table
        table = Table(
            box=ROUNDED,
            border_style="#7c3aed",
            header_style="bold #00ff9d",
            show_lines=True,
            expand=True,
        )
        table.add_column("Time", style="dim #94a3b8", width=19)
        table.add_column("Command", style="bold #f43f5e", width=22)
        table.add_column("Code", justify="center", style="bold #38bdf8", width=6)
        table.add_column("Spectral Epitaph", style="italic #e2e8f0")

        for e in entries:
            table.add_row(
                e.timestamp,
                f"`{e.command[:20]}`",
                str(e.exit_code),
                f"\"{e.epitaph}\"",
            )

        console.print(table)
        console.print()
