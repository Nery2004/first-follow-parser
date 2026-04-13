from src.first_follow import compute_first
from src.grammar import Grammar


def test_first_simple():
    grammar_text = """
    S -> a A | b
    A -> c | ε
    """
    grammar = Grammar.from_string(grammar_text)
    first_sets = compute_first(grammar)

    assert first_sets["S"] == {"a", "b"}
    assert first_sets["A"] == {"c", "ε"}