import sys
from pathlib import Path

# Ensure core package is importable during tests
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "core"))

from rpggen import main

def test_main_output(capsys):
    main()
    captured = capsys.readouterr()
    assert "placeholder" in captured.out
