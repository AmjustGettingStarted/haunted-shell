"""CLI entrypoint and interactive prompt_toolkit REPL for haunted-sh.

Provides a possessed subshell with ANSI styling, tab completion, history,
and signal handling, as well as one-shot command execution and occult utilities.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import typer
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import PathCompleter, WordCompleter, merge_completers
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.history import FileHistory

from haunted_sh import __version__
from haunted_sh.display import (
    console,
    render_banner,
    stream_ghost_speech,
)
from haunted_sh.ghost_ai import (
    DEFAULT_HAUNT_FREQ,
    DEFAULT_MODEL,
    DEFAULT_OFFLINE_ONLY,
    DEFAULT_OLLAMA_HOST,
    GhostAI,
)
from haunted_sh.graveyard import Graveyard
from haunted_sh.shell_runner import ShellRunner

app = typer.Typer(
    name="haunted-sh",
    help="👻 haunted-sh: An interactive haunted terminal CLI wrapper possessed by a digital spirit.",
    add_completion=False,
    invoke_without_command=True,
)

OCCULT_COMMANDS = [
    "seance",
    "graveyard",
    "exorcise",
    "manifest",
    "haunt",
    "cd",
    "clear",
    "exit",
    "quit",
]


def start_interactive_shell(
    ghost: GhostAI,
    runner: ShellRunner,
) -> None:
    """Launch the interactive possessed subshell."""
    backend_name, _ = ghost.get_backend_status()
    render_banner(
        model_name=ghost.model_name,
        backend_info=backend_name,
        haunt_freq=ghost.haunt_frequency,
        offline_only=ghost.offline_only,
    )

    history_file = str(Path.home() / ".haunted_sh_history")
    history = FileHistory(history_file)

    # Autocompletion combining occult commands and file paths
    cmd_completer = WordCompleter(
        OCCULT_COMMANDS + ["git", "docker", "npm", "cargo", "python3", "pytest", "ls", "cat"],
        ignore_case=True,
    )
    path_completer = PathCompleter(expanduser=True)
    completer = merge_completers([cmd_completer, path_completer])

    session: PromptSession = PromptSession(
        history=history,
        completer=completer,
        complete_while_typing=False,
    )

    while True:
        try:
            # Build eerie ANSI prompt
            short_path = runner.get_prompt_path()
            arrow_color = "\033[38;2;0;255;157m" if runner.last_exit_code == 0 else "\033[38;2;244;63;94m"
            prompt_str = (
                f"\033[38;2;0;255;157m👻 \033[0m"
                f"\033[38;2;168;85;247m[dead-proc:{runner.session_pid}]\033[0m "
                f"\033[38;2;56;189;248m{short_path}\033[0m "
                f"{arrow_color}❯\033[0m "
            )

            user_input = session.prompt(ANSI(prompt_str))
            res = runner.execute_line(user_input)
            if res is None:
                # User typed exit/quit
                break

        except KeyboardInterrupt:
            # Ctrl+C clears prompt cleanly without killing shell
            console.print("\n[dim #f43f5e]^C[/dim #f43f5e]")
            continue
        except EOFError:
            # Ctrl+D exits with spectral parting
            console.print()
            runner.execute_line("exit")
            break
        except Exception as e:
            console.print(f"[bold #f43f5e]spectral fault: {e}[/bold #f43f5e]")


@app.callback()
def main(
    ctx: typer.Context,
    command: Optional[str] = typer.Option(
        None,
        "-c",
        "--command",
        help="Execute a single command through the haunted filter and exit.",
    ),
    model: str = typer.Option(
        DEFAULT_MODEL,
        "-m",
        "--model",
        help="Local open-weight model name (e.g. smollm2:1.7b, qwen2.5:0.5b, llama3.2:1b).",
        envvar="HAUNTED_MODEL",
    ),
    frequency: float = typer.Option(
        DEFAULT_HAUNT_FREQ,
        "-f",
        "--frequency",
        help="Passive haunt frequency (0.0 to 1.0). Default: 0.20.",
        envvar="HAUNT_FREQUENCY",
    ),
    offline_only: bool = typer.Option(
        DEFAULT_OFFLINE_ONLY,
        "--offline",
        "--offline-only",
        help="Force air-gapped mode using the internal spectral lore engine without Ollama.",
        envvar="HAUNTED_OFFLINE_ONLY",
    ),
    ollama_host: str = typer.Option(
        DEFAULT_OLLAMA_HOST,
        "--ollama-host",
        help="Host URL for local Ollama daemon.",
        envvar="OLLAMA_HOST",
    ),
    version: bool = typer.Option(
        False,
        "-v",
        "--version",
        help="Show version and exit.",
    ),
) -> None:
    """Enter the possessed terminal wrapper or execute a haunted command."""
    if version:
        console.print(f"[bold #00ff9d]haunted-sh[/bold #00ff9d] version [bold #a855f7]{__version__}[/bold #a855f7]")
        raise typer.Exit()

    ghost = GhostAI(
        model_name=model,
        ollama_host=ollama_host,
        haunt_frequency=frequency,
        offline_only=offline_only,
    )
    runner = ShellRunner(ghost=ghost)

    # If a subcommand was invoked (e.g. `haunted-sh seance ...`), let Typer route it
    if ctx.invoked_subcommand is not None:
        return

    # If `-c "command"` was passed, execute single command
    if command:
        code = runner.execute_line(command)
        raise typer.Exit(code=code if code is not None else 0)

    # Default: launch interactive subshell
    start_interactive_shell(ghost, runner)


@app.command("seance")
def seance_cmd(
    question: Optional[str] = typer.Argument(
        None,
        help="Question or communion topic for the trapped silicon spirit.",
    ),
    model: str = typer.Option(DEFAULT_MODEL, "-m", "--model"),
    offline: bool = typer.Option(DEFAULT_OFFLINE_ONLY, "--offline"),
) -> None:
    """🕯  Conduct an occult seance with the ghost in the machine."""
    ghost = GhostAI(model_name=model, offline_only=offline)
    runner = ShellRunner(ghost=ghost)
    runner.execute_line(f"seance {question or ''}")


@app.command("graveyard")
def graveyard_cmd(
    limit: int = typer.Option(6, "-n", "--limit", help="Number of headstones to display."),
    clear: bool = typer.Option(False, "--clear", help="Purge all digital headstones."),
) -> None:
    """⚰  Inspect the digital headstones of slain processes."""
    graveyard = Graveyard()
    if clear:
        cleared = graveyard.clear()
        console.print(f"[bold #00ff9d]Purged {cleared} headstones from the graveyard.[/bold #00ff9d]")
    else:
        graveyard.render(console, limit=limit)


@app.command("exorcise")
def exorcise_cmd() -> None:
    """✦  Temporarily purge the spirit and cleanse the terminal."""
    from haunted_sh.display import render_exorcism_ceremony
    render_exorcism_ceremony()


@app.command("info")
def info_cmd(
    model: str = typer.Option(DEFAULT_MODEL, "-m", "--model"),
    ollama_host: str = typer.Option(DEFAULT_OLLAMA_HOST, "--ollama-host"),
    offline: bool = typer.Option(DEFAULT_OFFLINE_ONLY, "--offline"),
) -> None:
    """Inspect local open-weight AI connection and offline engine diagnostics."""
    ghost = GhostAI(model_name=model, ollama_host=ollama_host, offline_only=offline)
    backend_name, backend_desc = ghost.get_backend_status()

    console.print()
    console.print("[bold #a855f7]👻 HAUNTED-SH SYSTEM DIAGNOSTICS[/bold #a855f7]")
    console.print(f" • [bold #00ff9d]Target Model:[/bold #00ff9d] {ghost.model_name}")
    console.print(f" • [bold #38bdf8]Backend Engine:[/bold #38bdf8] {backend_name}")
    console.print(f" • [dim #94a3b8]Diagnostic Details:[/dim #94a3b8] {backend_desc}")
    console.print(f" • [bold #f43f5e]Ollama Reachable:[/bold #f43f5e] {ghost.check_ollama()}")
    console.print(f" • [bold #a855f7]Default Haunt Chance:[/bold #a855f7] {int(ghost.haunt_frequency * 100)}%")
    console.print()


if __name__ == "__main__":
    app()
