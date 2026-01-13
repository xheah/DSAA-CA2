"""
Turning a string into tokens
Convert a raw expression like (Alpha+(Delta+(Pi*(Beta*(Gamma/Sigma)))))
into a list like 
["(", "Alpha", "+", "(", "Delta", "+", "(", "Pi", "*", "(", "Beta", "*", "(", "Gamma", "/", "Sigma", ")", ")", ")", ")", ")"]

"""
from string import ascii_letters
class Lexer:
    def __init__(self):
        pass

    def tokenize(self, expr: str) -> list[str]:
        tokens = []
        var = ''
        for ch in expr:
            if ch not in ascii_letters:
                if len(var) > 0:
                    tokens.append(var)
                    var = ''
                tokens.append(ch)
            else:
                var += ch
        # Add any remaining variable at the end
        if len(var) > 0:
            tokens.append(var)
        return tokens
    

                