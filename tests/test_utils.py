import sys
from pathlib import Path

# Ensure core package is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "core"))

from rpggen.utils.text import slugify, chinese_length
from rpggen.utils.id import hash_id
from rpggen.utils.log import get_logger


def test_slugify_and_chinese_length():
    assert slugify("Hello, World!") == "hello-world"
    assert chinese_length("你好世界") == 4


def test_hash_id_deterministic():
    a = hash_id("test text")
    b = hash_id("test text")
    assert a == b
    assert len(a) == 10


def test_get_logger(tmp_path):
    log_file = tmp_path / "out.log"
    logger = get_logger("test", log_file=log_file)
    logger.info("hello")
    assert log_file.exists()
    assert "hello" in log_file.read_text()
