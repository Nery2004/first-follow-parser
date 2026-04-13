from src.first_follow import compute_first, compute_follow
from src.grammar import Grammar
from src.ll1_checker import is_ll1
from src.parsing_table import build_parsing_table


def test_parsing_table_ll1():
    grammar_text = """
    S -> a A | b
    A -> c | ε
    """
    grammar = Grammar.from_string(grammar_text)
    first_sets = compute_first(grammar)
    follow_sets = compute_follow(grammar, first_sets)
    table, conflicts = build_parsing_table(grammar, first_sets, follow_sets)

    assert is_ll1(table) is True
    assert conflicts == []