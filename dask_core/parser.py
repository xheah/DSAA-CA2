"""
Builds parse tree from tokens
"""
class ExpressionParser:
    def __init__(self):
        self.operators = ['+', '-', '*', '/', '++', '**', '//']
    
    def parse(self, expr: str = None):
        if expr is None:
            return None
        
        i = 0
        while i < len(expr):
            if expr[i] == '(':
                pass