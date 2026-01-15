"""
DaskExpression class (var name, raw expr, value, tree)
"""
from dask_core.parser import ExpressionParser
from dask_core.evaluator import Evaluator
from dask_core.parse_tree import ParseTree
class DaskExpression:
    def __init__(self, var_name: str, expr: str):
        self.name = var_name
        self.expression = expr
        self.parse_tree: ParseTree | None = None
        self.value = None
        self.build_tree()
        self.parse_tree.evaluate

    def build_tree(self, parser = ExpressionParser()):
        self.parse_tree = parser.parse(self.expression)
    