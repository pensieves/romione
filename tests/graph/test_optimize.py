import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from romione.graph.optimize import maximize, minimize


def test_expr_allowed():
    test_cases = [
        {
            "expr": "u*t+a*t**2/2",
            "symbol": "t",
            "symbol_res": ["-u/a"],
            "expr_res": ["-u**2/(2*a)"],
            "maxima_conditions": ["a < 0"],
            "minima_conditions": ["a > 0"],
        },
        {
            "expr": "(v**2-u**2)/(2*a)",
            "symbol": "v",
            "symbol_res": ["0"],
            "expr_res": ["-u**2/(2*a)"],
            "maxima_conditions": ["1/a < 0"],
            "minima_conditions": ["1/a > 0"],
        },
    ]

    for test in test_cases:
        for fn in (maximize, minimize):
            symbol, points, expr_values, conditions = fn(test["expr"], test["symbol"])

            assert symbol.name == test["symbol"]
            assert points == [parse_expr(i) for i in test["symbol_res"]]
            assert expr_values == [parse_expr(i) for i in test["expr_res"]]

            test_conditions = (
                test["maxima_conditions"] if fn == maximize 
                else test["minima_conditions"]
            )
            assert conditions == [parse_expr(i) for i in test_conditions]


def test_expr_disallowed():
    test_cases = [
        {
            "expr": "u*t+a*t**2/2",
            "symbol": "t",
            "symbol_res": [],
            "expr_res": [],
            "maxima_conditions": [],
            "minima_conditions": [],
        },
        {
            "expr": "(v**2-u**2)/(2*a)",
            "symbol": "v",
            "symbol_res": [],
            "expr_res": [],
            "maxima_conditions": [],
            "minima_conditions": [],
        },
    ]

    for test in test_cases:
        for fn in (maximize, minimize):
            symbol, points, expr_values, conditions = fn(
                test["expr"], test["symbol"], allow_expr_return=False
            )

            assert symbol.name == test["symbol"]
            assert points == [parse_expr(i) for i in test["symbol_res"]]
            assert expr_values == [parse_expr(i) for i in test["expr_res"]]

            test_conditions = (
                test["maxima_conditions"] if fn == maximize 
                else test["minima_conditions"]
            )

            assert conditions == [parse_expr(i) for i in test_conditions]


def test_symbol_infer():
    test_cases = [
        {
            "expr": "3*t+(-1)*t**2/2",
            "symbol": "infer",
            "symbol_res": ["3"],
            "expr_res": ["9/2"],
            "maxima_conditions": [True],
            "minima_conditions": [],
        },
        {
            "expr": "(v**2-3**2)/(2*(-1))",
            "symbol": "infer",
            "symbol_res": ["0"],
            "expr_res": ["9/2"],
            "maxima_conditions": [True],
            "minima_conditions": [],
        },
    ]

    for test in test_cases:
        for fn in (maximize, minimize):
            for allow_expr_return in (True, False):
                symbol, points, expr_values, conditions = fn(
                    test["expr"], test["symbol"], allow_expr_return=allow_expr_return,
                )

                assert symbol == next(iter(parse_expr(test["expr"]).free_symbols))
                
                if fn == maximize:
                    assert points == [parse_expr(i) for i in test["symbol_res"]]
                    assert expr_values == [parse_expr(i) for i in test["expr_res"]]
                    assert conditions == test["maxima_conditions"]
                else:
                    assert points == []
                    assert expr_values == []
                    assert conditions == []