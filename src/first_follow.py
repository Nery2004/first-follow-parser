from __future__ import annotations

from typing import Dict, List, Set

from src.grammar import EPSILON, ENDMARKER, Grammar


def compute_first(grammar: Grammar) -> Dict[str, Set[str]]:
    first: Dict[str, Set[str]] = {}

    # Inicializar FIRST de terminales
    for terminal in grammar.terminals:
        first[terminal] = {terminal}

    # Inicializar FIRST de no terminales
    for non_terminal in grammar.non_terminals:
        first[non_terminal] = set()

    first[EPSILON] = {EPSILON}

    changed = True
    while changed:
        changed = False

        for non_terminal, productions in grammar.productions.items():
            for production in productions:
                before = len(first[non_terminal])
                production_first = first_of_sequence(production, first, grammar)
                first[non_terminal].update(production_first)
                after = len(first[non_terminal])

                if after > before:
                    changed = True

    return {k: v for k, v in first.items() if k in grammar.non_terminals}


def first_of_sequence(
    symbols: List[str],
    first_sets: Dict[str, Set[str]],
    grammar: Grammar,
) -> Set[str]:
    if not symbols:
        return {EPSILON}

    result: Set[str] = set()

    if symbols == [EPSILON]:
        return {EPSILON}

    all_can_derive_epsilon = True

    for symbol in symbols:
        if symbol == EPSILON:
            result.add(EPSILON)
            break

        symbol_first = set()

        if symbol in grammar.non_terminals:
            symbol_first = first_sets.get(symbol, set())
        else:
            symbol_first = {symbol}

        result.update(symbol_first - {EPSILON})

        if EPSILON not in symbol_first:
            all_can_derive_epsilon = False
            break

    if all_can_derive_epsilon:
        result.add(EPSILON)

    return result


def compute_follow(
    grammar: Grammar,
    first_sets: Dict[str, Set[str]],
) -> Dict[str, Set[str]]:
    follow: Dict[str, Set[str]] = {
        non_terminal: set() for non_terminal in grammar.non_terminals
    }

    # Regla: $ en FOLLOW del símbolo inicial
    follow[grammar.start_symbol].add(ENDMARKER)

    changed = True
    while changed:
        changed = False

        for left, productions in grammar.productions.items():
            for production in productions:
                for i, symbol in enumerate(production):
                    if symbol not in grammar.non_terminals:
                        continue

                    beta = production[i + 1 :]
                    first_beta = first_of_sequence(beta, _merge_first_sets(first_sets, grammar), grammar)

                    before = len(follow[symbol])

                    # FIRST(beta) - {ε}
                    follow[symbol].update(first_beta - {EPSILON})

                    # Si beta => ε o beta vacío, agregar FOLLOW(left)
                    if not beta or EPSILON in first_beta:
                        follow[symbol].update(follow[left])

                    after = len(follow[symbol])
                    if after > before:
                        changed = True

    return follow


def _merge_first_sets(
    non_terminal_first: Dict[str, Set[str]],
    grammar: Grammar,
) -> Dict[str, Set[str]]:
    merged = {}

    for t in grammar.terminals:
        merged[t] = {t}

    for nt, values in non_terminal_first.items():
        merged[nt] = set(values)

    merged[EPSILON] = {EPSILON}
    return merged