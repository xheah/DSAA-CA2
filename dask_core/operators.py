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


def _is_positive_integer(value) -> bool:
    """Check if value is a positive integer (or float with no decimal part)."""
    if isinstance(value, int):
        return value > 0
    if isinstance(value, float):
        return value > 0 and value.is_integer()
    return False


class SumOperator(Operator):
    symbol = "++"

    def apply(self, evaluator, left, right):
        if not _is_positive_integer(left) or not _is_positive_integer(right):
            return None
        return evaluator._sum_to(int(left)) + evaluator._sum_to(int(right))


class DivSumOperator(Operator):
    symbol = "//"

    def apply(self, evaluator, left, right):
        if not _is_positive_integer(left) or not _is_positive_integer(right):
            return None
        divisor = evaluator._sum_to(int(right))
        if divisor == 0:
            return None
        return evaluator._sum_to(int(left)) / divisor


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
