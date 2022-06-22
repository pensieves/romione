from romione.graph.parse_utils import impute_diff_args


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