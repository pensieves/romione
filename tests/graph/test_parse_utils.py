from romione.graph.parse_utils import (
    process_and_parse_expr,
    impute_diff_args,
    fn_repl,
)


def test_diff_args_imputation():
    test_cases = [
        (
            "a + t + t**2",
            "a + t + t**2",
        ),
        (
            "x.diff(t)+y.diff(t)+z.diff(a)+w.diff(a,t)",
            "x(t).diff(t)+y(t).diff(t)+z(a).diff(a)+w(a,t).diff(a,t)",
        ),
        (
            "a + t + x.diff(t) + y.diff(a,11,t,2)",
            "a + t + x(t).diff(t) + y(a,t).diff(a,11,t,2)",
        ),
    ]

    for expr, imputed_expr in test_cases:
        assert imputed_expr == impute_diff_args(expr)


def test_function_replace():
    test_cases = [
        dict(expr="a", result="a"),
        dict(expr="a", repl_map=None, simplify=False, result="a"),
        dict(expr="x(t)", result="t"),
        dict(expr="x(t)", repl_map=dict(x="t**2"), result="t**2"),
        dict(expr="sin(t**2/(1+t**3))", result="t**2/(1+t**3)"),
        dict(expr="sin(t)*cos(t)", result="t**2"),
        dict(expr="sin(t)", repl_map=dict(sin="cos(t)"), result="cos(t)"),
        dict(expr="x.diff(t)", repl_map=dict(x="t**2"), result="2*t"),
        dict(expr="x.diff(a,1,t,2)", repl_map=dict(x="a**2*t**3"), result="12*a*t"),
        dict(
            expr="a+t+sin(t)+x.diff(t)",
            repl_map=dict(x="t**2", sin="log(t**2)"),
            result="a+3*t+log(t**2)",
        ),
    ]

    for test_case in test_cases:
        result = process_and_parse_expr(test_case.pop("result"))
        assert result == fn_repl(**test_case)
