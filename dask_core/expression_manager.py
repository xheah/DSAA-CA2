"""
Manages all expressions (add, modify, lookup, sort)
"""
from dask_core.parser import ExpressionParser
class ExpressionManager:
    def __init__(self):
        self.expressions = {} # dict[str, DaskExpression]
        self.parser = ExpressionParser()

    