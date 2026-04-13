from __future__ import annotations

from typing import Dict, List, Set

from tabulate import tabulate

from src.grammar import EPSILON, Grammar


def format_set(name: str, values: Set[str]) -> str:
    ordered = sorted(values)
    return f"{name} = {{ " + ", ".join(ordered) + " }}"


def print_first_sets(first_sets: Dict[str, Set[str]]) -> None:
    print("\nFIRST:")
    for non_terminal in sorted(first_sets.keys()):
        print(format_set(f"FIRST({non_terminal})", first_sets[non_terminal]))


def print_follow_sets(follow_sets: Dict[str, Set[str]]) -> None:
    print("\nFOLLOW:")
    for non_terminal in sorted(follow_sets.keys()):
        print(format_set(f"FOLLOW({non_terminal})", follow_sets[non_terminal]))


def print_parsing_table(
    grammar: Grammar,
    parsing_table: Dict[str, Dict[str, List[List[str]]]],
    terminals: List[str],
) -> None:
    headers = ["NT/T"] + terminals
    rows = []

    for non_terminal in sorted(grammar.non_terminals):
        row = [non_terminal]
        for terminal in terminals:
            productions = parsing_table.get(non_terminal, {}).get(terminal, [])
            if not productions:
                row.append("")
            else:
                text = " | ".join(
                    f"{non_terminal} -> {' '.join(prod)}" for prod in productions
                )
                row.append(text)
        rows.append(row)

    print("\nTabla de análisis sintáctico predictivo:")
    print(tabulate(rows, headers=headers, tablefmt="grid"))