"""Tests for the digital graveyard module."""

from pathlib import Path
from haunted_sh.display import console
from haunted_sh.graveyard import Graveyard


def test_graveyard_record_and_load(tmp_path: Path):
    grave_file = tmp_path / "test_graveyard.json"
    gy = Graveyard(filepath=grave_file)

    assert len(gy.get_entries()) == 0

    # Record deaths
    gy.record_death("git checkout non-existent", 1, "/repo", "error: pathspec not found", "A lost timeline.")
    gy.record_death("npm test", 2, "/repo", "npm ERR! Test failed.", "The test suite became a tomb.")

    assert len(gy.get_entries()) == 2
    entries = gy.get_entries()
    assert entries[0].command == "npm test"  # most recent first
    assert entries[0].exit_code == 2
    assert entries[1].command == "git checkout non-existent"

    # Reload from disk
    gy_reload = Graveyard(filepath=grave_file)
    assert len(gy_reload.get_entries()) == 2
    stats = gy_reload.get_stats()
    assert stats["total"] == 2
    assert "npm" in stats["most_lethal_command"] or "git" in stats["most_lethal_command"]

    # Clear
    cleared = gy_reload.clear()
    assert cleared == 2
    assert len(gy_reload.get_entries()) == 0


def test_graveyard_render(tmp_path: Path):
    grave_file = tmp_path / "test_render.json"
    gy = Graveyard(filepath=grave_file)
    gy.record_death("cargo build", 101, "/src", "unresolved import", "Compiler despair.")

    # Check rendering does not crash
    gy.render(console, limit=4)

