from src.first_follow import compute_first, compute_follow
from src.grammar import Grammar


def test_follow_simple():
    grammar_text = """
    S -> a A
    A -> c | ε
    """
    grammar = Grammar.from_string(grammar_text)
    first_sets = compute_first(grammar)
    follow_sets = compute_follow(grammar, first_sets)

    assert "$" in follow_sets["S"]
    assert "$" in follow_sets["A"]