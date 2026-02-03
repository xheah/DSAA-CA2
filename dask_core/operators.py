class Operator:
    symbol = ""

    def apply(self, evaluator, left, right):
        raise NotImplementedError


class AddOperator(Operator):
    symbol = "+"

    def apply(self, evaluator, left, right):
        return left + right


class SubOperator(Operator):
    symbol = "-"

    def apply(self, evaluator, left, right):
        return left - right


class MulOperator(Operator):
    symbol = "*"

    def apply(self, evaluator, left, right):
        return left * right


class DivOperator(Operator):
    symbol = "/"

    def apply(self, evaluator, left, right):
        if right == 0:
            return None
        return left / right


class SumOperator(Operator):
    symbol = "++"

    def apply(self, evaluator, left, right):
        return evaluator._sum_to(left) + evaluator._sum_to(right)


class DivSumOperator(Operator):
    symbol = "//"

    def apply(self, evaluator, left, right):
        divisor = evaluator._sum_to(right)
        if divisor == 0:
            return None
        return evaluator._sum_to(left) / divisor


class PowOperator(Operator):
    symbol = "**"

    def apply(self, evaluator, left, right):
        return left**right


def build_operator_registry():
    operators = [
        AddOperator(),
        SubOperator(),
        MulOperator(),
        DivOperator(),
        SumOperator(),
        DivSumOperator(),
        PowOperator(),
    ]
    return {op.symbol: op for op in operators}
