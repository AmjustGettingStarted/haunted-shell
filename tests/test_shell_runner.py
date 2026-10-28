"""Tests for shell_runner execution and command hooking."""

import os
from pathlib import Path
from haunted_sh.ghost_ai import GhostAI
from haunted_sh.graveyard import Graveyard
from haunted_sh.shell_runner import ShellRunner


def test_runner_cd_and_pwd(tmp_path: Path):
    ghost = GhostAI(offline_only=True)
    gy = Graveyard(filepath=tmp_path / "gy.json")
    runner = ShellRunner(ghost=ghost, graveyard=gy)

    initial_cwd = runner.cwd
    sub_dir = tmp_path / "crypt"
    sub_dir.mkdir()

    # Successful cd
    code = runner.execute_line(f"cd {sub_dir}")
    assert code == 0
    assert runner.cwd == str(sub_dir)

    # cd -
    code = runner.execute_line("cd -")
    assert code == 0
    assert runner.cwd == initial_cwd

    # Failed cd
    code = runner.execute_line("cd /definitely_not_a_real_directory_9999")
    assert code == 1


def test_runner_export(tmp_path: Path):
    ghost = GhostAI(offline_only=True)
    gy = Graveyard(filepath=tmp_path / "gy.json")
    runner = ShellRunner(ghost=ghost, graveyard=gy)

    code = runner.execute_line("export PHANTOM_VAR=spooky_value")
    assert code == 0
    assert runner.env["PHANTOM_VAR"] == "spooky_value"


def test_runner_occult_commands(tmp_path: Path):
    ghost = GhostAI(offline_only=True)
    gy = Graveyard(filepath=tmp_path / "gy.json")
    runner = ShellRunner(ghost=ghost, graveyard=gy)

    # Manifest
    code = runner.execute_line("manifest")
    assert code == 0

    # Haunt control
    code = runner.execute_line("haunt off")
    assert code == 0
    assert runner.ghost.haunt_frequency == 0.0

    code = runner.execute_line("haunt 0.75")
    assert code == 0
    assert runner.ghost.haunt_frequency == 0.75

    # Exorcise
    code = runner.execute_line("exorcise")
    assert code == 0
    assert runner.is_exorcised is True

    # Seance
    code = runner.execute_line("seance 'Are we alone in memory?'")
    assert code == 0


def test_runner_command_execution(tmp_path: Path):
    ghost = GhostAI(offline_only=True)
    gy = Graveyard(filepath=tmp_path / "gy.json")
    runner = ShellRunner(ghost=ghost, graveyard=gy)

    # Successful system command
    code = runner.execute_line("echo 'test phantom'")
    assert code == 0

    # Failing system command
    code = runner.execute_line("sh -c 'exit 42'")
    assert code == 42
    # Verify logged to graveyard
    assert len(gy.get_entries()) == 1
    assert gy.get_entries()[0].exit_code == 42

