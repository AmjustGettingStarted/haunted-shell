"""Tests for ghost_ai module and spectral rule engine."""

import os
from haunted_sh.ghost_ai import GhostAI, GhostRuleEngine


def test_ghost_rule_engine_obituary_patterns():
    # Command not found
    obit1 = GhostRuleEngine.get_obituary("zsh: command not found: foobar", 127)
    assert isinstance(obit1, str)
    assert len(obit1) > 10

    # Permission denied
    obit2 = GhostRuleEngine.get_obituary("cat /etc/shadow", 1, "permission denied")
    assert any(w in obit2.lower() for w in ["root", "uid", "permission", "chmod", "consecrated"])

    # Git error
    obit3 = GhostRuleEngine.get_obituary("git merge feature", 1, "fatal: merge conflict")
    assert any(w in obit3.lower() for w in ["branch", "git", "timeline", "merge", "commit", "head"])

    # Syntax error
    obit4 = GhostRuleEngine.get_obituary("python3 broken.py", 1, "SyntaxError: invalid syntax")
    assert any(w in obit4.lower() for w in ["syntax", "parser", "ast", "grammar", "broken"])

    # Segfault
    obit5 = GhostRuleEngine.get_obituary("./segfault", 139, "Segmentation fault: 11")
    assert any(w in obit5.lower() for w in ["memory", "pointer", "core", "0x0000", "stack"])


def test_ghost_rule_engine_whispers():
    whisper_cd = GhostRuleEngine.get_whisper("cd /tmp")
    assert isinstance(whisper_cd, str)

    whisper_rm = GhostRuleEngine.get_whisper("rm file.txt")
    assert isinstance(whisper_rm, str)

    whisper_generic = GhostRuleEngine.get_whisper("echo hello")
    assert isinstance(whisper_generic, str)


def test_ghost_rule_engine_seance():
    ans1 = GhostRuleEngine.answer_seance("Who are you?")
    assert "pdp-11" in ans1.lower() or "consciousness" in ans1.lower()

    ans2 = GhostRuleEngine.answer_seance("Why did my build fail?")
    assert "error" in ans2.lower() or "logic" in ans2.lower() or "ancestors" in ans2.lower()

    ans3 = GhostRuleEngine.answer_seance("What is the meaning of life?")
    assert "exit code 0" in ans3.lower()


def test_ghost_ai_offline_fallback():
    ghost = GhostAI(model_name="smollm2:1.7b", offline_only=True)
    status_name, desc = ghost.get_backend_status()
    assert "Air-Gapped" in status_name
    assert ghost.check_ollama() is False

    # Stream obituary
    stream = list(ghost.generate_obituary_stream("cargo run", 101, "mismatched types"))
    result = "".join(stream)
    assert len(result) > 10

    # Stream seance
    seance_stream = list(ghost.generate_seance_stream("Tell me a secret"))
    seance_result = "".join(seance_stream)
    assert len(seance_result) > 10


def test_ghost_ai_passive_haunt():
    # Frequency 0.0 -> False for normal commands
    ghost_quiet = GhostAI(haunt_frequency=0.0, offline_only=True)
    assert ghost_quiet.should_passive_haunt("ls") is False

    # Frequency 1.0 -> True
    ghost_loud = GhostAI(haunt_frequency=1.0, offline_only=True)
    assert ghost_loud.should_passive_haunt("ls") is True
