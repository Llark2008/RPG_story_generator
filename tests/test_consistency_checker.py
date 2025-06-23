import sys
from pathlib import Path

# Make core package importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "core"))

from rpggen import ConsistencyChecker
from langchain_community.llms import FakeListLLM
from langchain_community.embeddings import FakeEmbeddings


def test_score_and_check():
    docs = ["Alice loves Bob", "Bob hates Charlie"]
    llm = FakeListLLM(responses=["0.9", "Score: 0.4"])
    embeddings = FakeEmbeddings(size=3)
    checker = ConsistencyChecker(llm=llm, embeddings=embeddings, score_threshold=0.5)
    checker.build_index(docs)

    assert checker.check("Is Alice mentioned?") is True
    score = checker.score("Is Bob friendly to Charlie?")
    assert score == 0.4
