from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Set

EPSILON = "ε"
ENDMARKER = "$"


@dataclass
class Grammar:
    start_symbol: str
    productions: Dict[str, List[List[str]]] = field(default_factory=dict)
    non_terminals: Set[str] = field(default_factory=set)
    terminals: Set[str] = field(default_factory=set)

    @staticmethod
    def from_string(grammar_text: str) -> "Grammar":
        lines = [
            line.strip()
            for line in grammar_text.strip().splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]

        productions: Dict[str, List[List[str]]] = {}
        non_terminals: Set[str] = set()
        start_symbol = None

        # Primera pasada: detectar no terminales
        for line in lines:
            if "->" not in line:
                raise ValueError(f"Línea inválida: {line}")
            left, _ = line.split("->", 1)
            left = left.strip()
            non_terminals.add(left)
            if start_symbol is None:
                start_symbol = left

        # Segunda pasada: procesar producciones
        for line in lines:
            left, right = line.split("->", 1)
            left = left.strip()
            alternatives = [alt.strip() for alt in right.split("|")]

            if left not in productions:
                productions[left] = []

            for alt in alternatives:
                if alt == EPSILON:
                    productions[left].append([EPSILON])
                else:
                    symbols = alt.split()
                    productions[left].append(symbols)

        # Detectar terminales
        terminals: Set[str] = set()
        for _, rhs_list in productions.items():
            for rhs in rhs_list:
                for symbol in rhs:
                    if symbol != EPSILON and symbol not in non_terminals:
                        terminals.add(symbol)

        return Grammar(
            start_symbol=start_symbol,
            productions=productions,
            non_terminals=non_terminals,
            terminals=terminals,
        )

    @staticmethod
    def from_file(path: str) -> "Grammar":
        with open(path, "r", encoding="utf-8") as f:
            return Grammar.from_string(f.read())

    def __str__(self) -> str:
        lines = []
        for non_terminal, rhs_list in self.productions.items():
            joined = " | ".join(" ".join(rhs) for rhs in rhs_list)
            lines.append(f"{non_terminal} -> {joined}")
        return "\n".join(lines)