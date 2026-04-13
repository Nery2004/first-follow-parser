from __future__ import annotations

import os

from src.first_follow import compute_first, compute_follow
from src.grammar import Grammar
from src.ll1_checker import is_ll1
from src.parsing_table import build_parsing_table, get_table_terminals
from src.utils import print_first_sets, print_follow_sets, print_parsing_table


def run_grammar(path: str) -> None:
    print(f"Archivo: {path}")

    grammar = Grammar.from_file(path)

    print("\nGramática ingresada:")
    print(grammar)

    first_sets = compute_first(grammar)
    follow_sets = compute_follow(grammar, first_sets)

    print_first_sets(first_sets)
    print_follow_sets(follow_sets)

    parsing_table, conflicts = build_parsing_table(grammar, first_sets, follow_sets)
    terminals = get_table_terminals(grammar)

    print_parsing_table(grammar, parsing_table, terminals)

    ll1 = is_ll1(parsing_table)
    print("\n¿Es LL(1)?", "Sí" if ll1 else "No")

    if conflicts:
        print("\nConflictos encontrados:")
        for conflict in conflicts:
            print("-", conflict)
    else:
        print("\nNo se encontraron conflictos en la tabla.")


def main() -> None:
    examples_dir = "examples"
    grammar_files = [
        os.path.join(examples_dir, "grammar_expr.txt"),
        os.path.join(examples_dir, "grammar_simple.txt"),
        os.path.join(examples_dir, "grammar_if_else.txt"),
    ]

    for path in grammar_files:
        run_grammar(path)
        print("\n")


if __name__ == "__main__":
    main()