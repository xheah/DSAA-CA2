"""
Builds parse tree from tokens
"""
class ExpressionParser:
    def __init__(self):
        self.operators = ['+', '-', '*', '/', '++', '**', '//']