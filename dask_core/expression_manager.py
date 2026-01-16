"""
Manages all expressions (add, modify, lookup, sort)
"""
from dask_core.parser import ExpressionParser
from dask_core.expression import DaskExpression
import re
class ExpressionManager:
    def __init__(self):
        self.expressions: dict[str, DaskExpression] = {} # dict[str, DaskExpression]
        self.parser = ExpressionParser()
        self.add_expression("Alpha", "(2+(4*5))")
        self.add_expression("Pi", "(Alpha*3)")
        self.add_expression("Mango", "((Alpha+(Delta+(Pi*(Beta*(Gamma/Sigma)))))/2)")

    def add_expression(self, var_name: str, expression_str: str):
        """
        Docstring for add_expression
        
        :param self: Description
        :param var_name: Description
        :type var_name: str
        :param expression_str: Description
        :type expression_str: str
        """
        # expression = self.parser.parse(var_name, expression_str)
        self.expressions[var_name] = DaskExpression(var_name, expression_str)

    def validate_expression(self, expression:str) -> tuple:
        """
        Validate whether an expression fits all the conventions of a DASK Expression.
        
        :param self: EM
        :param expression: Dask Expression
        :type expression: str
        
        Returns:
            tuple: error message, boolean of whether valid, var_name, var_expression
        """
        valid_operators = {'+', '-', '*', '/', '**', '++', '//'}
        allowed_chars = set('0123456789+-*/()=.')

        if '=' not in expression:
            return "*Missing '=' sign in expression. Please re enter the expression*", False, '', ''
        
        if expression.count('=') > 1:
            return "*Multiple '=' signs in expression. Please re enter the expression*", False, '', ''

        if expression.count('(') != expression.count(')'):
            return "*Mismatched parentheses in expression. Please re enter the expression*", False, '', ''
        
        if re.search(r'\(\s*\)', expression):
            return "*Empty parentheses in expression. Please re enter the expression*", False, '', ''
            
        for char in expression:
            if char not in valid_operators and char not in allowed_chars and not char.isalpha():
                return f"*Invalid character '{char}' in expression. Please re enter the expression*", False, '', ''
            

        name, expr = expression.split('=', 1)
        name = name.strip()
        expr = expr.strip()

        if not re.match(r'^[a-zA-Z_]+$', name):
            return "*Invalid variable name. Please re enter the expression*", False, '', ''
        
        if re.search(r'[\+\-*/^][\s\)]*$', expr):
            return "*Expression cannot end with an operator. Please re enter the expression*", False, '', ''
        
        if re.search(r'^[+\-*/^]\s*', expr):
            return "*Expression cannot start with an operator. Please re enter the expression*", False, '', ''

        if re.search(r'(^|[=(*/+])\s*-\s*[\d\.]', expr):
            return "*Negative numbers are not allowed. Please re enter the expression*", False, '', ''

        for number in re.findall(r'[\d\.]+', expr):
            if not re.fullmatch(r'(\d+(\.\d*)?|\.\d+)', number):
                return "*Invalid number format. Please re enter the expression*", False, '', ''
        
        if expr == '':
            return "*Expression cannot be empty. Please re enter the expression*", False, '', ''
        
        if '(' not in expr or ')' not in expr:
            return "*Empty parentheses in expression. Please re enter the expression*", False, '', ''   
    
        return '', True, name, expr
        
    def get_expression(self):
        pass

    def evaluate_all(self): # re-evaluate all the values for all dask expressions contained within EM
        for var_name, expr in self.expressions.items():
            expr.value = expr.evaluate(context=self.expressions)