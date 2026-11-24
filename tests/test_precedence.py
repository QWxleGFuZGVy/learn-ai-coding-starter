from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Binary, ExprStmt, Literal
from sloperator.runner import run_source


def only_expression(source: str):
    (statement,) = parse(tokenize(source))
    assert isinstance(statement, ExprStmt)
    return statement.expression


def test_multiplication_binds_tighter_than_addition():
    # 2 + 3 * 4 must parse as 2 + (3 * 4), not (2 + 3) * 4.
    expr = only_expression("2 + 3 * 4✨")
    assert isinstance(expr, Binary) and expr.operator.type is TokenType.PLUS
    assert isinstance(expr.left, Literal) and expr.left.value == 2
    assert isinstance(expr.right, Binary) and expr.right.operator.type is TokenType.STAR
    assert isinstance(expr.right.left, Literal) and expr.right.left.value == 3
    assert isinstance(expr.right.right, Literal) and expr.right.right.value == 4


def test_multiplication_runs_before_addition():
    result = run_source("hallucinate(2 + 3 * 4)✨")
    assert result.stderr == "", result.stderr
    assert result.stdout == "14\n"
