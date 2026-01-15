"""
DaskExpression class (var name, raw expr, value, tree)
"""
from dask_core.parser import ExpressionParser
from dask_core.parse_tree import ParseTree
from dask_core.evaluator import Evaluator
class DaskExpression:
    def __init__(self, var_name: str, expr: str):
        self.name = var_name
        self.expression = expr
        self.parse_tree: ParseTree = self.build_tree()
        self.value = None

    def build_tree(self, parser = ExpressionParser()):
        self.parse_tree = parser.parse(self.expression)
        return self.parse_tree

    def evaluate(self, evaluator: Evaluator = None, context: dict | None = None):
        if self.parse_tree is None:
            return None
        if context is None:
            return None
        if evaluator is None:
            evaluator = Evaluator()
        return self.parse_tree.evaluate(evaluator, context)
    