import re
import sympy as sp
from sympy.vector import CoordSys3D
from sympy.parsing.sympy_parser import parse_expr


def impute_diff_args(expr):
    r"""Impute args into the function for correct diff parsing by sympy.
    e.g. x.diff(t)+y.diff(a,11,t,2) to x(t).diff(t)+y(a,t).diff(a,11,t,2)"""
    look_behind = r"(?<=diff\()" # check if preceded by diff(
    args_chars = r"[^\)]*" # any char but the closing bracket for diff
    look_ahead = r"(?=\))" # clossing bracket for diff(
    args_pattern = re.compile(f"{look_behind}{args_chars}{look_ahead}")
    args = re.findall(args_pattern, expr)

    # func to remove order of differentiation
    order_pattern = re.compile(r",\d+")
    remove_diff_order = lambda arg: re.sub(order_pattern, "", arg)
    
    if args:
        # replace func pops the args list from left 
        # and wraps it in parentheses before .diff
        repl_fn = lambda match_obj: f"({remove_diff_order(args.pop(0))}).diff"
        expr = re.sub(".diff", repl_fn, expr)

    return expr


def process_and_parse_expr(expr):
    expr = impute_diff_args(expr)
    expr = parse_expr(expr)
    return expr


def parse_vector(value, coord_sys=CoordSys3D("N")):
    if isinstance(value, (str, int, float)):
        value = parse_expr(str(value))

        # create a mapping e.g. sp.Symbol("i") -> coord_sys.i
        vec_map = {
            sp.Symbol(vec._name.split(".")[1]): vec for vec in coord_sys._base_vectors
        }

        components = sp.collect(value, vec_map.keys(), evaluate=False)

        if set.intersection(set(vec_map.keys()), set(components.keys())):
            value = 0 * coord_sys._base_vectors[0]
            for k, v in components.items():
                value += v * vec_map.get(k, k)

    return value
