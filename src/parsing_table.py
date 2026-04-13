from __future__ import annotations

from typing import Dict, List, Set, Tuple

from src.first_follow import first_of_sequence
from src.grammar import EPSILON, ENDMARKER, Grammar


def build_parsing_table(
    grammar: Grammar,
    first_sets: Dict[str, Set[str]],
    follow_sets: Dict[str, Set[str]],
) -> Tuple[Dict[str, Dict[str, List[List[str]]]], List[str]]:
    table: Dict[str, Dict[str, List[List[str]]]] = {
        nt: {} for nt in grammar.non_terminals
    }
    conflicts: List[str] = []

    merged_first = {}
    for t in grammar.terminals:
        merged_first[t] = {t}
    for nt, values in first_sets.items():
        merged_first[nt] = values
    merged_first[EPSILON] = {EPSILON}

    for left, productions in grammar.productions.items():
        for production in productions:
            prod_first = first_of_sequence(production, merged_first, grammar)

            # Para cada terminal en FIRST(alpha)
            for terminal in (prod_first - {EPSILON}):
                if terminal not in table[left]:
                    table[left][terminal] = []
                table[left][terminal].append(production)

                if len(table[left][terminal]) > 1:
                    conflicts.append(
                        f"Conflicto en M[{left}, {terminal}] con producciones: "
                        + " | ".join(" ".join(p) for p in table[left][terminal])
                    )

            # Si ε está en FIRST(alpha), usar FOLLOW(A)
            if EPSILON in prod_first:
                for terminal in follow_sets[left]:
                    if terminal not in table[left]:
                        table[left][terminal] = []
                    table[left][terminal].append(production)

                    if len(table[left][terminal]) > 1:
                        conflicts.append(
                            f"Conflicto en M[{left}, {terminal}] con producciones: "
                            + " | ".join(" ".join(p) for p in table[left][terminal])
                        )

    return table, conflicts


def get_table_terminals(grammar: Grammar) -> List[str]:
    ordered = sorted(grammar.terminals)
    if ENDMARKER not in ordered:
        ordered.append(ENDMARKER)
    return ordered