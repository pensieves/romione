from sympy.parsing.sympy_parser import parse_expr
from romione.graph.heuristics import complexity


def test_complexity():
    test_cases = [
        ("a**2+a", "t", 0),
        ("a*t+1", "t", 1),
        ("a*t**3/2*(t**2+1)", "t", 3),
        ("sin(t)", "t", 1), 
        ("sin(t)+cos(t)", "t", 1),
        ("sin(t)*cos(t)", "t", 2),
        ("a*t+sin(t)*cos(t)", "t", 3),
        ("a*t+sin(t)*cos(t)", "t, a", 4),
        ("a*t**3+u*t**2+cos(t**2)*sin(t/(1+exp(t**3)))", "t,a", 7),
        ("a*t**3+u*t**2+cos(t**2)*sin(t/(1+exp(t**3)))", "t,a,u", 7),
    ]

    for expr, tgt_symbols, complexity_value in test_cases:
        expr = parse_expr(expr)
        tgt_symbols = [s.strip() for s in tgt_symbols.split(",")]
        assert complexity(expr, tgt_symbols) == complexity_value
