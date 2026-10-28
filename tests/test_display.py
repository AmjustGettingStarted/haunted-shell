"""Tests for display aesthetics and glitch effects."""

from haunted_sh.display import corrupt_text, get_banner_art, stream_ghost_speech


def test_corrupt_text():
    clean = "The machine is possessed"
    glitched = corrupt_text(clean, intensity=0.5)
    assert glitched != clean
    assert len(glitched) >= len(clean)

    # 0 intensity returns unmodified
    assert corrupt_text(clean, intensity=0.0) == clean


def test_banner_art():
    banner = get_banner_art()
    assert "HAUNTED" in banner or "██╗" in banner


def test_stream_ghost_speech():
    result = stream_ghost_speech("Whispers from the phosphor.", typing_delay=0.0001)
    assert result == "Whispers from the phosphor."
