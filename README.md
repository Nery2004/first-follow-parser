# First, Follow y Tabla de Análisis Sintáctico Predictivo

## Descripción
Este proyecto implementa el cálculo de los conjuntos FIRST y FOLLOW para gramáticas libres de contexto, así como la construcción automática de la tabla de análisis sintáctico predictivo.

Además, el programa determina si una gramática es LL(1), reportando conflictos en la tabla cuando existan.

## Estructura del proyecto

```bash
first-follow-parser/
├── README.md
├── requirements.txt
├── .gitignore
├── main.py
├── examples/
│   ├── grammar_expr.txt
│   ├── grammar_simple.txt
│   └── grammar_if_else.txt
├── src/
│   ├── __init__.py
│   ├── grammar.py
│   ├── first_follow.py
│   ├── parsing_table.py
│   ├── ll1_checker.py
│   └── utils.py
└── tests/
    ├── test_first.py
    ├── test_follow.py
    └── test_parsing_table.py
