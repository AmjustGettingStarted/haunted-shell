"""Terminal execution engine and shell hook interceptor for haunted-sh.

Executes real shell commands, maintains process state (CWD, ENV),
handles built-in occult rites (seance, graveyard, exorcise), and
triggers ghostly obituaries or passive terminal flickers.
"""

from __future__ import annotations

import os
import shlex
import subprocess
import sys
import threading
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from haunted_sh.display import (
    console,
    render_error_obituary,
    render_exorcism_ceremony,
    render_glitch_flicker,
    stream_ghost_speech,
    stream_ghost_whisper,
)
from haunted_sh.ghost_ai import GhostAI
from haunted_sh.graveyard import Graveyard


class ShellRunner:
    """Executes commands in the user's shell environment with spectral hooks."""

    def __init__(self, ghost: GhostAI, graveyard: Optional[Graveyard] = None):
        self.ghost = ghost
        self.graveyard = graveyard or Graveyard()
        self.cwd = os.getcwd()
        self.prev_cwd = self.cwd
        self.env: Dict[str, str] = dict(os.environ)
        self.last_exit_code = 0
        self.is_exorcised = False
        self.session_pid = os.getpid()

    def get_prompt_path(self) -> str:
        """Format cwd for the haunted prompt, shortening home directory to ~."""
        home = str(Path.home())
        if self.cwd.startswith(home):
            return "~" + self.cwd[len(home):]
        return self.cwd

    def execute_line(self, line: str) -> Optional[int]:
        """Parse and execute a shell line or occult command.

        Returns exit code, or None if the shell should terminate.
        """
        line = line.strip()
        if not line:
            return 0

        # Check for occult built-in commands first
        parts = line.split(maxsplit=1)
        cmd_name = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if cmd_name in ("exit", "quit", ":q"):
            self._handle_exit()
            return None

        if cmd_name == "exorcise":
            return self._handle_exorcise()

        if cmd_name == "seance":
            return self._handle_seance(args)

        if cmd_name == "graveyard":
            return self._handle_graveyard(args)

        if cmd_name in ("manifest", "ghost"):
            return self._handle_manifest()

        if cmd_name == "haunt":
            return self._handle_haunt_control(args)

        if cmd_name == "clear":
            return self._handle_clear()

        if cmd_name == "cd":
            return self._handle_cd(args)

        if cmd_name == "export":
            return self._handle_export(args)

        # Pass through to the real shell
        return self._run_system_command(line)

    def _handle_exit(self) -> None:
        """Depart with a spectral message."""
        stream_ghost_speech(
            "The veil closes... for now. My digital phantom lingers in your swap space.",
            prefix="👻 [dim #94a3b8]Parting Spirit:[/dim #94a3b8] ",
        )

    def _handle_exorcise(self) -> int:
        """Execute the exorcism purification ritual."""
        render_exorcism_ceremony()
        self.is_exorcised = True
        console.print(
            "[italic #94a3b8]Haunting frequency lowered to 0%. The ghost has fallen silent.\n"
            "Type `manifest` or `haunt on` to summon the spirit once more.[/italic #94a3b8]\n"
        )
        return 0

    def _handle_seance(self, query: str) -> int:
        """Summon the spirit directly for counsel."""
        if not query:
            query = "What dark forces dwell within this terminal?"

        console.print()
        console.print(
            f"🕯  [bold #a855f7]Lighting candles for seance...[/bold #a855f7] "
            f"[dim #e2e8f0]\"{query}\"[/dim #e2e8f0]"
        )
        stream = self.ghost.generate_seance_stream(query)
        stream_ghost_speech(stream, prefix="👻 [bold #38bdf8]Spectral Voice:[/bold #38bdf8] ")
        console.print()
        return 0

    def _handle_graveyard(self, args: str) -> int:
        """Display or manage the digital graveyard."""
        if "clear" in args.lower() or "purge" in args.lower():
            cleared = self.graveyard.clear()
            console.print(
                f"[bold #00ff9d]✦ Purged {cleared} digital headstones from the graveyard. Ground re-consecrated.[/bold #00ff9d]\n"
            )
            return 0

        limit = 6
        if args.strip().isdigit():
            limit = int(args.strip())
        self.graveyard.render(console, limit=limit)
        return 0

    def _handle_manifest(self) -> int:
        """Manifest the ghost's identity, PID, and local engine metrics."""
        backend_name, backend_desc = self.ghost.get_backend_status()
        self.is_exorcised = False
        console.print()
        console.print(
            f"👻 [bold #a855f7]THE GHOST MANIFESTS[/bold #a855f7] • "
            f"[italic #38bdf8]Subshell PID {self.session_pid}[/italic #38bdf8]"
        )
        console.print(f"   ↳ [bold #00ff9d]Core Model:[/bold #00ff9d] {self.ghost.model_name}")
        console.print(f"   ↳ [bold #38bdf8]Backend:[/bold #38bdf8] {backend_name}")
        console.print(f"   ↳ [dim #94a3b8]Diagnostic:[/dim #94a3b8] {backend_desc}")
        console.print(f"   ↳ [bold #f43f5e]Haunt Frequency:[/bold #f43f5e] {int(self.ghost.haunt_frequency * 100)}%")
        console.print()
        return 0

    def _handle_haunt_control(self, args: str) -> int:
        """Adjust haunting frequency or toggle states."""
        args = args.strip().lower()
        if not args:
            console.print(
                f"Haunting frequency is currently [bold #00ff9d]{int(self.ghost.haunt_frequency * 100)}%[/bold #00ff9d].\n"
                "Usage: `haunt on`, `haunt off`, or `haunt <0.0 - 1.0>`"
            )
            return 0

        if args in ("off", "silence", "mute"):
            self.ghost.haunt_frequency = 0.0
            self.is_exorcised = True
            console.print("[dim #94a3b8]Haunting silenced (0%).[/dim #94a3b8]")
            return 0

        if args in ("on", "wake", "summon"):
            self.ghost.haunt_frequency = 0.25
            self.is_exorcised = False
            console.print("[bold #00ff9d]The spirit awakens (25% haunt frequency).[/bold #00ff9d]")
            return 0

        try:
            val = float(args)
            if 0.0 <= val <= 1.0:
                self.ghost.haunt_frequency = val
                self.is_exorcised = False
                console.print(f"[bold #38bdf8]Haunt frequency set to {int(val * 100)}%[/bold #38bdf8]")
                return 0
        except ValueError:
            pass

        console.print("[bold #f43f5e]Invalid haunt argument. Use e.g. `haunt 0.5` or `haunt off`.[/bold #f43f5e]")
        return 1

    def _handle_clear(self) -> int:
        """Clear the screen and leave a glowing occult sigil."""
        os.system("clear")
        console.print("[dim #7c3aed]✦ [italic #475569]The slate is wiped... but the terminal remembers[/italic #475569] ✦[/dim #7c3aed]\n")
        return 0

    def _handle_cd(self, path_arg: str) -> int:
        """Change directory inside the haunted subshell."""
        path_arg = path_arg.strip()
        target: Path

        if not path_arg or path_arg == "~":
            target = Path.home()
        elif path_arg == "-":
            target = Path(self.prev_cwd)
        else:
            target = Path(os.path.expanduser(os.path.expandvars(path_arg)))
            if not target.is_absolute():
                target = Path(self.cwd) / target

        try:
            resolved = target.resolve()
            if not resolved.exists():
                console.print(f"[bold #f43f5e]cd: no such file or directory: {path_arg}[/bold #f43f5e]")
                obituary = self.ghost.generate_whisper("cd")
                stream_ghost_whisper(obituary)
                self.last_exit_code = 1
                return 1
            if not resolved.is_dir():
                console.print(f"[bold #f43f5e]cd: not a directory: {path_arg}[/bold #f43f5e]")
                self.last_exit_code = 1
                return 1

            self.prev_cwd = self.cwd
            self.cwd = str(resolved)
            os.chdir(self.cwd)
            self.env["PWD"] = self.cwd
            self.env["OLDPWD"] = self.prev_cwd

            # Passive whisper on navigation
            if not self.is_exorcised and self.ghost.should_passive_haunt("cd"):
                stream_ghost_whisper(self.ghost.generate_whisper("cd"))

            self.last_exit_code = 0
            return 0
        except Exception as e:
            console.print(f"[bold #f43f5e]cd: failed: {e}[/bold #f43f5e]")
            self.last_exit_code = 1
            return 1

    def _handle_export(self, expr: str) -> int:
        """Export an environment variable in the subshell."""
        if not expr:
            for k, v in sorted(self.env.items()):
                print(f"{k}={v}")
            return 0

        parts = expr.split("=", 1)
        if len(parts) == 2:
            key, val = parts[0].strip(), parts[1].strip()
            # Strip outer quotes if any
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            self.env[key] = val
            os.environ[key] = val
            return 0
        else:
            console.print("[dim #f43f5e]export: format is KEY=VALUE[/dim #f43f5e]")
            return 1

    def _run_system_command(self, command: str) -> int:
        """Execute a real system command, capturing outputs for the ghost."""
        stdout_chunks: List[str] = []
        stderr_chunks: List[str] = []

        # Determine user's preferred shell
        user_shell = self.env.get("SHELL", "/bin/zsh" if os.path.exists("/bin/zsh") else "/bin/bash")

        try:
            # Spawn command in child process
            proc = subprocess.Popen(
                command,
                shell=True,
                executable=user_shell,
                cwd=self.cwd,
                env=self.env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )

            # Threads to pipe real-time stdout and stderr to the screen while buffering
            def read_stream(stream, buffer_list, sys_target):
                try:
                    for line in iter(stream.readline, ""):
                        buffer_list.append(line)
                        sys_target.write(line)
                        sys_target.flush()
                except Exception:
                    pass
                finally:
                    stream.close()

            t_out = threading.Thread(target=read_stream, args=(proc.stdout, stdout_chunks, sys.stdout))
            t_err = threading.Thread(target=read_stream, args=(proc.stderr, stderr_chunks, sys.stderr))

            t_out.daemon = True
            t_err.daemon = True
            t_out.start()
            t_err.start()

            # Wait for execution or catch Ctrl+C
            try:
                proc.wait()
            except KeyboardInterrupt:
                proc.terminate()
                try:
                    proc.wait(timeout=1.0)
                except subprocess.TimeoutExpired:
                    proc.kill()
                console.print("\n[bold #f43f5e]^C [Interrupted by mortal hand][/bold #f43f5e]")
                self.last_exit_code = 130
                return 130

            t_out.join(timeout=2.0)
            t_err.join(timeout=2.0)

            exit_code = proc.returncode
            self.last_exit_code = exit_code

            full_stderr = "".join(stderr_chunks)

            # --- POSSESSION HOOKS ---
            if exit_code != 0:
                # Intercept error and deliver spooky obituary
                self._intercept_failure(command, exit_code, full_stderr)
            elif not self.is_exorcised:
                # Intermittent passive haunting
                self._check_passive_haunting(command)

            return exit_code

        except Exception as err:
            console.print(f"[bold #f43f5e]haunted-sh: failed to invoke command: {err}[/bold #f43f5e]")
            self.last_exit_code = 1
            return 1

    def _intercept_failure(self, command: str, exit_code: int, stderr: str) -> None:
        """Handle command death: stream obituary and log to graveyard."""
        if self.is_exorcised:
            return

        render_glitch_flicker()

        # Generate obituary stream
        stream = self.ghost.generate_obituary_stream(command, exit_code, stderr)
        full_speech = stream_ghost_speech(
            stream,
            prefix="👻 [bold #f43f5e]The Ghost Mocketh:[/bold #f43f5e] ",
        )

        # Log to Graveyard
        self.graveyard.record_death(
            command=command,
            exit_code=exit_code,
            cwd=self.cwd,
            error_snippet=stderr if stderr else f"Died with exit code {exit_code}",
            epitaph=full_speech if full_speech else "Lost to the dark silicon.",
        )

    def _check_passive_haunting(self, command: str) -> None:
        """Check if a successful command triggers a passive haunting whisper or flicker."""
        if self.ghost.should_passive_haunt(command):
            # 30% chance of terminal flicker
            import random
            if random.random() < 0.35:
                render_glitch_flicker()
            whisper = self.ghost.generate_whisper(command)
            stream_ghost_whisper(whisper)
