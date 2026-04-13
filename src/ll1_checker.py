from __future__ import annotations

from typing import Dict, List


def is_ll1(
    parsing_table: Dict[str, Dict[str, List[List[str]]]]
) -> bool:
    for _, row in parsing_table.items():
        for _, productions in row.items():
            if len(productions) > 1:
                return False
    return True